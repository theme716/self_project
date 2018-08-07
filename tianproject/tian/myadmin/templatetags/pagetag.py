from django import template
register = template.Library()

#自定义标签
from django.utils.html import format_html
@register.simple_tag

def showpage(count,request):
    #count 总也是
    #request 当前页面的请求对象

    #begin开始页
    #end 结束页

    #获取所有参数,在每一次页码跳转时,携带已有参数
    kv = ''
    for x in request.GET:
        if x != 'p':
            kv+= '&'+x+'='+request.GET[x]

    count = int(count)

    #在请求获取当前页码数,如果没有 默认1
    p = int(request.GET.get('p',1))

    begin = p - 4
    end = p + 5

    #判断如果当前页码数 小于 5
    if p < 5:
        begin = 1
        end = 10
    #如果当前页码数小鱼5 总页数-5
    if p > count - 5:
        begin = count - 9
        end = count

    #如果总页数小于10

    if count < 10 :
        begin = 1
        end = count

    page = ''
    page += '<li><a href="?p=1'+kv+'">首尔</a></li>'

    if p <=1:
        page +='<li><a href=">p=1'+kv+'">上一页</a></li>'

    for x in range(begin,end+1):

        if x == p:
            page +='<li class="am-active"><a href="?p='+str(x)+kv+'">'+str(x)+'</a></li>'

        else:
            page +='<li><a href="?p='+str(x)+kv+'">'+str(x)+'</a></li>'


    if p>= count:
        page += '<li><a href="?p='+str(count)+kv+'">下一页</a></li>'

    else:
        page += '<li><a href="?p='+str(p+1)+kv+'">下一页</a></li>'

    page += '<li><a href="?p='+str(count)+kv+'">尾页</a></li>'

    return format_html(page)

from django.utils.html import format_html
@register.simple_tag

def sxf(n1,n2):
    data = n1 / n2

    return round(data)


from django.utils.html import format_html
@register.simple_tag
def cheng(n1,n2):
    n1 = int(n1)
    n2 = float(n2)


    return n1*n2
