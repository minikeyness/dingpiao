from django.shortcuts import render
from django.db import connection, transaction, IntegrityError
# from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth

# from django.contrib.auth.decorators import login_required
from mysite.forms import *
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
import json
from mysite.models import myJsonEncoder
def home(request):
    return render(request, 'home.html')
    #render_to_response需要加context_instance=
    #render（）可以自动验证crsf_token问题


def about(request):
    return render(request, 'about.html')




def ypcx (request) :
    return render(request,  "ypcx.html")

def alogin(request):
    if request.method == "GET":
        msg = request.GET.get('msg')
        if msg is not None and msg == 'login':
            msg = '请先登录！'
        elif msg is not None and msg == 'suc':
            msg = '修改密码成功!，请重新登录!'
        elif msg is not None and msg == 'err':
            msg = '用户名或密码错误!'
        else:
            msg = None
        return render(request, "login.html", {'msg': msg})
    else:  # 提交登录请求post
        username = request.POST.get('uname', '')
        password = request.POST.get('pwd', '')
        user = auth.authenticate(name_email=username, password=password)
        if user is not None:
            auth.login(request, user)
            #return redirect(reverse('home'),arg=[])
            return HttpResponseRedirect("/user/center/")
        else:
            err = "登录名或密码错误！"
            return HttpResponseRedirect("/login/?msg=err")


def alogin_out(request):
    auth.logout(request)
    return HttpResponseRedirect("/home/")


def register(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            nu = Myuser(nickName=form.cleaned_data['nickName'], userEmail=form.cleaned_data['userEmail'],
                        passPwd=form.cleaned_data['passPwd'])
            nu.set_hashedpwd()
            try:
                nu.save()
            except Exception as ex:
                return render(request, "register.html", {'form': form, 'cw': u"注册失败!"})
            else:
                return render(request, "register.html", {'form': form, 'cg': u"注册成功！!"})
        else:
            return render(request, "register.html", {'form': form})
    else:
        form = RegForm()
    return render(request, "register.html", {'form': form})

def searchyp ( request) :
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
def creatorder(request):
    success = "success"
    trainnum = request.POST.get("trainnum")
    start  = request.POST.get("start")
    end = request.POST.get("end")
    date = request.POST.get("date")
    cursor = connection.cursor()
    sql = u"SELECT  id FROM trainticketonline_trainseat" \
          u" WHERE  trainticketonline_trainseat.trainnum='"+trainnum+"' " \
          u" AND trainticketonline_trainseat.seatstatus1 = '1'"\
          u" AND trainticketonline_trainseat.date = '"+date+"'" \
          u" LIMIT 1  "
    cursor.execute(sql)
    train = cursor.fetchone()
    if not train:
        return HttpResponse(json.dumps({"left": 'false'}))
    trainid = train[0][0]
    sql3 = u"SET @@session.tx_isolation='SERIALIZABLE';" + u"UPDATE trainticketonline_trainseat " \
          u" SET  " \
          u" seatstatus1 = '0'," \
          u" from1station = (" \
          u" SELECT stationnum" \
          u" FROM trainticketonline_station" \
          u" WHERE trainticketonline_station.stationname = '"+start+"'),"\
          u" to1station = (SELECT stationnum" \
          u" FROM trainticketonline_station" \
          u" WHERE trainticketonline_station.stationname = '"+end+"')" \
          u" WHERE id = '"+trainid+"'"
    try:
        cursor.execute(sql3)
    except Exception as ex:
        return HttpResponse(json.dumps({"failed":'true'}))
    sql2 = u" SELECT carnum,seatnum " \
          u"  FROM trainticketonline_trainseat " \
          u" WHERE id = '"+trainid+"'"
    cursor.execute(sql2)
    carseat = cursor.fetchall()
    return HttpResponse(json.dumps({"carseat":carseat}))