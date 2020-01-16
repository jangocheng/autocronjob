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

from django.contrib import auth
from .forms import LoginForm
from utils.admin_permission import superpermission
from django.contrib.auth import get_user_model
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
