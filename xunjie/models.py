from django.db import models

# Create your models here.
class User(models.Model):  #用户信息表
    name=models.CharField(max_length=20,primary_key=True) #账号
    nameid=models.CharField(max_length=20,null=True) #姓名
    password=models.CharField(max_length=20,null=False)
    email=models.CharField(max_length=20,null=True)
    iphone=models.CharField(max_length=20,null=True)
    jiaose=models.CharField(max_length=20,null=True)
    status=models.BooleanField( default=True)
    address=models.CharField(max_length=20,null=True)
    role=models.CharField(max_length=20,null=True)#用户的角色
class quanxian(models.Model):
    code_name=models.CharField(max_length=20,null=False)
    jon_code=models.CharField(max_length=20,null=False)
    job_name=models.CharField(max_length=20,null=False)
    level=models.CharField(max_length=2,null=True)
class SKU(models.Model):  #产品分类
    id=models.CharField(max_length=20,primary_key=True) #编号
    name=models.CharField(max_length=100,null=False) #名称
    type=models.CharField(max_length=40,null=True) #规格
    classification=models.CharField(max_length=40,null=True) #商品分类
    unit=models.CharField(max_length=40,null=True) #规格
    pur_min_num = models.IntegerField(default=0,null=True) #最小起订量
    pur_multiple_num = models.IntegerField(default=0,null=True) #采购倍数
    so_min_num = models.IntegerField(default=0,null=True)  # 销售最小起订量
    so_multiple_num = models.IntegerField(default=0,null=True)  # 销售倍数
    page_num=models.IntegerField(default=0,null=True) #包装数
    update_time=models.CharField(max_length=20,null=True) #更新的时间
    status = models.BooleanField(default=True)  # 门店的状态
class Stock(models.Model): #库存明细表
    id = models.CharField(max_length=20, primary_key=True)  # 编号
    name = models.CharField(max_length=100, null=False)  # 名称
    type = models.CharField(max_length=40, null=True)  # 规格
    classification = models.CharField(max_length=40, null=True)  # 商品分类
    unit = models.CharField(max_length=40, null=True)  # 规格
    page_num = models.IntegerField(default=0)  # 包装数
    stock_num = models.IntegerField(default=0)  # 库存量总数量
    order_num = models.IntegerField(default=0)  # 订单的占用量
    avail_num = models.IntegerField(default=0)  # 可用量
    Reserved_num = models.IntegerField(default=0)  # 分配量
    Picked_num = models.IntegerField(default=0)  # 拣货量
    Frozen_num = models.IntegerField(default=0)  # 冻结量
    Pending_num = models.IntegerField(default=0)  # 上架量
    Incoming_num = models.IntegerField(default=0)  # 收货量
    update_time = models.CharField(max_length=20, null=True)  # 更新的时间
    stocks_tatus = models.CharField(max_length=4, null=True,default='2')  # 状态 ,1:库存满足了;2:库存不满足

class Roles(models.Model):  #角色名称表
    role_name = models.CharField(max_length=40,null=False) #角色名称
    role_explain = models.CharField(max_length=100,null=True)  #角色描述
class Roles_Del(models.Model): #角色详情表
    role_name = models.CharField(max_length=40, null=False)  # 角色名称,以下内容和权限一样了
    code_name = models.CharField(max_length=20, null=False,default='null')
    jon_code = models.CharField(max_length=20, null=False,default='null')
    job_name = models.CharField(max_length=20, null=False,default='null')
    level = models.CharField(max_length=2, null=True)
class Store(models.Model): #门店信息
    code = models.CharField(max_length=40, null=False)  # 门店编码
    name = models.CharField(max_length=40, null=False)  #
    city_code = models.CharField(max_length=40, null=True)  #
    city_name = models.CharField(max_length=40, null=True)  #
    level = models.CharField(max_length=4, null=True) #站点等级
    status=models.BooleanField( default=True)   #状态
class Boci(models.Model):  #订货批次信息表
    boci = models.CharField(max_length=20, null=True, default='')  # 波次,
    status = models.CharField(max_length=10, null=True,default='待下发')  # 下发状态
    note = models.CharField(max_length=100, null=True)  #
    create_time = models.CharField(max_length=40, null=True)  # 后台创建生成的时间
