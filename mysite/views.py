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
    c = {}
    c.update(csrf(request))
    if request.method == "GET":
        return render_to_response("ordersearch.html", c)
    else:
        render_to_response("ordersearch.html", c)


def alogin(request):
    c = {}
    c.update(csrf(request))
    if request.method == "GET":
        return render_to_response("login.html", c)
    else:
        render_to_response("login.html", c)


def register(request):
    c = {}
    c.update(csrf(request))
    if request.method == "GET":
        return render_to_response("register.html",c)
    else:
        render_to_response("register.html", c)
