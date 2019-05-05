import json

from apis.page_api import pages
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from apis.dbop import DataOperate


# Create your views here.
# @login_required(login_url='/login/')
@login_required
def index(request):
    return render(request, 'index.html')


@login_required
@csrf_exempt
def password_change(request):
    """
    修改密码
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request,"account/password_change_form.html")
    else:
        user = authenticate(username=request.user.username,
                            password=request.POST['id_old_psd'])
        if user and user.is_active:
            user.set_password(request.POST['id_new_psd'])
            user.save()
            dict_resp = {"e": 'success'}
        else:
            dict_resp = {"e": 'fail', "msg": "旧密码错误或用户已失效"}

        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False),
                            content_type="application/json")


@login_required
def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """
    pra_keyword = request.GET.get('keyword','')

    user_objs = User.objects.order_by("username")

    if pra_keyword:
        user_objs = user_objs.filter(username__contains=pra_keyword)

    _, p, objs, page_range, current_page, show_first, show_end = pages(
        user_objs, request)
    return render(request, "account/user_list.html",locals())


@login_required
def group_list(request):
    """
    组列表
    :param request:
    :return:
    """
    pra_keyword = request.GET.get('keyword','')

    group_objs = Group.objects.order_by("name")

    if pra_keyword:
        group_objs = group_objs.filter(name__contains=pra_keyword)

    _, p, objs, page_range, current_page, show_first, show_end = pages(
        group_objs, request)
    return render(request, "account/group_list.html", locals())


class UserGroupRelaForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset= User.objects.all(),
                                           required=True,
                                           widget=FilteredSelectMultiple(
                                               "用户:",is_stacked=False
                                           ))

    class Media:
        js = ('admin/js/vendor/jquery/jquery.js', 'admin/js/jquery.init.js')

    class Meta:
        model = User
        fields = ("username",)


@login_required
def create_group(request):
    """
    创建用户组
    :param request:
    :return:
    """
    user_form = UserGroupRelaForm()
    if request.method == "POST":
        user_form = UserGroupRelaForm(request.POST)
        try:
            usergroup = Group.objects.create(name=request.POST['usergroup'])

            user_objs = [User.objects.get(id=user_id) for user_id in request.POST.getlist('users','')]
            for i in user_objs:
                i.groups.add(usergroup)
            return HttpResponseRedirect(reverse('account:group_list'))
        except Exception as e:
            errors = str(e)
            return render(request, "account/create_group.html",locals())
    else:
        return render(request,"account/create_group.html",locals())


@login_required
@csrf_exempt
def del_group(request):
    """
    删除用户组
    :param request:
    :return:
    """
    group_id = request.POST['gid']
    status, msg = DataOperate.delete(Group, id=group_id)
    return HttpResponse(
        json.dumps({"e": status, "msg": msg}, ensure_ascii=False),
        content_type="application/json")


@login_required
@csrf_exempt
def update_group(request):
    """
    更新用户组
    :param request:
    :return:
    """
    if request.method == "GET":
        ugroup = DataOperate.get_object(Group, id=request.GET.get('gid'))
        uform = UserGroupRelaForm(
            initial={"users": ugroup.user_set.all()}
        )
        return render(request, "account/update_group.html", locals())

    else:
        try:
            ugroup = DataOperate.get_object(Group, id=request.POST['id_id'])
            # 判断是否已经有组名存在
            isgroup = Group.objects.filter(name=request.POST['usergroup']).exclude(id=request.POST['id_id'])
            if isgroup:
                raise Exception(
                    '已存在组名: ' + request.POST['usergroup'] + "，请重新输入")

            ugroup.name=request.POST['usergroup']
            ugroup.save()
            # 清除原来的关系
            ugroup.user_set.clear()

            user_objs = [User.objects.get(id=user_id) for user_id in
                         request.POST.getlist('users', '')]
            for i in user_objs:
                i.groups.add(ugroup)

            return HttpResponseRedirect(reverse('account:group_list'))
        except Exception as e:
            errors = str(e)

            uform = UserGroupRelaForm(
                initial={"users": ugroup.user_set.all()}
            )
            return render(request, "account/update_group.html", locals())
