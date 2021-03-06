from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.base import TemplateView
from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('login/', LoginView.as_view(template_name="account/login.html"),
         name="login"),
    path('logout/', LogoutView.as_view(template_name="account/logout.html"),
         name="logout"),
    path('index/', views.index, name='index'),

    # 忘记密码
    path('password-reset/', PasswordResetView.as_view(
        template_name="account/password_reset_form.html",
        email_template_name="account/password_reset_email.html",
        subject_template_name="account/password_reset_subject.txt",
        success_url="/password-reset-done/"
    ), name="password_reset"),

    path("password-reset-done/", PasswordResetDoneView.as_view(
        template_name="account/password_reset_done.html"
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="account/password_reset_confirm.html",
             success_url='/password-reset-complete/'),
         name="password_reset_confirm"),

    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

    # 修改密码
    path('password_change/',views.password_change,name="password_change"),

    # 用户详情
    path('user_list/', views.user_list, name="user_list"),
    path('user_list/create_user', views.create_user, name='create_user'),
    path('user_list/del_user', views.del_user, name="del_user"),
    path('user_list/update_user', views.update_user, name="update_user"),

    # 用户组
    path('group_list/', views.group_list, name="group_list"),
    path('group_list/create_group', views.create_group, name="create_group"),
    path('group_list/del_group', views.del_group, name="del_group"),
    path('group_list/update_group', views.update_group, name="update_group"),
]
