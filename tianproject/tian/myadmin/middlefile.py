from django.shortcuts import render
from django.http import HttpResponse
import re

class middledef:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):

        #定义允许的请求路径
        urllist = ['/admin/login/','/admin/getvcode/']

        #判断是否要进入后台
        if re.match('/admin/',request.path) and request.path not in urllist:
            
            #判断是否登录
            if not request.session.get('AdminUser',None):
                #如果没有登录,则跳转带登录页面
                return HttpResponse('<script>alert("请登录");location.href="/admin/login"</script>')



        response = self.get_response(request)
        return response