import json

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# @login_required(login_url='/login/')
@login_required
def index(request):
    return render(request, 'index.html')


@login_required
@csrf_exempt
def password_change(request):
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
