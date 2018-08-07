from .. models import Types
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse



def admin_type_add(request):
    
    context = {'tlist':Typeorder()}
    return render(request,'type/add.html',context)


def admin_type_insert(request):
    try:
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']

        if ob.pid == '0':
            ob.path = '0,'

        else:
            #如果添加的不是顶级分类 需要获取父类的path路径 ,拼接上pid
            p = Types.objects.get(id=ob.pid)
            ob.path = p.path+str(ob.pid)+','
        ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="/admin/type/list"</script>')

    except:
        return HttpResponse('<script>alert("添加成功");location.href="/admin/type/add"</script>')

def admin_type_list(request):
    # types = request.GET.get('type',None)
    # print(types)

    keywords = request.GET.get('keywords','')
    # print(keywords)

    
    if keywords:
        # from django.db.models import Q
        data = Types.objects.filter(name__contains=keywords)
        print(data)
    else:
        data = Typeorder()

        print(data)


    #分页
    from django.core.paginator import Paginator
    #实例化分页类 参数1 查询的数据, 参数2 每页要显示的数据个数
    paginator = Paginator(data,5)

    #当前页码
    p = int(request.GET.get('p',1))
    print(p)

    #根据当前页码获取当前页 应该显示的数据
    typelist = paginator.page(p)

    #获取当前页的页码数
    # num = paginator.page_range
    # print(num)

    context = {'tlist':typelist}
    return render(request,'type/list.html',context)


def Typeorder():
    #获取所有商品的分类
    #select *,concat(path,id) as paths from myadmin_types order by paths;
    ob = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')

    for x in ob:
        print(x)
        n = int(len(x.path) /2)-1
        x.name = (n*'|---')+x.name

        # 给当前对象 添加一个所属父类的属性
        if x.pid == 0:
            x.pname = '顶级分类'

        else:
            obj = Types.objects.get(id = x.pid)
            x.pname = obj.name

    return ob

def admin_type_edit(request,tid):
    ob = Types.objects.get(id=tid)
    context={'tinfo':ob,'tlist':Typeorder()}

    return render(request,'type/edit.html',context)

def admin_type_update(request):
    try:
        ob = Types.objects.get(id=request.POST['id'])
        print(request.POST['id'])
        ob.name = request.POST['name']
        ob.save()
        return HttpResponse('<script>alert("修改成功");location.href="/admin/type/list/"</script>')
    except:
        return HttpResponse('<script>alert("修改失败");location.href="/admin/type/edit/'+request.POST['id']+'/"</script>')


def admin_type_del(request):
    num = Types.objects.filter(pid = request.GET['tid']).count()

    if num:
        return JsonResponse({'status':1,'msg':'当前类下有其他子类,不能删除'})

    #没有子类
    ob = Types.objects.get(id = request.GET['tid'])
    ob.delete()

    return JsonResponse({'status':0,'msg':'可以删除'})