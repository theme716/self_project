from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from myadmin.models import Users,Types,Goods,Address,Order,OrderInfo
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


#获取导航分类
def gettype():

    #获取所有二级分类
    data = Types.objects.exclude(pid=0)
    return data

def tian():
    tian = Types.objects.exclude(pid = 0)
    for x in tian:
        x.sub = Goods.objects.filter(typeid = x.id)
    return tian


def index(request):

    #获取所有顶级分类
    data = Types.objects.filter(pid = 0)

    for x in data :
        x.sub = Types.objects.filter(pid=x.id)
        for v in x.sub:
            v.sub = Goods.objects.filter(typeid = v.id)


    tian = Types.objects.exclude(pid = 0)
    for x in tian:
        x.sub = Goods.objects.filter(typeid = x.id)




    context = {'typelist':gettype(),'navlist':data,'tian':tian}
    return render(request,'home/index.html',context)



def list(request,tid):

    #根据id获取当前分类的信息
    tob = Types.objects.get(id = tid)
    if tob.pid == 0:

        #顶级分类
        data = tob

        #获取二级分类
        data.sub = Types.objects.filter(pid = tob.id)

        #获取二级分类的id 并加入到ibs列表
        ibs = []
        for x in data.sub:
            ibs.append(x.id)
        print(ibs)

        data.goods = Goods.objects.filter(typeid__in=ibs)
    # {'name':'服装','sub':[{'name':'男装'},{'name':'女装'}],'goods':[{},{},{},{}]}


    else:

        #先获父级对象(二级分类的pid等于顶级分类的id)
        data = Types.objects.get(id=tob.pid)

        #获取当前子类的商品信息 (二级分类的id和商品的typeid一样)
        data.goods = Goods.objects.filter(typeid=tob.id)

        #获取所有同级信息,包括当前类
        data.sub = Types.objects.filter(pid = tob.pid)

        #给data数据追加一个obj对象
        data.obj = tob










    context = {'typelist':gettype(),'data':data,'tian':tian()}
    return render(request,'home/list.html',context)
    

def info(request,gid):
    ginfo = Goods.objects.get(id = gid)
    context = {'typelist':gettype(),'ginfo':ginfo,'tian':tian()}

    return render(request,'home/info.html',context)


def cartadd(request):
    try:

        #接收商品id
        gid = request.GET['gid']

        #加入购物车的数量
        num = int(request.GET['num'])

        #获取购物车的数据
        data = request.session.get('cart',{})

        #判断商品是否存在购物车中
        if gid in data:
            #如果已经存在,找到商品,修改数量
            data[gid]['num']+=num
        else:
            #获取商品信息
            goods = Goods.objects.get(id = gid)

            #把新的商品信息,追加到data数据中
            data[gid] = {'id':goods.id,'title':goods.title,'price':str(goods.price),'pic':goods.pic,'num':num}


        #加入到session
        request.session['cart']=data

        return JsonResponse({'code':0,'msg':'加入购物车成功'})
    except:
        return JsonResponse({'code':1,'msg':'加入购物车失败'})


#购物车删除
def cartdel(request):
    gid = request.GET['gid']

    data = request.session.get('cart',{})

    del data[gid]

    print(data)

    request.session['cart'] = data

    return JsonResponse({'code':0,'msg':'移除成功'})


def cartedit(request):
    gid = request.GET['gid']

        #加入购物车的数量
    num = int(request.GET['num'])

    data = request.session.get('cart',{})

    data[gid]['num'] = num

    print(data)

    request.session['cart'] = data
    
    return JsonResponse({'code':0,'msg':'修改成功'})



def cartlist(request):
    context = {'typelist':gettype(),'tian':tian()}
    return render(request,'home/cartlist.html',context)

def cartclear(request):
    request.session['cart']={}
    return HttpResponse('<script>location.href="/"</script>')



def cartnum(request):
    data = request.session['cart']
    print(data)
    num = 0
    for x in data:
        num += int(data[x]['num'])
    print(num)

    return JsonResponse({'num':num})

#订单

#订单确定
def orderconfirm(request):

    if request.method == 'GET':

        #获取用户选择的商品
        ids = request.GET['ids'].split(',')
        print(ids)

        #从session中读取购物车信息
        cartdata = request.session['cart']

        orderdata = {}

        #遍历session字典中的键(id),如果id在ids表中,则orderdata[id] = cartdata[id]
        for x in cartdata:
            if x in ids:
                orderdata[x] = cartdata[x]

        #把用户选择购买的商品存入session
        request.session['order'] = orderdata

        #需要让用户确认收货地址 获取当前用户的所有地址信息
        address = Address.objects.filter(uid = request.session['VipUser']['uid'])

        context = {'typelist':gettype(),'address':address,'tian':tian()}
        return render(request,'home/orderconfirm.html',context)


    elif request.method == 'POST':


        #执行地址的添加
        ob = Address()
        ob.uid = Users.objects.get(id = request.session['VipUser']['uid'])
        ob.aname = request.POST['aname']
        ob.aphone = request.POST['aphone']
        ob.aads = request.POST['aads']

        #状态修改 将新的默认地址以为的地址状态改为0
        s = request.POST.get('status',0)

        if s == '1':
            #把其他地址状态改为0
            obs = Address.objects.filter(status=1)

            for x in obs:
                x.status = 0
                x.save()
        ob.status = s
        ob.save()
        return HttpResponse('<script>alert("地址添加成功");location.href="/order/confirm/?ids='+request.GET['ids']+'"</script>')