class Purchase_order_tou(models.Model):
    order_code = models.CharField(max_length=20)  # 单号,平台上的单号
    boci = models.CharField(max_length=20,null=True)  #波次,记录每次的波次信息,手工填写
    date = models.CharField(max_length=40, null=True)  #
    create_time = models.CharField(max_length=40, null=True)  #后台创建生成的时间
    store_code = models.CharField(max_length=20, null=False)  #
    store_name = models.CharField(max_length=40, null=True)  #
    note = models.CharField(max_length=100, null=True)  #
    status = models.CharField(max_length=10, null=True,default='待下发')  #
    sure_status = models.CharField(max_length=10, null=True,default='未确认')  #门店确认标识
    biaozhi = models.CharField(max_length=40, null=True)  #每次下发的标识
class Purchase_Del(models.Model):                       #订单单身信息
    order_code = models.CharField(max_length=20)  # 单号,平台上的单号
    item_code = models.CharField(max_length=20)
    item_name = models.CharField(max_length=200,null=True)
    item_gg = models.CharField(max_length=200,default='',null=True)  #规格
    unit = models.CharField(max_length=20,default='',null=True)  #单位
    num = models.IntegerField(default=0)
    sure_num = models.IntegerField(default=0)  #有赢回传确认的数量
    note = models.CharField(max_length=200, null=True,default='')
    boci = models.CharField(max_length=20, null=True,default='')  # 波次,记录每次的波次信息,手工填写
    date = models.CharField(max_length=40, null=True,default='')  #
    store_code = models.CharField(max_length=20, null=True,default='')  #
    store_name = models.CharField(max_length=40, null=True,default='')  #
    status = models.CharField(max_length=10, null=True, default='待下发')  #
    biaozhi = models.CharField(max_length=40, null=True)  # 每次下发的标识
class SO_First_API(models.Model):
    order_code = models.CharField(max_length=20)  # 单号,平台上的单号
    boci = models.CharField(max_length=20, null=True, default='')  # 波次,
    date = models.CharField(max_length=40, null=True)  # 后台创建生成的时间
    status = models.CharField(max_length=10, null=True)  #下发状态
    type = models.CharField(max_length=10, null=True)  # 类型下发/接受
    detial = models.CharField(max_length=1000, null=True)  #详细状态
class Sale_order_tou(models.Model):
    order_code = models.CharField(max_length=20)  # 单号,平台上的单号
    boci = models.CharField(max_length=20,null=True)  #波次,记录每次的波次信息,手工填写
    date = models.CharField(max_length=40, null=True)  #
    create_time = models.CharField(max_length=40, null=True)  #后台创建生成的时间
    store_code = models.CharField(max_length=20, null=False)  #
    store_name = models.CharField(max_length=40, null=True)  #
    note = models.CharField(max_length=100, null=True)  #
    status = models.CharField(max_length=10, null=True,default='待下发')  #
    biaozhi = models.CharField(max_length=40, null=True)  #每次下发的标识
    pur_code = models.CharField(max_length=20,null=True)  # 采购单号
class Sale_Del(models.Model):                       #订单单身信息
    order_code = models.CharField(max_length=20)  # 单号,平台上的单号
    item_code = models.CharField(max_length=20)
    item_name = models.CharField(max_length=200,null=True)
    item_gg = models.CharField(max_length=200,default='',null=True)  #规格
    unit = models.CharField(max_length=20,default='',null=True)  #单位
    num = models.IntegerField(default=0)
    sure_num = models.IntegerField(default=0)  #标识配送确认数量
    note = models.CharField(max_length=200, null=True,default='')
    boci = models.CharField(max_length=20, null=True,default='')  # 波次,记录每次的波次信息,手工填写
    date = models.CharField(max_length=40, null=True,default='')  #
    store_code = models.CharField(max_length=20, null=True,default='')  #
    store_name = models.CharField(max_length=40, null=True,default='')  #
    status = models.CharField(max_length=10, null=True, default='待下发')  #
    biaozhi = models.CharField(max_length=40, null=True)  # 每次下发的标识
    pur_code = models.CharField(max_length=20,null=True)  # 采购单号
class SALE_First_API(models.Model):
    order_code = models.CharField(max_length=20)  # 单号,平台上的单号
    boci = models.CharField(max_length=20, null=True, default='')  # 波次,
    date = models.CharField(max_length=40, null=True)  # 后台创建生成的时间
    status = models.CharField(max_length=10, null=True)  #下发状态
    type = models.CharField(max_length=10, null=True)  # 类型下发/接受
    detial = models.CharField(max_length=1000, null=True)  #详细状态
