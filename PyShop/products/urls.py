from django.urls import path
# 注意这里不可以写 import views
# 可能会引用到错误的文件
from . import views


urlpatterns = [
    # empty string
    # representing the root of this app
    # /products
    # ↓ not calling index()
    path('', views.index),
    path('new', views.new),
    path('new/test', views.test)
]