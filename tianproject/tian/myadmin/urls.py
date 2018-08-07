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
#从当前路径下的view文件里面调用views和typeviews的py脚本
from . view import views,typeviews,goodsviews


urlpatterns = [

    #ajax上传文件
    url(r'^ajax/upload/$',goodsviews.admin_ajaxupload,name='admin_ajaxupload'),
    #后台登录
    url(r'^login/$',views.login,name='admin_login'),

    #退出登录
    url(r'^loginout/$',views.loginout,name='admin_loginout'),

    #验证码
    url(r'^getvcode/$',views.getvcode,name='getvcode'),



    #后台管理主页
    url(r'^$',views.adminindix,name='admindex'),

    #后台会员添加页面
    url(r'^user/add/$',views.admin_useradd,name='admin_useradd'),

    #后台会员添加操作
    url(r'^user/insert/$',views.admin_insert,name='admin_userinsert'),
    
    #后台会员列表
    url(r'^user/list/$',views.admin_list,name='admin_userlist'),
    
    #后台会员状态
    url(r'^user/status/$',views.admin_status,name='admin_userstatus'),
    
    #后台会员删除
    url(r'^user/del/(?P<id>[0-9]+)$',views.admin_del,name='admin_userdel'),
    
    #后台会员编辑
    url(r'^user/edit/(?P<id>[0-9]+)$',views.admin_edit,name='admin_useredit'),
    
    #后台会员修改后更新
    url(r'^user/update/$',views.admin_update,name='admin_userupdate'),



    #后台商品分类管理
    url(r'^type/add/$',typeviews.admin_type_add,name='admin_typeadd'),

    url(r'^type/insert/$',typeviews.admin_type_insert,name='admin_typeinsert'),

    url(r'^type/list/$',typeviews.admin_type_list,name='admin_typelist'),

    url(r'^type/edit/(?P<tid>[0-9]+)$',typeviews.admin_type_edit,name='admin_typeedit'),

    url(r'^type/update/$',typeviews.admin_type_update,name='admin_typeupdate'),

    url(r'^type/del/$',typeviews.admin_type_del,name='admin_typedel'),


    #商品信息管理

    url(r'^goods/add/$',goodsviews.admin_goods_add,name='admin_goodsadd'),

    url(r'^goods/insert/$',goodsviews.admin_goods_insert,name='admin_goodsinsert'),

    url(r'^goods/list/$',goodsviews.admin_goods_list,name='admin_goodslist'),

    url(r'^goods/status/$',goodsviews.admin_goods_status,name='admin_goodsstatus'),

    url(r'^goods/delete/$',goodsviews.admin_goods_delete,name='admin_goodsdelete'),

    url(r'^goods/edit/(?P<gid>[0-9]+)$',goodsviews.admin_goods_edit,name='admin_goodsedit'),

    url(r'^goods/update/$',goodsviews.admin_goods_update,name='admin_goodsupdate'),



    #订单管理
    url(r'^order/list/$',views.admin_order_list,name='admin_orderlist'),

    url(r'^order/status/$',views.admin_order_status,name='orderstatus'),

    url(r'^order/orderinfo/(?P<oid>[0-9]+)$',views.admin_order_info,name='admin_orderinfo'),

    #个人中心











]
