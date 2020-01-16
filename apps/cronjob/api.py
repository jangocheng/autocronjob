# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView, Response
from django_celery_beat.models import MailAddress, WebhookUrl, PeriodicTask
from cronjob.serializers import MailAddressSerializer, WebhookUrlSerializer
# 首页数据api接口
from django_celery_results.models import TaskResult
from rest_framework import status
from cronjob.client import CeleryClient
from utils.get_broker_data.get_broker_data import get_broker_data

try:
    import simplejson as json
except ImportError:
    import json
import datetime
import time


class MailAddressViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                         mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = MailAddress.objects.all()
    serializer_class = MailAddressSerializer


class WebhookUrlViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                        mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = WebhookUrl.objects.all()
    serializer_class = WebhookUrlSerializer


class IndexChartData(APIView):
    """
    首页数据
    """
    def get(self, request):
        date_list = list()
        success_count_list = list()
        failure_count_list = list()
        task_dict = dict()
        other_list = list()
        not_consume_list = list()
        instance = CeleryClient()
        response = instance.workers()
        task_obj = PeriodicTask.objects.all()
        # task执行状态数量
        task_total_num = task_obj.count()
        task_running_num = task_obj.filter(enabled=1).count()
        task_stop_num = task_obj.filter(enabled=0).count()
        # worker list
        for item in response:
            query_count = 0
            for query in item['queues']:
                not_consume_list.append(
                    {"x": f"{query}", "y": get_broker_data(query)})
                query_count += task_obj.filter(queue=query).count()
            task_dict[item['name']] = query_count
        # task周统计
        begin_date = (datetime.datetime.now() - datetime.timedelta(
            days=6)).strftime("%Y-%m-%d")
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(
            time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
        query = TaskResult.objects.filter(
            date_done__range=[begin_date, end_date.strftime(
                '%Y-%m-%d 23:59:59')
                              ], task_name='cronjob.tasks.runs_command'
        ).values('status')
        # 生成一周日期
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            date_time = [begin_date, begin_date.strftime('%Y-%m-%d 23:59:59')]
            success_count_list.append(query.filter(status='SUCCESS',
                                                   date_done__range=date_time
                                                   ).count())
            failure_count_list.append(query.filter(status='FAILURE',
                                                   date_done__range=date_time
                                                   ).count())
            other_list.append(
                query.filter(date_done__range=date_time).exclude(
                    status='SUCCESS').exclude(status='FAILURE').count())
            begin_date += datetime.timedelta(days=1)
        # 返回汇总数据
        chart_data = {"date_list": date_list,
                      "success_count_list": success_count_list,
                      "failure_count_list": failure_count_list,
                      "other_list": other_list,
                      "task_dict": task_dict,
                      "taskTotalNum": task_total_num,
                      "taskRunNum": task_running_num,
                      "taskStopNum": task_stop_num,
                      "notConsume": not_consume_list,
                      "workerNum": len(
                          response) if response is not None else 0}
        return Response(chart_data, status=status.HTTP_200_OK)
