"""tian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    #列表页
    url(r'^list/(?P<tid>[0-9]+)$',views.list,name='list'),
    #详情页
    url(r'^info/(?P<gid>[0-9]+)$',views.info,name='info'),
    #注册页
    url(r'^register/$',views.register,name='register'),
    #登录
    url(r'^login/$',views.login,name='login'),
    #退出登录
    url(r'^loginout/$',views.loginout,name='loginout'),


    #购物车

    #加入购物车
    url(r'^cart/add/$',views.cartadd,name='cartadd'),

    #购物车页面
    url(r'^cart/list/$',views.cartlist,name='list'),

    #清空购物车
    url(r'^cart/clear/$',views.cartclear,name='cartclear'),

    # 删除购物车商品
    url(r'^cart/del/$',views.cartdel,name='cartdel'),


    # 修改购物车数量
    url(r'^cart/edit/$',views.cartedit,name='cartedit'),

    #查询商品总数量ajax
    url(r'^cart/num$',views.cartnum,name='cartnum'),

    #下单
    #订单确定
    url(r'^order/confirm/$',views.orderconfirm,name='orderconfirm'),

    #生产订单
    url(r'^order/create/$',views.ordercreate,name='ordercreate'),

    #付款
    url(r'^order/buy/$',views.orderbuy,name='orderbuy'),


    #我的订单
    url(r'^myorder/$',views.myorder,name='myorder'),


    #前台个人中心信息
    url(r'^user/info/$',views.userinfo,name='userinfo'),

    #前台个人中心地址信息
    url(r'^user/addressinfo/$',views.useraddressinfo,name='useraddressinfo'),

    #前台个人中心地址信息ajax
    url(r'^user/addressajax/$',views.addressajax,name='addressajax'),


    url(r'^user/addressdel$',views.addressdel,name='addressdel'),







    













]
