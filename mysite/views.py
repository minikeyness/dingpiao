from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from mysite.forms import *


def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))
    #render_to_response需要加context_instance=
    #render（）可以自动验证crsf_token问题


def about(request):
    return render_to_response('about.html')


def order(request):
    if request.method == "GET":
        return render(request, "ordersearch.html")
    else:
        return render(request, "ordersearch.html")


def alogin(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get('uname', '')
        password = request.POST.get('pwd', '')
        user = auth.authenticate(name_email=username, password=password)
        if user is not None:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to home page.
            return render(request, "home.html")
        else:
            err = "登录名或密码错误！"
            return render(request, "login.html", {'errors', err})


def alogin_out(request):
    auth.logout(request)
    # Redirect to home page.
    return HttpResponseRedirect("home.html")


def register(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            nu = Myuser(nickName=form.cleaned_data['nickName'], userEmail=form.cleaned_data['userEmail'],
                      passPwd=form.cleaned_data['passPwd'])
            nu.set_hashedpwd()
            nu.save()
            render(request, "login.html", {'form': form})
    else:
        form = RegForm()
    return render(request, "register.html", {'form': form})
