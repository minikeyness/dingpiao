from django.db import connection, transaction, IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
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


# 检测是否登录，否则跳转到登录页面,不实用next page
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
                except :
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
     if req.is_ajax() and req.method == 'POST':
        uid = req.user.id
        name = req.POST.get('realname')
        phone = req.POST.get('phone')
        idcard = req.POST.get('idcard')
        if name and phone and idcard:
            try:
                with transaction.atomic():
                    cursor = connection.cursor()
                    sql1 = u"UPDATE users SET realName = '%s',phoneNum = '%s',idCard ='%s' WHERE id =%s"\
                        % (name, phone, idcard, uid, )
                    sql2 = u"INSERT INTO peoples(realName,idCard,phoneNum,uId) VALUES('%s', '%s', '%s' ,%s)"\
                        % (name, idcard, phone, uid)
                    cursor.execute(sql1)
                    cursor.execute(sql2)
            except : # 相当于不抛出异常,系统也就不会处理什么了
                return HttpResponse(json.dumps({"msg": "添加失败!"}))
            else:
                return HttpResponse(json.dumps({"msg": "添加成功！", "suc": 'true'}))
        else:
            return HttpResponse(json.dumps({"msg": "三项数据都不能为空！"}))
     else:
        return Http404()


@login_required(redirect_field_name=None, login_url="/login/?msg=login")
def addotherreal(req):
    if req.is_ajax() and req.method == 'POST':
        uid = req.user.id
        name = req.POST.get('realname')
        phone = req.POST.get('phone')
        idcard = req.POST.get('idcard')
        if name and phone and idcard:
            try:
                cursor = connection.cursor()
                sql = u"INSERT INTO peoples(realName,idCard,phoneNum,uId) VALUES('%s', '%s', '%s' ,%s)"\
                    % (name, idcard, phone, uid)
                cursor.execute(sql)
            except: # 相当于不抛出异常,系统也就不会处理什么了
                return HttpResponse(json.dumps({"msg": "添加失败!"}))
            else:
                return HttpResponse(json.dumps({"msg": "添加成功！", "suc": 'true'}))
        else:
            return HttpResponse(json.dumps({"msg": "三项数据都不能为空！"}))
    else:
        return Http404()


@login_required(redirect_field_name=None, login_url="/login/?msg=login")
def delpeople(req):
    if req.is_ajax() and req.method == 'POST':
        did = req.POST.get('id')
        if did:
            try:
                cursor = connection.cursor()
                sql = u"DELETE FROM peoples WHERE id =%s" % (did,)
                cursor.execute(sql)
            except: # 相当于不抛出异常,系统也就不会处理什么了
                return HttpResponse(json.dumps({"msg": "删除失败!"}))
            else:
                return HttpResponse(json.dumps({"msg": "删除成功！", "suc": 'true'}))
        else:
            return HttpResponse(json.dumps({"msg": "三项数据都不能为空！"}))
    else:
        return Http404()

@login_required(redirect_field_name=None, login_url="/login/?msg=login")
def order(request):
        return render(request, "ordersearch.html")

def searchorder ( request) :
   # if request.method = 'POST'
    startstation1 = request.POST.get("startstation")
    endstation1 = request.POST.get("endstation")
    date1 = request.POST.get("date")
    cursor = connection.cursor()
    sql = u"SELECT trainnum FROM trainticketonline_train_station WHERE trainnum IN (" \
          u" SELECT trainnum  From trainticketonline_train_station" \
          u" where station = ( SELECT stationnum"\
          u"  FROM trainticketonline_station" \
          u" WHERE stationname = '%s' ))  AND " \
          u"station = ( SELECT stationnum" \
          u" FROM trainticketonline_station" \
          u" WHERE stationname= '%s' ) "%(startstation1,endstation1)
    cursor.execute(sql)
    trainlist = cursor.fetchall()
    ticketlist = ()
    starttimeandprice = ()
    endtimeandprice = ()
    starttime = ()
    endtime = ()
    numoftrain = 0
    for train in trainlist:
       sql = u"SELECT COUNT(*)  FROM trainticketonline_trainseat " \
             u"WHERE trainticketonline_trainseat.date= ' "+date1+" ' " \
             u"AND trainticketonline_trainseat.trainnum='%s' " \
             u"AND trainticketonline_trainseat.seatstatus1 = '1'" %(train)
       cursor.execute(sql)
       ticketlist = ticketlist + cursor.fetchall()
       sql = u"select price" \
             u" FROM trainticketonline_train_station" \
             u" WHERE station = (SELECT stationnum" \
             u" FROM trainticketonline_station" \
             u" WHERE stationname = '"+startstation1+"')" \
             u"AND trainnum = '%s'"%(train)
       cursor.execute(sql)
       starttimeandprice = starttimeandprice + cursor.fetchall()
       sql = u"select price" \
             u" FROM trainticketonline_train_station" \
             u" WHERE station = ( SELECT stationnum" \
             u" FROM trainticketonline_station" \
             u" WHERE stationname = '"+endstation1+"' )" \
             u"AND trainnum = '%s' "%(train)
       cursor.execute(sql)
       endtimeandprice = endtimeandprice + cursor.fetchall()
       sql = u"select outtime" \
             u" FROM trainticketonline_train_station" \
             u" WHERE station = ( SELECT stationnum" \
             u" FROM trainticketonline_station" \
             u" WHERE stationname = '"+startstation1+"' )" \
             u"AND trainnum = '%s' "%(train)
       cursor.execute(sql)
       starttime = starttime + cursor.fetchall()
       sql = u"select intime" \
             u" FROM trainticketonline_train_station" \
             u" WHERE station = ( SELECT stationnum" \
             u" FROM trainticketonline_station" \
             u" WHERE stationname = '"+endstation1+"' )" \
             u"AND trainnum = '%s' "%(train)
       cursor.execute(sql)
       endtime = endtime + cursor.fetchall()
       numoftrain = len(ticketlist)
    return HttpResponse(json.dumps({"trainlist": trainlist,"ticketlist":ticketlist,
                                    "startprice":starttimeandprice
                                    ,"endprice":endtimeandprice
                                    , "starttime":starttime
                                    ,"endtime":endtime
                                    ,"numoftrain":numoftrain}
                                  )
                        )
