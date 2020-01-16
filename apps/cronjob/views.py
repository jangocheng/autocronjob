# -*- coding:utf-8 -*-

from django.views.generic import View, DetailView, ListView, DeleteView, CreateView, UpdateView, TemplateView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render as my_render
from django.shortcuts import render_to_response
from django.contrib.messages.views import SuccessMessageMixin
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask, MailAddress, WebhookUrl
from django_celery_beat.admin import PeriodicTaskForm
from django_celery_results.models import TaskResult
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from celery import current_app
from django.urls import reverse_lazy
from rest_framework import status

from django.db.models import Count
from user.views import LoginRequiredMixin
from cronjob.client import CeleryClient
from utils.audit_record_decorator import dag_operation_log_decorator
from django.utils.decorators import method_decorator

from utils.get_broker_data.get_broker_data import get_broker_data
from utils.admin_permission import superpermission
try:
    import simplejson as json
except ImportError:
    import json
import datetime
import time


class AutoCronjobIndex(LoginRequiredMixin, View):
    """首页"""

    def get(self, request):
        """7天的数据"""
        return my_render(request, "index.html", locals())


class TaskExecuteStateView(View):

    def get(self, request):
        date_list = list()
        success_count_list = list()
        failure_count_list = list()
        task_dict = dict()
        other_list = list()
        queue_list = list()
        instance = CeleryClient()
        response = instance.workers()
        task_obj = PeriodicTask.objects.all()
        # task status num
        task_total_num = task_obj.count()
        task_running_num = task_obj.filter(enabled=1).count()
        task_stop_num = task_obj.filter(enabled=0).count()
        # worker list
        for item in response:
            query_count = 0
            for query in item['queues']:
                queue_list.append([query, get_broker_data(query)])
                query_count += task_obj.filter(queue=query).count()
            task_dict[item['name']] = query_count
        # task周统计
        begin_date = (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d")
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
        query = TaskResult.objects.filter(date_done__range=[begin_date, end_date.strftime('%Y-%m-%d 23:59:59')],
                                          task_name='cronjob.tasks.runs_command').values('status')
        # 生成一周日期
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            date_time = [begin_date, begin_date.strftime('%Y-%m-%d 23:59:59')]
            success_count_list.append(query.filter(status='SUCCESS', date_done__range=date_time).count())
            failure_count_list.append(query.filter(status='FAILURE', date_done__range=date_time).count())
            other_list.append(
                query.filter(date_done__range=date_time).exclude(status='SUCCESS').exclude(status='FAILURE').count())
            begin_date += datetime.timedelta(days=1)
        # 返回汇总数据
        chart_data = {"date_list": date_list,
                      "success_count_list": success_count_list,
                      "failure_count_list": failure_count_list,
                      "other_list": other_list,
                      "task_dict": task_dict,
                      "task_total_num": task_total_num,
                      "task_running_num": task_running_num,
                      "task_stop_num": task_stop_num,
                      "queue_list": queue_list,
                      "celery_worker_num": len(response) if response is not None else 0}
        return JsonResponse(chart_data, status=status.HTTP_200_OK)


class MailListView(LoginRequiredMixin, ListView):
    """邮件告警列表"""
    model = MailAddress
    template_name = "mail_list.html"
    context_object_name = "mail_info"


class MailCreateView(LoginRequiredMixin, TemplateView):
    """创建邮件告警地址"""
    template_name = "mail_create.html"


class WebhookListView(LoginRequiredMixin, ListView):
    """webhook 列表"""
    model = WebhookUrl
    template_name = "webhook_list.html"
    context_object_name = "webhook_list"


class WebhookCreateView(LoginRequiredMixin, TemplateView):
    """创建webhook"""
    template_name = "webhook_create.html"


class workers(LoginRequiredMixin, View):
    """
    worker
    """

    def get(self, request):
        instance = CeleryClient()
        response = instance.workers()

        if not response:
            return HttpResponse(json.dumps([]), content_type="application/json")
        else:
            return HttpResponse(json.dumps(response), content_type="application/json")

    def post(self, request):
        pass


@method_decorator(superpermission, name='dispatch')
class WorkersIndex(LoginRequiredMixin, View):
    """
    worker 列表
    """

    def get(self, request):
        instance = CeleryClient()
        response = instance.workers()
        return render_to_response('workers.html', locals())


@method_decorator(superpermission, name='dispatch')
class PoolConfiguration(LoginRequiredMixin, View):
    """
    pool 配置
    """

    def get(self, request):
        instance = CeleryClient()
        stats = instance.worker_stats
        return render_to_response('pool_configuration.html', locals())


@method_decorator(superpermission, name='dispatch')
class QueuesConfiguration(LoginRequiredMixin, View):
    """
    队列配置
    """

    def get(self, request):
        instance = CeleryClient()
        response = instance.active_queues()
        return render_to_response('queues_configuration.html', locals())

    def post(self, request):
        pass


class Operations(LoginRequiredMixin, View):
    """
    操作，针对动态函数进行操作
    """

    def get(self, request):
        command = self.request.GET.get('command', '')
        parameter = json.loads(self.request.GET.get('parameter', ''))
        instance = CeleryClient()
        response = instance.execute(command, parameter)
        return HttpResponse(json.dumps(response), content_type="application/json")


@method_decorator(dag_operation_log_decorator('创建Crontab任务'), name="post")
class PeriodicTaskCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    创建定时任务
    """
    form_class = PeriodicTaskForm
    template_name = 'periodictask_create.html'
    success_url = reverse_lazy('periodictask_list')
    success_message = "%(name)s was created successfully"
    model = PeriodicTask

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        active_queues = CeleryClient().active_queues()
        kwargs.update({
            "regtasks": list(sorted(name for name in current_app.tasks if not name.endswith('tailf_log'))),
            "queues": [queue_info['name'] for hostname, all_queue_info in active_queues.items() for
                       queue_info in all_queue_info] if active_queues else ['None']
        })
        return kwargs


@method_decorator(dag_operation_log_decorator('更新Crontab任务'), name="post")
class PeriodicTaskUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    更新定时任务
    """
    form_class = PeriodicTaskForm
    template_name = 'periodictask_update.html'
    success_url = reverse_lazy('periodictask_list')
    success_message = "%(name)s was updated successfully"
    model = PeriodicTask

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        active_queues = CeleryClient().active_queues()
        kwargs.update({
            "regtasks": list(sorted(name for name in current_app.tasks if not name.endswith('tailf_log'))),
            "queues": [queue_info['name'] for hostname, all_queue_info in active_queues.items() for
                       queue_info in all_queue_info] if active_queues else ['None']
        })
        return kwargs


class PeriodicTaskList(LoginRequiredMixin, ListView):
    """
    定时任务列表
    """
    template_name = 'periodictask_list.html'
    context_object_name = "job_list"
    model = PeriodicTask


class PeriodicTaskDetail(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    定时任务的详细
    """
    form_class = PeriodicTaskForm
    template_name = 'periodictask_detail.html'
    success_url = reverse_lazy('periodictask_list')
    model = PeriodicTask

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            "regtasks": list(sorted(name for name in current_app.tasks if not name.endswith('tailf_log')))
        })
        return kwargs


@method_decorator(dag_operation_log_decorator('删除Crontab任务'), name="delete")
class PeriodicTaskDelete(LoginRequiredMixin, DeleteView):
    """
    删除定时任务
    """
    model = PeriodicTask

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'delete failed, error:%s' % e},
                                status=status.HTTP_403_FORBIDDEN)
        return JsonResponse({'status': True, 'message': 'deleted success!'}, status=status.HTTP_200_OK)


@method_decorator(dag_operation_log_decorator('创建Crontab间隔'), name="post")
class CrontabCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    crontab create
    """
    template_name = 'crontab_create.html'
    success_url = reverse_lazy('crontab_list')
    success_message = "crontab was created successfully"
    model = CrontabSchedule
    fields = ['minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year']


class CrontabList(LoginRequiredMixin, SuccessMessageMixin, ListView):
    """
    定时时间列表
    """
    template_name = 'crontab_list.html'
    model = CrontabSchedule
    context_object_name = 'crontab_list'
    success_url = reverse_lazy('crontab_list')


@method_decorator(dag_operation_log_decorator('更新Crontab间隔'), name="post")
class CrontabUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    更新定时时间
    """
    template_name = 'crontab_update.html'
    model = CrontabSchedule
    success_message = "crontab was updated successfully"
    success_url = reverse_lazy('crontab_list')
    fields = ['minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year']


@method_decorator(dag_operation_log_decorator('删除Crontab间隔'), name="delete")
class CrontabDelete(LoginRequiredMixin, DeleteView):
    """
    删除定时时间
    """
    model = CrontabSchedule

    # success_url = reverse_lazy('crontab_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'deleted failed, error:%s' % e},
                                status=status.HTTP_403_FORBIDDEN)
        return JsonResponse({'status': True, 'message': 'deleted success!'}, status=status.HTTP_200_OK)


class IntervalList(LoginRequiredMixin, ListView):
    """
    时间间隔列表
    """
    template_name = 'interval_list.html'
    model = IntervalSchedule
    context_object_name = 'interval_list'


@method_decorator(dag_operation_log_decorator('创建Interval间隔'), name="post")
class IntervalCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    时间间隔创建
    """
    template_name = 'interval_create.html'
    success_url = reverse_lazy('interval_list')
    success_message = "interval was created successfully"
    model = IntervalSchedule
    fields = '__all__'


@method_decorator(dag_operation_log_decorator('更新Interval间隔'), name="post")
class IntervalUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    更新时间间隔
    """
    template_name = 'interval_update.html'
    success_url = reverse_lazy('interval_list')
    model = IntervalSchedule
    success_message = "interval was updated successfully"
    fields = '__all__'


@method_decorator(dag_operation_log_decorator('删除Interval间隔'), name="delete")
class IntervalDelete(LoginRequiredMixin, DeleteView):
    """
    删除时间间隔
    """
    model = IntervalSchedule

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'delete failed, error:%s' % e},
                                status=status.HTTP_403_FORBIDDEN)
        return JsonResponse({'status': True, 'message': 'deleted success!'},
                            status=status.HTTP_200_OK)


class RunTask(LoginRequiredMixin, View):
    """
    手动运行任务
    """

    def get(self, request):
        id = self.request.GET.get('id', None)
        name = self.request.GET.get('name', None)
        try:
            querry_res = PeriodicTask.objects.get(id=id, name=name)
            args = json.loads(querry_res.args)
            kwargs = json.loads(querry_res.kwargs)
            queue = querry_res.queue
            routing_key = querry_res.routing_key
            task_name = querry_res.task
        except ObjectDoesNotExist:
            response = {'status': 'fail', 'message': 'task name %s doesn\'t exits' % (name)}
            return HttpResponse(json.dumps(response), content_type="application/json", status=status.HTTP_403_FORBIDDEN)
        if queue == 'None' or queue == None:
            queue = 'celery'
        res = current_app.send_task(task_name,
                                    args=args,
                                    kwargs=kwargs,
                                    queue=queue,
                                    routing_key=routing_key,
                                    # reply=True, # 异步发送指令，无需等待
                                    # max_retries=3, # 最大重试
                                    # soft_time_limit=80000,
                                    # time_limit=86400 # 设置为24小时，任务超时，如果未完成将被kill掉，并启动新的worker去代替
                                    )
        response = {'status': 'success', 'message': 'task name %s has been running,task id is %s' % (name, res.id)}
        return HttpResponse(json.dumps(response), content_type="application/json", status=status.HTTP_200_OK)


class StopTask(LoginRequiredMixin, View):
    """
    手动停止定时任务
    """

    def get(self, request):
        id = request.GET.get('id')
        name = request.GET.get('name')
        enable = "0"
        try:
            querry_res = PeriodicTask.objects.get(id=id, name=name)
            # querry_res.update(**{"enabled": enable})
            querry_res.enabled = enable
            querry_res.save()

        except ObjectDoesNotExist:
            response = {'status': 'fail', 'message': 'task name %s doesn\'t exits' % (name)}
            return HttpResponse(json.dumps(response), content_type="application/json", status=status.HTTP_403_FORBIDDEN)
        response = {'status': 'success', 'message': 'task name %s has been stopping.' % (name)}
        return HttpResponse(json.dumps(response), content_type="application/json", status=status.HTTP_200_OK)


class TaskResultDetail(LoginRequiredMixin, DetailView):
    """
    定时任务结果的详细
    """
    model = TaskResult
    template_name = 'taskresult_detail.html'


class TaskResultView(LoginRequiredMixin, View):
    """
    非api 任务结果分页显示
    """

    def get(self, request):
        start_time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return my_render(request, 'taskresult_list.html', locals())

    def post(self, request):

        dataTable = {}
        search_data = {}
        aodata = json.loads(request.POST.get("aodata"))
        for item in aodata:
            if item['name'] == "sEcho":
                sEcho = int(item['value'])  # 客户端发送的标识
            if item['name'] == "iDisplayStart":
                iDisplayStart = int(item['value'])  # 起始索引
            if item['name'] == "iDisplayLength":
                iDisplayLength = int(item['value'])  # 每页显示的行数
            if item['name'] == "task_kwargs":
                search_data['task_kwargs__contains'] = item['value']
            if item['name'] == "search_time":
                search_data['date_done__range'] = item['value']

        if search_data:
            all_data_list = TaskResult.objects.filter(**search_data).order_by('-date_done')
        else:
            all_data_list = TaskResult.objects.all().order_by('-date_done')
        resultLength = all_data_list.count()
        # 对list进行分页
        paginator = Paginator(all_data_list, iDisplayLength)
        # 把数据分成10个一页。
        try:
            all_data_list = paginator.page(iDisplayStart / 10 + 1)
        # 请求页数错误
        except PageNotAnInteger:
            all_data_list = paginator.page(1)
        except EmptyPage:
            all_data_list = paginator.page(paginator.num_pages)
        data = []
        for item in all_data_list:
            row = {"task_id": item.task_id,
                   "task_name": item.task_name,
                   "task_kwargs": item.task_kwargs,
                   "date_done": item.date_done.strftime('%Y-%m-%d %H:%M:%S'),
                   "id": item.id,
                   "status": "<span  style='color: #00ff00;font-weight: 900'>%s</span>" % item.status if item.status == 'SUCCESS' else "<span style='color: #ff0000;font-weight: 900'>%s</span>" % item.status,
                   }
            data.append(row)
        # 对最终的数据进行倒序排序
        data = sorted(data, key=lambda item: item['date_done'], reverse=True)
        dataTable['iTotalRecords'] = resultLength  # 数据总条数
        dataTable['sEcho'] = sEcho + 1
        dataTable['iTotalDisplayRecords'] = resultLength  # 显示的条数
        dataTable['aaData'] = data
        return HttpResponse(json.dumps(dataTable, ensure_ascii=False))


class TaskStateSucessRateApi(LoginRequiredMixin, View):
    def get(self, request):
        task_name = self.request.GET.get('task_name', None)
        start_time = self.request.GET.get('start_time', (datetime.datetime.now() - datetime.timedelta(days=3)).strftime(
            '%Y-%m-%d %H:%M:%S'))
        end_time = self.request.GET.get('end_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        taskstate_data = list()
        [taskstate_data.append({'name': i['status'], 'y': int(i['total']), }) for i in
         TaskResult.objects.filter(date_done__range=[start_time, end_time]).filter(task_name=task_name).values(
             'status').annotate(total=Count('status')).order_by('total')]
        for taskstate in taskstate_data:
            if taskstate['name'] == 'SUCCESS':
                taskstate['color'] = '#66ff33'
            elif taskstate['name'] == 'FAILURE':
                taskstate['color'] = 'red'
        chart_data = {'name': task_name, 'data': taskstate_data}
        return HttpResponse(json.dumps(chart_data), content_type="application/json")


class TaskStateFailureCountApi(LoginRequiredMixin, View):
    def get(self, request):
        task_name = self.request.GET.get('task_name', None)
        start_time = self.request.GET.get('start_time', (datetime.datetime.now() - datetime.timedelta(days=3)).strftime(
            '%Y-%m-%d %H:%M:%S'))
        end_time = self.request.GET.get('end_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data = list()
        task_name = list()
        [[data.append(i['failure_count']), task_name.append(i['task_name'])] for i in
         TaskResult.objects.values('task_name').filter(date_done__range=[start_time, end_time]).filter(
             status='FAILURE').annotate(failure_count=Count('status')).order_by('-failure_count')]
        return HttpResponse(json.dumps({'data': data, 'task_name_cat': task_name}), content_type="application/json")


class TaskStateExecuteCountApi(LoginRequiredMixin, View):
    def get(self, request):
        start_time = self.request.GET.get('start_time', (datetime.datetime.now() - datetime.timedelta(days=3)).strftime(
            '%Y-%m-%d %H:%M:%S'))
        end_time = self.request.GET.get('end_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        task_name = self.request.GET.get('task_name', None)
        query = TaskResult.objects.filter(date_done__range=[start_time, end_time]).filter(task_name=task_name).values(
            'status')
        failure_count = query.filter(status='FAILURE').count()
        execute_count = query.filter(status='SUCCESS').count()
        chart_data = {'name': task_name, 'data': [failure_count, execute_count],
                      'task_name_cat': ['failure_count', 'execute_count']}
        return HttpResponse(json.dumps(chart_data), content_type="application/json")


class TaskStateChart(LoginRequiredMixin, View):
    def get(self, request):
        start_time = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        task_name_list = PeriodicTask.objects.order_by().values('task').distinct()
        return render_to_response('taskstatechart.html', locals())


@method_decorator(superpermission, name='dispatch')
class RegisteredTasksIndex(LoginRequiredMixin, View):
    def get(self, request):
        instance = CeleryClient()
        response = instance.registered_tasks()
        return render_to_response('registered_tasks.html', locals())


@method_decorator(superpermission, name='dispatch')
class WorkerStatus(LoginRequiredMixin, View):
    def get(self, request):
        instance = CeleryClient()
        stats = instance.worker_stats
        active_tasks = instance.active_tasks()
        reserved_tasks = instance.reserved_tasks()
        revoked_tasks = instance.revoked_tasks()
        scheduled_tasks = instance.scheduled_tasks()
        return render_to_response('worker_status.html', locals())
