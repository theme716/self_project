from django.db import models

# Create your models here.
#会员模型
class Users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=11,null=True)
    sex = models.CharField(max_length=1,null=True)
    age = models.IntegerField(null=True)
    picurl = models.CharField(max_length=100,default='/static/pics/default/default.jpg')
    #0正常 1禁用 2管理员 3下架删除
    status = models.IntegerField(default=0)    
    addtime = models.DateTimeField(auto_now_add=True)



#商品分类模型
class Types(models.Model):
    name = models.CharField(max_length=50)
    pid = models.IntegerField()
    path = models.CharField(max_length=50)


class Goods(models.Model):
    #商品所属分类
    typeid = models.ForeignKey(to="Types",to_field="id")
    #商品标题
    title = models.CharField(max_length=255)
    #商品价格
    price = models.DecimalField(max_digits=8, decimal_places=2)
    #商品库存
    storage = models.IntegerField()
    #商品图片
    pic = models.CharField(max_length=50)
    #商品详情
    info = models.TextField()
    #购买数量
    num = models.IntegerField(default=0)
    #点击数量
    clicknum = models.IntegerField(default=0)
    #商品状态 1:新品 2:热销 3:下架
    status = models.IntegerField(default=1)
    #商品添加时间
    addtime = models.DateTimeField(auto_now_add=True)


#会员收货地址

class Address(models.Model):

    #用户id
    uid = models.ForeignKey(to="Users",to_field="id")
    # 收货人
    aname = models.CharField(max_length=20)
    # 收货地址
    aads = models.CharField(max_length=255)
    # 收货电话
    aphone = models.CharField(max_length=11)
    # 是否为默认 1 默认,
    status = models.IntegerField(default=0)

# 订单表
class Order(models.Model):
    uid = models.ForeignKey('Users',to_field="id")
    address = models.ForeignKey('Address',to_field='id')
    totalprice = models.FloatField()
    totalnum = models.IntegerField()
    # 1 未付款 2已付款,待发货,3已发货,待收货,4已完成,5已取消
    status = models.IntegerField()
    addtime = models.DateTimeField(auto_now_add=True)


# 订单详情
class OrderInfo(models.Model):
    orderid = models.ForeignKey('Order',to_field="id")
    gid =  models.ForeignKey('Goods',to_field="id")
    num = models.IntegerField()
    price = models.FloatField()