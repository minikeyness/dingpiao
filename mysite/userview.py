from django.db import connection, transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect


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

