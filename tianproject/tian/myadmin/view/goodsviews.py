from .. models import Types,Goods
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from . typeviews import Typeorder




def admin_ajaxupload(request):

    import time,random

    myfile = request.FILES.get('pic',None)
    print(myfile)
    # 判断是否有文件上传
    if not myfile:
        return JsonResponse({'code':1,'msg':'没有文件上传'})

    # 执行文件上传
    # 自定义文件名 时间戳+随机数+.jpg
    filename = str(time.time())+str(random.randrange(10000,99999))

    # 获取当前上传文件的后缀名
    hzm = myfile.name.split('.').pop()
    # 允许上传的文件类型
    arr = ['png','jpg','gif','jpeg','bmp','icon']
    # 如果上传的文件类型不正确
    if hzm not in arr:
        return JsonResponse({'code':2,'msg':'上传的文件类型错误'})

    # 打开文件
    file = open('./static/pics/redius/'+filename+'.'+hzm,'wb+')
    # 分块写入文件  
    for chunk in myfile.chunks():      
           file.write(chunk)  
    # 关闭文件
    file.close()

    # 返回文件的url路径
    return JsonResponse({'code':0,'msg':'上传成功','url':'/static/pics/redius/'+filename+'.'+hzm})




def admin_goods_add(request):
    
    context = {'tlist':Typeorder()}
    return render(request,'admin/goods/add.html',context)

def admin_goods_insert(request):

    # from . views import uploads

    if not request.FILES.get('pic',None):
        return HttpResponse('<script>alert("请选择上传商品的图片");location.href="/admin/goods/add/"</script>')

    try:
        ob = Goods()
        ob.typeid = Types.objects.get(id = request.POST['typeid'])
        ob.title = request.POST.get('title')
        ob.price = request.POST['price']
        ob.storage = request.POST['storage']
        ob.info = request.POST['info']
        ob.pic = uploads(request)
        ob.save()

        import os
        path = '/home/yc/tianproject/tianproject/tian'+request.POST['picurl']
        os.remove(path)

        return HttpResponse('<script>alert("添加成功");location.href="/admin/goods/list/"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="/admin/goods/add/"</script>')




def admin_goods_list(request):
    # 搜索条件
    types = request.GET.get('type',None)

    #搜索参数
    keywords = request.GET.get('keywords','')

    statuslist = {'新品':1,'热销':2}
    if types:
        if types == 'all':
            from django.db.models import Q
            data = Goods.objects.filter(Q(title__contains=keywords)|Q(price__contains=keywords)|Q(storage__contains=keywords)|Q(num__contains=keywords)|Q(clicknum__contains=keywords)|Q(addtime__contains=keywords)|Q(status__contains=statuslist.get(keywords,'aa'))).exclude(status=3)
        elif types == 'title':
            data = Goods.objects.filter(title__contains=keywords).exclude(status=3)

        elif types == 'price':
            data = Goods.objects.filter(price__contains=keywords).exclude(status=3)

        elif types == 'storage':
            data = Goods.objects.filter(storage__contains=keywords).exclude(status=3)

        elif types == 'num':
            data = Goods.objects.filter(num__contains=keywords).exclude(status=3)

        elif types == 'clicknum':
            data = Goods.objects.filter(clicknum__contains=keywords).exclude(status=3)

        elif types == 'addtime':
            data = Goods.objects.filter(addtime__contains=keywords).exclude(status=3)

        elif types == 'status':
            data = Goods.objects.filter(status__contains=statuslist.get(keywords,'aaa')).exclude(status=3)
        elif types =='typeid':
            if keywords:
                obj = Types.objects.filter(name__contains=keywords)
                for x in obj:
                    print(x.id)
                    data = Goods.objects.filter(typeid=x.id).exclude(status=3)
            else:
                data= Goods.objects.exclude(status=3)

    else:
        data = Goods.objects.exclude(status=3)


 #分页
    from django.core.paginator import Paginator
    #实例化分页类 参数1 查询的数据, 参数2 每页要显示的数据个数
    paginator = Paginator(data,5)

    #当前页码
    p = int(request.GET.get('p',1))
    print(p)

    #根据当前页码获取当前页 应该显示的数据
    goodslist = paginator.page(p)




    context = {'glist':goodslist}
    return render(request,'admin/goods/list.html',context)


def admin_goods_status(request):
    
    ob = Goods.objects.get(id = request.GET['gid'])
    ob.status = int(request.GET['status'])
    ob.save()
    return HttpResponse('')


def admin_goods_delete(request):
    ob = Goods.objects.get(id=request.GET['gid'])
    ob.status = 3
    ob.save()

    return HttpResponse('ok')


def admin_goods_edit(request,gid):



    ob = Goods.objects.get(id = gid)

    print(ob.info)
    print(ob.typeid.name)

    typename = ob.typeid.name

    tob = Types.objects.filter(name = typename)
    print(tob)
    from django.utils.html import format_html
    ob.info = format_html(ob.info)

    # print(ob)
    context = {'glist':ob,'tlist':tob}
    return render(request,'admin/goods/edit.html',context)


def admin_goods_update(request):

    # from . views import uploads
    ob = Goods.objects.get(id=request.POST['id'])
    ob.title = request.POST['title']
    ob.price = request.POST['price']
    ob.storage = request.POST['storage']
    ob.info = request.POST['info']
    if request.POST['picurl']:

        ob.pic = uploads(request)
        import os
        path = '/home/yc/tianproject/tianproject/tian'+request.POST['picurl']
        os.remove(path)
    ob.save()

    return HttpResponse('<script>alert("修改成功");location.href="/admin/goods/list/"</script>')




def uploads(request):

    import time,random

    myfile = request.FILES.get('pic',None)
    print(myfile)
    #判断是否上传文件

    # if not myfile:
    #     return '/static/pics/default/default.jpg'


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
