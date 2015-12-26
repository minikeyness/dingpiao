from django.db import connection, transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import Http404, HttpResponse
from django.contrib import auth
import json


# 检测是否登录，否则跳转到登录页面
@login_required(redirect_field_name=None, login_url="/login/?msg=login")
def usercontact(requset):
    cursor = connection.cursor()
    sql = u'select * FROM peoples where uId=%s' % (requset.user.id, )
    cursor.execute(sql)
    peoplelist = cursor.fetchall()
    # names = [{row[0]} for row in peoplelist]
    # cursor.execute("call Proc_Set_Isread(%s,%s)",[id,'1']) 存储过程的执行
    return render(requset, "contactpage.html", {"peoples": peoplelist})


# 检测是否登录，否则跳转到登录页面
@login_required(redirect_field_name=None, login_url="/login/?msg=login")
def userinfo(requset):
    return render(requset, "userpage.html")


@login_required(redirect_field_name=None, login_url="/login/?msg=login")
def modifypwd(req):
    if req.is_ajax() and req.method == 'POST':
        u = req.user
        oldpwd = req.POST.get('ch_oldpwd')
        pwd1 = req.POST.get('ch_cifpwd1')
        pwd2 = req.POST.get('ch_cifpwd2')
        if u.check_password(oldpwd):
            if pwd1 == pwd2:
                try:
                    newpwd = u.hashed_password(pwd2)
                    u.changepwd(newpwd=newpwd)
                except Exception as e:
                    return HttpResponse(json.dumps({"msg": "修改失败!"}))
                else:
                    auth.logout(req)
                    return HttpResponse(json.dumps({"msg": "修改成功！请重新登录！", "suc": 'true'}))
            else:
                return HttpResponse(json.dumps({"msg": "两次密码输入不一致！"}))
        else:
            return HttpResponse(json.dumps({"msg": "密码错误!"}))
    else:
        return Http404()


@login_required(redirect_field_name=None, login_url="/login/?msg=login")
def addreal(req):
    pass