#订单生产
def ordercreate(request):

    #在session获取订单数据
    data = request.session['order']
    print(data)
    totalprice = 0
    totalnum = 0

    for x in data:
        n = float(data[x]['price'])*data[x]['num']
        totalprice += n
        totalnum += data[x]['num']


    #创建订单
    order = Order()
    order.uid = Users.objects.get(id = request.session['VipUser']['uid'])
    order.address = Address.objects.get(id = request.POST['addressid'])
    order.totalprice = totalprice
    order.totalnum = totalnum
    order.status = 1
    order.save()

    #读取购物车数据
    cart = request.session['cart']

    #创建订单详情
    for x in data:
        orderinfo = OrderInfo()

        #订单号
        orderinfo.orderid = order

        #获取当前购买的商品对象
        goods = Goods.objects.get(id=x)

        orderinfo.gid = goods
        orderinfo.num = data[x]['num']
        orderinfo.price = data[x]['price']
        orderinfo.save()

        #创建完订单后 删除购物车session的数据
        del cart[x]

        #修改商品的购买数量 和库存
        goods.num += data[x]['num']
        goods.storage -= data[x]['num']
        goods.save()



    #清空session中的订单数据
    request.session['order'] = {}

    #更新购物车
    request.session['cart'] = cart

    #跳转到付款页面 后面跟上order 的id号
    return HttpResponse('<script>alert("订单创建成功");location.href="/order/buy/?orderid='+str(order.id)+'"</script>')





#付款
def orderbuy(request):
    orderid = request.GET.get('orderid',None)

    if orderid:
        #通过订单ID获取订单信息,并传到页面当中
        order = Order.objects.get(id=orderid)
        context = {'order':order,'tian':tian()}
        return render(request,'home/buy.html',context)

#我的订单
def myorder(request):
    #获取当前登录用户的所有订单信息

    orders = Order.objects.filter(uid = request.session['VipUser']['uid'])

    context = {'orders':orders,'tian':tian()}

    return render(request,'home/myorder.html',context)





def register(request):
    #判断当前请求方式
    if request.method =='GET':
        return render(request,'home/register.html')

    elif request.method == 'POST':

        #执行注册
        # 判断用户名是否存在
        res = Users.objects.filter(username = request.POST['username']).exists()
        if res:
            return HttpResponse('<script>alert("用户名已存在");location.href="/register"</script>')
        else:

            ob = Users()
            ob.username = request.POST['username']
            ob.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')

            #把用户信息存储到session
            request.session['VipUser'] = {'name':ob.username,'pic':ob.picurl,'uid':ob.id}
            return HttpResponse('<script>alert("注册成功,欢迎登录");location.href="/"</script>')


#登录           
def login(request):
    if request.method == 'GET':
        return render(request,'home/login.html')

    elif request.method == 'POST':
        #查询用户名
        #判断验证码是否正确

        if request.POST['code'].lower() != request.session['verifycode'].lower():
            return HttpResponse('<script>alert("验证码错误");location.href="/login/"</script>')

        #判断用户名,密码
        ob = Users.objects.filter(username = request.POST['username'])
        if ob:
            ob = ob[0]
            if check_password(request.POST['password'],ob.password):
                #密码正确
                #进行登录
                request.session['VipUser'] = {'name':ob.username,'pic':ob.picurl,'uid':ob.id}
                return HttpResponse('<script>alert("登录成功");location.href="/"</script>')

        return HttpResponse('<script>alert("用户名或密码错误");location.href="/login/"</script>')



def loginout(request):
    del request.session['VipUser']

    return HttpResponse('<script>location.href="/"</script>')


def userinfo(request):
    ob = Users.objects.get(id=request.session['VipUser']['uid'])
    print(ob)
    context={'ulist':ob}
    if request.method == 'GET':

        return render(request,'home/userinfo.html',context)

    elif request.method == 'POST':
        ob = Users.objects.get(id=request.POST['uid'])
        ob.username = request.POST['username']
        ob.email = request.POST['email']
        ob.phone = request.POST['phone']
        ob.age = request.POST['age']
        ob.sex = request.POST['sex']
        
        if request.FILES.get('pic'):
            if ob.picurl != '/static/pics/default/default.jpg':
                import os

                os.remove('.'+ob.picurl)
            ob.picurl = uploads(request)
        ob.save()
        
        

    return HttpResponse('<script>alert("修改成功");location.href="/user/info/"</script>')


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



def useraddressinfo(request):
    if request.method == 'GET':
        ob = Address.objects.filter(uid = request.session['VipUser']['uid'])
        print(ob)
        context={'address':ob}

        return render(request,'home/useraddressinfo.html',context)


    elif request.method == 'POST':
        ob = Address()
        ob.uid = Users.objects.get(id = request.session['VipUser']['uid'])
        ob.aname = request.POST['aname']
        ob.aphone = request.POST['aphone']
        ob.aads = request.POST['aads']

        #状态修改 将新的默认地址以为的地址状态改为0
        s = request.POST.get('status',0)

        if s == '1':
            #把其他地址状态改为0
            obs = Address.objects.filter(status=1)

            for x in obs:
                x.status = 0
                x.save()
        ob.status = s
        ob.save()
        

        return HttpResponse('<script>alert("地址添加成功");location.href="/user/addressinfo/"</script>')



def addressajax(request):
    ob = Address.objects.exclude(id = request.GET['aid'])

    for x in ob:
        if x.status == 1:
            x.status = 0
            x.save()

    ab = Address.objects.get(id = request.GET['aid'])
    ab.status = 1
    ab.save()

    return JsonResponse({'code':0,'msg':'设为默认地址'})




def addressdel(request):
    ob = Address.objects.get(id=request.GET['aid'])
    ob.delete()

    return JsonResponse({'msg':'删除成功'})
















