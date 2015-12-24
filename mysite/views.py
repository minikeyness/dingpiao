from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf


def home(request):
    return render_to_response('home.html')


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
        return render(request, "login.html")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        return render(request, "register.html")
