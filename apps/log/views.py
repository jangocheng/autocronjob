# -*- coding:utf-8 -*-

from django.views.generic import TemplateView, View
from user.views import LoginRequiredMixin
from django.shortcuts import render as my_render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from log.models import OperationLog, HistoryLogRecords
from django_celery_beat.models import PeriodicTask
from django.contrib.auth import get_user_model

import json
import datetime

User = get_user_model()


class OperationLogListView(LoginRequiredMixin, TemplateView):
    """
    日志分页显示 api
    """
    template_name = 'op_log.html'


class OperationLogView(LoginRequiredMixin, View):
    """
    非api 日志分页显示
    """
    def get(self, request):
        start_time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return my_render(request, 'op_log.html', locals())

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
            if item['name'] == 'op_user':
                search_data['op_user'] = item['value']
            if item['name'] == "search_time":
                search_data['op_time__range'] = item['value']
        if search_data:
            all_data_list = OperationLog.objects.filter(**search_data).order_by('-op_time')
        else:
            all_data_list = OperationLog.objects.all().order_by('-op_time')
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
            row = {"op_user": item.op_user,
                   "op_user_ip": item.op_user_ip,
                   "op_msg": item.op_msg,
                   "op_object": item.op_object,
                   "op_time": item.op_time.strftime('%Y-%m-%d %H:%M:%S'),
                   "is_success": "<span class='label label-success'>操作成功</span>" if item.is_success == True else "<span class='label label-default'>操作失败</span>" ,
                   "op_failed_msg": item.op_failed_msg}
            data.append(row)
        # 对最终的数据进行倒序排序
        data = sorted(data, key=lambda item: item['op_time'], reverse=True)
        dataTable['iTotalRecords'] = resultLength  # 数据总条数
        dataTable['sEcho'] = sEcho + 1
        dataTable['iTotalDisplayRecords'] = resultLength  # 显示的条数
        dataTable['aaData'] = data
        return HttpResponse(json.dumps(dataTable, ensure_ascii=False))


class HistoricalUserLog(LoginRequiredMixin, View):
    """
    非api task日志分页显示
    """
    def get(self, request):
        start_time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return my_render(request, 'histoty_records_periodictask.html', locals())

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
            if item['name'] == 'op_user':
                search_data['op_user'] = item['value']
            if item['name'] == "search_time":
                search_data['op_time__range'] = item['value']
        if search_data:
            all_data_list = HistoryLogRecords.objects.filter(**search_data).order_by('-op_time')
        else:
            all_data_list = HistoryLogRecords.objects.all().order_by('-op_time')
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
            row = {"op_user": item.op_user,
                   "op_msg": item.op_msg,
                   "op_type": item.op_type,
                   "op_time": item.op_time.strftime('%Y-%m-%d %H:%M:%S')}
                   # "is_success": "<span class='label label-success'>操作成功</span>" if item.is_success == True else "<span class='label label-default'>操作失败</span>" ,
                   # "op_failed_msg": item.op_failed_msg}
            data.append(row)
        # 对最终的数据进行倒序排序
        data = sorted(data, key=lambda item: item['op_time'], reverse=True)
        dataTable['iTotalRecords'] = resultLength  # 数据总条数
        dataTable['sEcho'] = sEcho + 1
        dataTable['iTotalDisplayRecords'] = resultLength  # 显示的条数
        dataTable['aaData'] = data
        return HttpResponse(json.dumps(dataTable, ensure_ascii=False))
