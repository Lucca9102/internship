from django.http import HttpResponse
from django.shortcuts import render
from .models import Products


def index(request):
    # 获取所有产品
    products = Products.objects.all()
    # 字典用于传参
    return render(request, 'index.html',
                  {'products': products})


def new(request):
    return HttpResponse('<h1>New Products</h1>')


def test(request):
    return HttpResponse('test')