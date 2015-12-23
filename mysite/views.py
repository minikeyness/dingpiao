from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext


def home(request):
    return render_to_response('home.html')


def about(request):
    return render_to_response('about.html')


def order(request):
    return render_to_response('ordersearch.html')

