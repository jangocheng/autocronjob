# -*- coding:utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import render as my_render
from django.views.generic import TemplateView, ListView, View

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import HttpResponse
from django.contrib import auth
from .forms import LoginForm
from .models import UserProfile
from utils.admin_permission import superpermission
from django.contrib.auth import get_user_model
import json
import datetime

User = get_user_model()


class LoginRequiredMixin(AccessMixin):

    @method_decorator(login_required(redirect_field_name='next', login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            'next': self.request.GET.get('next', '')
        })
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        login_form = self.get_form()
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            pass_word = login_form.cleaned_data['password']
            if User.objects.filter(username=user_name).exists():
                next = request.POST.get('next', '')
                user = authenticate(username=user_name, password=pass_word)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.session.clear_expired()
                        if next:
                            return HttpResponseRedirect(next)
                        else:
                            return HttpResponseRedirect(reverse('index'))
                    else:
                        return my_render(request, "login.html", {"msq": "用户未激活，请联系管理！"})
                else:
                    return my_render(request, "login.html", {"msq": "用户未激活或密码错误，请联系管理员！"})
            else:
                return my_render(request, "login.html", {"msq": "用户不存在，请确定用户名后再次登录！"})
        else:
            return my_render(request, "login.html", {"msq": "用户验证失败，请联系管理员！", "login_form": login_form})


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect("/login/")


@method_decorator(superpermission, name='dispatch')
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "user_list.html"
    context_object_name = "user_info"


@method_decorator(superpermission, name='dispatch')
class UserCreateView(LoginRequiredMixin, TemplateView):
    template_name = "user_create.html"


class UserOpHistoryLog(LoginRequiredMixin, View):
    """
    非api 日志分页显示
    """
    def get(self, request):
        start_time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return my_render(request, 'user_history_op_log.html', locals())

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
            # if item['name'] == 'op_user':
            #     search_data['op_user'] = item['value']
            if item['name'] == "search_time":
                search_data['history_date__range'] = item['value']
        if search_data:
            all_data_list = User.history.filter(**search_data).order_by('-history_date')
        else:
            all_data_list = User.history.all().order_by('-history_date')
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

        # ope_type = {'~': 'update', '+': 'create', '-': 'delete'}
        # new_record, old_record, *_ = all_data_list
        # # print(User.history.all().count())
        # delta = new_record.diff_against(old_record)
        # for change in iter(delta.changes):
        #     print("{} changed from {} to {}".format(change.field, change.old, change.new))
        #     row = {"op_user": User.objects.get(id=new_record.history_user_id).username,
        #            "op_msg": "{} changed from {} to {}".format(change.field, change.old, change.new),
        #            "op_object": ope_type[new_record.history_type],
        #            "op_time": new_record.history_date.strftime('%Y-%m-%d %H:%M:%S')}
        #
        #     data.append(row)
        # 对最终的数据进行倒序排序
        data = sorted(data, key=lambda item: item['op_time'], reverse=True)
        dataTable['iTotalRecords'] = resultLength  # 数据总条数
        dataTable['sEcho'] = sEcho + 1
        dataTable['iTotalDisplayRecords'] = resultLength  # 显示的条数
        dataTable['aaData'] = data
        return HttpResponse(json.dumps(dataTable, ensure_ascii=False))
