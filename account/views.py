import json

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apis.page_api import pages

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

    assets_list, p, assets, page_range, current_page, show_first, show_end = pages(
        user_objs, request)
    return render(request, "account/user_list.html",locals())
