"""autocronjob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.static import serve

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from cronjob.api import MailAddressViewSet, WebhookUrlViewSet, IndexChartData
from user.api import UserProfileViewSet
from log.api import OpLogViewSet

router = routers.DefaultRouter()
# 用户接口
router.register(r'user', UserProfileViewSet, base_name="user")
# 审计日志接口(审计内容待补充)
router.register(r'log', OpLogViewSet, base_name='log')
# mail接口
router.register(r'mail', MailAddressViewSet, base_name='mail')
# webhook接口
router.register(r'webhook', WebhookUrlViewSet, base_name='webhook')

urlpatterns = [
    path('admin/', admin.site.urls),
    # 应用接口
    path('api/', include(router.urls)),
    # 非api接口
    path('', include('user.urls')),
    path('', include('cronjob.urls')),
    path('', include('log.urls')),
    # index数据接口
    re_path(r'^api/index_chart_data/$', IndexChartData.as_view(), name='index_chart_data'),
    # drf登录认证
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # jwt认证
    re_path(r'^api/token-auth/$', obtain_jwt_token),
    # api文档
    re_path(r'^docs/', include_docs_urls(title="autocronjob")),
]
