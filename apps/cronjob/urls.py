# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from django.conf.urls import re_path
from cronjob.views import (WorkersIndex, Operations, PoolConfiguration,
                           QueuesConfiguration, PeriodicTaskList,
                           CrontabCreate, CrontabList, CrontabUpdate,
                           CrontabDelete, PeriodicTaskCreate, IntervalList,
                           RunTask, StopTask, TaskResultView, AutoCronjobIndex,
                           IntervalCreate, IntervalUpdate, IntervalDelete,
                           TaskResultDetail, TaskStateChart, PeriodicTaskDetail,
                           PeriodicTaskUpdate, PeriodicTaskDelete, TaskStateSucessRateApi,
                           TaskStateFailureCountApi, TaskStateExecuteCountApi,
                           RegisteredTasksIndex, WorkerStatus, MailListView, MailCreateView,
                           WebhookListView, WebhookCreateView, TaskExecuteStateView)

urlpatterns = [
    re_path(r'^$', AutoCronjobIndex.as_view(), name='index'),
    re_path(r'^mail/$', MailListView.as_view(), name='mail_list'),
    re_path(r'^mail/create/$', MailCreateView.as_view(), name='mail_add'),
    re_path(r'^webhook/$', WebhookListView.as_view(), name='webhook_list'),
    re_path(r'^webhook/create/$', WebhookCreateView.as_view(), name='webhook_add'),
    re_path(r'^workers/$', WorkersIndex.as_view(), name='workers_index'),
    re_path(r'^operations/$', Operations.as_view(), name='operations'),
    re_path(r'^pool_configuration/$', PoolConfiguration.as_view(), name='pool_configuration'),
    re_path(r'^queues_configuration/$', QueuesConfiguration.as_view(), name='queues_configuration'),
    re_path(r'^periodictask/add/$', PeriodicTaskCreate.as_view(), name='periodictask_add'),
    re_path(r'^periodictask/(?P<pk>[0-9]+)/update/$', PeriodicTaskUpdate.as_view(), name='periodictask_update'),
    re_path(r'^periodictask/$', PeriodicTaskList.as_view(), name='periodictask_list'),
    re_path(r'^periodictask/(?P<pk>[0-9]+)/$', PeriodicTaskDetail.as_view(), name="periodictask_detail"),
    re_path(r'^periodictask/delete/(?P<pk>[0-9]+)/$', PeriodicTaskDelete.as_view(), name='periodictask_delete'),
    re_path(r'^crontab/add$', CrontabCreate.as_view(), name='crontab_add'),
    re_path(r'^crontab/$', CrontabList.as_view(), name='crontab_list'),
    re_path(r'^crontab/(?P<pk>[0-9]+)/update/$', CrontabUpdate.as_view(), name='crontab_update'),
    re_path(r'^crontab/delete/(?P<pk>[0-9]+)/$', CrontabDelete.as_view(), name='crontab_delete'),
    re_path(r'^interval/$', IntervalList.as_view(), name='interval_list'),
    re_path(r'^interval/add/$', IntervalCreate.as_view(), name='interval_add'),
    re_path(r'^interval/(?P<pk>[0-9]+)/update/$', IntervalUpdate.as_view(), name='interval_update'),
    re_path(r'^interval/delete/(?P<pk>[0-9]+)/$', IntervalDelete.as_view(), name='interval_delete'),
    re_path(r'^taskresult/(?P<pk>[0-9]+)/$', TaskResultDetail.as_view(), name='taskresult_detail'),
    re_path(r'^taskresult/$', TaskResultView.as_view(), name='taskresult_list'),
    re_path(r'^task_state_chart/$', TaskStateChart.as_view(), name='task_state_chart'),
    re_path(r'^run_task/$', RunTask.as_view(), name='run_task'),
    re_path(r'^stop_task/$', StopTask.as_view(), name='stop_task'),
    re_path(r'^task_state_sucess_rate_api/$', TaskStateSucessRateApi.as_view(), name='task_state_sucess_rate_api'),
    re_path(r'^task_state_failure_count_api/$', TaskStateFailureCountApi.as_view(), name='task_state_failure_count_api'),
    re_path(r'^task_state_execute_count_api/$', TaskStateExecuteCountApi.as_view(), name='task_state_execute_count_api'),
    re_path(r'^registered_tasks_index/$', RegisteredTasksIndex.as_view(), name='registered_tasks_index'),
    re_path(r'^worker_status/$', WorkerStatus.as_view(), name='worker_status'),
    re_path(r'^api/taskexecutestate/$', TaskExecuteStateView.as_view(), name='taskexecutestate_api')
]

