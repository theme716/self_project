from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from .. models import Users,Order,OrderInfo
# Create your views here.


def login(request):
    #如果访问当前页面的请求方式为GET,则返回一个登录页面
    if request.method == 'GET':
        return render(request,'admin/login.html')

    elif request.method == 'POST':
        #执行登录
        #判断验证码是否真情
        if request.POST['vcode'].lower() != request.session['verifycode'].lower():
            return HttpResponse('<script>alert("验证码错误");location.href="/admin/login"</script>')

        #判断用户,和密码
        ob = Users.objects.filter(username=request.POST['username'])
        print(ob[0])
        if ob:
            ob = ob[0]


            #判断密码
            if check_password(request.POST['password'],ob.password):

                #判断是否是管理员
                if ob.status == 2:
                    #有权限
                    #进行登录
                    request.session['AdminUser'] = {'name':ob.username,'pic':ob.picurl}

                    return HttpResponse('<script>alert("登录成功");location.href="/admin/"</script>')

                else:
                    return HttpResponse('<script>alert("没有权限登录");location.href="/admin/login"</script>')

            else:
                return HttpResponse('<script>alert("密码错误");location.href="/admin/login"</script>')

        else:
            return HttpResponse('<script>alert("用户名不存在");location.href="/admin/login"</script>')



    # return render(request,'admin/login.html')

def loginout(request):
    del request.session['AdminUser']

    return HttpResponse('<script>alert("退出成功");location.href="/admin/login"</script>')


def getvcode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')



def adminindix(request):
    return render(request,'admin/main.html')


def admin_useradd(request):
    return render(request,'admin/add.html')


def admin_insert(request):
    #
    pic = uploads(request)
    if not pic:
        return HttpResponse('<script>alert("上传文件类型错误");location.href = "/admin/user/add"</script>')

    try:
        ob = Users()
        ob.username = request.POST.get('username')
        print(request.POST.get('username'))
        ob.password = make_password(request.POST['password'],None, 'pbkdf2_sha256')
        ob.email = request.POST.get('email')
        ob.phone = request.POST.get('phone')
        ob.age = request.POST.get('age')
        ob.sex = request.POST.get('sex')
        ob.picurl = pic
        ob.save()

        if request.POST['picurl']:
            import os
            path = '/home/yc/tianproject/tianproject/tian'+request.POST['picurl']
            os.remove(path)

        # return HttpResponse('添加成功')
        return HttpResponse('<script>alert("添加成功");location.href="/admin/user/list/"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="/admin/user/add/"</script>')
        # return HttpResponse('添加失败')


def admin_list(request):
    # 搜索条件
    types = request.GET.get('type',None)

    #搜索参数
    keywords = request.GET.get('keywords','')

    #状态搜索的定义
    statuslist = {'正常':0,'禁用':1}

    #判断是否有搜索条件
    if types:

        if types == 'all':
            from django.db.models import Q
            data = Users.objects.filter(Q(username__contains=keywords)|Q(email__contains=keywords)|Q(phone__contains=keywords)|Q(age__contains=keywords)|Q(sex__contains=keywords)|Q(status__contains=statuslist.get(keywords,'aa')))
        
        elif types == 'username':
            data = Users.objects.filter(username__contains=keywords)

        elif types == 'email':
            data = Users.objects.filter(email__contains=keywords)

        elif types =='phone':
            data = Users.objects.filter(phone__contains=keywords)

        elif types == 'age':
            data = Users.objects.filter(age__contains=keywords)

        elif types == 'sex':
            data = Users.objects.filter(sex__contains=keywords)

        elif types == 'status':
            data = Users.objects.filter(status__contains=statuslist.get(keywords,'aaa'))
            print(data)

    else:
        #没有搜索条件,获取全部
        data = Users.objects.exclude(status=3)

    from django.core.paginator import Paginator

    #当前页码
    paginator = Paginator(data,3)
    print(paginator)

    p = int(request.GET.get('p',1))
    #根据当前页码获取当前页面应该显示的数据
    userlist = paginator.page(p)

    #获取当前页面的页码数(1,177)
    num = paginator.page_range





    #不包含status等于3的数据
   
    
    context = {'ulist':userlist,'pagenum':num}
    return render(request,'admin/list.html',context)


def admin_status(request):
    ob = Users.objects.get(id = request.GET['uid'])
    ob.status = int(request.GET['status'])
    ob.save()
    return HttpResponse('')


def admin_del(request,id):
    ob = Users.objects.get(id=id)
    ob.status = 3
    ob.save()
    return HttpResponse('<script>alert("删除成功");location.href="/admin/user/list/"</script>')


def admin_edit(request,id):
    ob = Users.objects.get(id = id)
    print(ob)
    context = {'data':ob}
    return render(request,'admin/edit.html',context)


def admin_update(request):
    try:
        ob = Users.objects.get(id=request.POST['id'])
        print(ob)
        ob.username = request.POST.get('username')
        ob.email = request.POST.get('email')
        ob.phone = request.POST.get('phone')
        ob.age = request.POST.get('age')
        ob.sex = request.POST.get('sex')

        if request.FILES.get('pic'):
            if ob.picurl != '/static/pics/default/default.jpg':
                import os

                os.remove('.'+ob.picurl)
            ob.picurl = uploads(request)
        ob.save()
        
        if request.POST['picurl']:
            import os
            path = '/home/yc/tianproject/tianproject/tian'+request.POST['picurl']
            os.remove(path)

        return HttpResponse('<script>alert("修改成功");location.href="/admin/user/list/"</script>')
    except:
        return HttpResponse('<script>alert("修改失败");location.href="/admin/user/edit/'+str(ob.id)+'"</script>')



    

def uploads(request):

    import time,random

    myfile = request.FILES.get('pic',None)
    print(myfile)
    #判断是否上传文件

    if not myfile:
        return '/static/pics/default/default.jpg'


    #执行上传文件
    filename = str(time.time())+str(random.randrange(100,999))

    hzm = myfile.name.split('.').pop()

    arr = ['png','jpg','gif','jpeg','bmp','icon']

    if hzm not in arr:
        return False

    file = open('./static/pics/'+filename+'.'+hzm,'wb+')

    #分块写入文件

    for x in myfile.chunks():
        file.write(x)

    file.close()

    return '/static/pics/' + filename +'.' +hzm



#订单列表
def admin_order_list(request):
    ob = Order.objects.all()
    context = {'order':ob}

    return render(request,'admin/orderlist.html',context)


def admin_order_status(request):
    ob = Order.objects.get(id = request.GET['oid'])
    ob.status = int(request.GET['status'])
    ob.save()
    return HttpResponse('')


def admin_order_info(request,oid):
    oid = int(oid)
    ob = Order.objects.get(id=oid)
    
    context = {'info':ob}

    return render(request,'admin/adminorderinfo.html',context)