from django.db import connection, transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def usercontact(requset):
    if requset.user.is_authenticated():
        cursor = connection.cursor()
        sql = u'select * FROM peoples where uId=%s' % (requset.user.id, )
        cursor.execute(sql)
        peoplelist = cursor.fetchall()
        # names = [{row[0]} for row in peoplelist]
        # cursor.execute("call Proc_Set_Isread(%s,%s)",[id,'1']) 存储过程的执行
        return render(requset, "contactpage.html", {"peoples": peoplelist})
    else:
        return render(requset, "login.html")


@login_required
def userinfo(requset):
    if requset.user.is_authenticated():
        return render(requset, "userpage.html")
    else:
        return render(requset, "login.html")

# c = {}
# c.update(csrf(request))