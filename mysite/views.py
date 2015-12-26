from django.shortcuts import render
# from django.http import Http404
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
# from django.contrib.auth.decorators import login_required
from mysite.forms import *
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def home(request):
    return render(request, 'home.html')
    #render_to_response需要加context_instance=
    #render（）可以自动验证crsf_token问题


def about(request):
    return render(request, 'about.html')


def order(request):
        return render(request, "ordersearch.html")


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
            return HttpResponseRedirect("/home/")
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
