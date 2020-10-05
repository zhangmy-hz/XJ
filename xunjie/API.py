import hashlib  #调用
import json,requests
import os,time,datetime
import requests   #http请求
import binascii   #进制转换工具
from xunjie.models import SKU,Purchase_order_tou,Purchase_Del,SO_First_API,Stock,Sale_Del,Sale_order_tou,SALE_First_API,Boci
from xunjie.sql import pysql_update
#优赢API测试

api_url='https://yyapi.800best.com/partner/api/process'    #测试地址
partnerID='ahxj'             #客户ID
partnerKey='a32e7560-2863-4fe0-93bd-56588acab240'           #密匙
warehouseCode='001'      #仓库编码
userCode='迅捷' #有赢经手人
departmentCode='001'  #有赢部门编码
headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}     #http头信息
#业务参数
def SKU_API():  #SKU信息查询\
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
    serviceType = 'QUERY_GOODS_INFO'  # 单据类型
    data=''  #查询SKU信息时,data是空的
    bizData =data +partnerKey
    bizData=bizData.encode(encoding='UTF-8')   #转换为UTF8
    sign=hashlib.md5(bizData).hexdigest()  #生成签名,md5算法
    login_data={"serviceType":serviceType,"partnerID":partnerID,"sign":sign,"bizData":data}  #生产传输数据

    response=requests.post(url=api_url,data=login_data,headers=headers)   #传输数据   params 改成data
    print(response.text)
    sku_data = {}
    sku_data=response.json()     #得到SKU信息
    if sku_data:
        sku_data=sku_data.get('data')   #得到SKU信息
        for sku_i in sku_data:
           # print('开始输出',sku_i.get('unitList')[0])
            if SKU.objects.filter(id=sku_i.get('code')): #表示商品已经存在了
                SKU.objects.filter(id=sku_i.get('code')).update(name=sku_i.get('fullName'),type=sku_i.get('specification'),classification=sku_i.get('category'),unit=sku_i.get('unitList')[0].get('name'),
                                   page_num=sku_i.get('unitList')[0].get('countToBase'),update_time=date,pur_min_num=sku_i.get('unitList')[0].get('purchaseMinQuantity'),
                                                                pur_multiple_num=sku_i.get('unitList')[0].get('purchaseStepQuantity'),so_min_num=sku_i.get('unitList')[0].get('saleMinQuantity'),
                                                                so_multiple_num=sku_i.get('unitList')[0].get('saleStepQuantity'),status=sku_i.get('enabled'))
            else:
                sku=SKU(id=sku_i.get('code'),name=sku_i.get('fullName'),type=sku_i.get('specification'),unit=sku_i.get('unitList')[0].get('name'),classification=sku_i.get('category'),
                                   page_num=sku_i.get('unitList')[0].get('countToBase'),update_time=date,pur_min_num=sku_i.get('unitList')[0].get('purchaseMinQuantity'),
                                                                pur_multiple_num=sku_i.get('unitList')[0].get('purchaseStepQuantity'),so_min_num=sku_i.get('unitList')[0].get('saleMinQuantity'),
                                                                so_multiple_num=sku_i.get('unitList')[0].get('saleStepQuantity'),status=sku_i.get('enabled'))
                sku.save()
            ##更新数字是None的字段为0;思考:没有和为0是两个概念
           # SKU.objects.filter(so_min_num__isnull=True).update(so_min_num=0)
           # SKU.objects.filter(so_multiple_num__isnull=True).update(so_multiple_num=0)
    #return (response.text)

#同步库存接口
def STOCK_API():  #SKU信息查询\

    serviceType = 'GET_STOCKS'  # 单据类型
    wareH = ['001'] #仓库列表
    data={}
    #获取SKU信息
    user_json = []
    nr = SKU.objects.all().values('id')
    for user_i in nr:
        user_json.append(user_i.get('id'))

    data['warehouseCodes'] = wareH
    data['ownerCode'] = ""
    data['goodsCodes'] = user_json   #所有的SKU列表
    data=str(data)
    bizData =data +partnerKey
    bizData=bizData.encode(encoding='UTF-8')   #转换为UTF8
    sign=hashlib.md5(bizData).hexdigest()  #生成签名,md5算法
    login_data={"serviceType":serviceType,"partnerID":partnerID,"sign":sign,"bizData":data}  #生产传输数据

    response=requests.post(url=api_url,data=login_data,headers=headers)   #传输数据   params 改成data
    sku_data = {}
    result=response.json()     #得到SKU信息
    if result.get('result') == False:  # 标识先发失败
        return ('error')
    elif result.get('result') == True:  # 标识先发失败
        Stock.objects.all().delete()   #信息全部删除掉
        sku_data = result.get('data')  # 得到SKU信息
        for data_i in sku_data:
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
            if data_i.get('quantity') > 0 or data_i.get('quantityPending')> 0 or data_i.get('quantityIncoming')>0: #数量大于0
                stocks= Stock(id=data_i.get('goodsCode'),stock_num=data_i.get('quantity'),avail_num=data_i.get('quantityAvailable'),Reserved_num=data_i.get('quantityReserved'),
                      Picked_num=data_i.get('quantityPicked'),Frozen_num=data_i.get('quantityFrozen'),Pending_num=data_i.get('quantityPending'),Incoming_num=data_i.get('quantityIncoming'),update_time=date)
                stocks.save()#保存信息
        #批量更新数据库内容
        pysql_update("update xunjie_stock set name = B.name,type=B.type,classification=B.classification,unit=B.unit,page_num=B.page_num  from xunjie_stock A inner join xunjie_sku B on A.id = B.id ")
        return ('OK')
#下发第一次销售订单
def tans_time(tss1):#时间转化为时间戳
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    # 转为时间戳
    timeStamp = time.mktime(timeArray)
    return (int(round(timeStamp * 1000))) #返回内容
def SO_API(boci):  #订单信息传输
    serviceType = 'CREATE_SALES_ORDER'  # 单据类型
    #读取对应的订单信息--第一次采购订单下发
    tou_json=[] #初始化查询结果集
    pur_tous=Purchase_order_tou.objects.filter(boci=boci,status='待下发').values()
    for user_i in pur_tous:
        tou_json.append(user_i)
    #逐个订单开始下发
    for pur_i in tou_json:
        date_new = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
        data = {}  # 初始化数据对象
        detailList=[] #订单明细记录集合
        data['orderDate']=tans_time(pur_i.get('create_time')) #日期
        data['deliveryDate']=tans_time(pur_i.get('create_time')) #送货预约时间
        data['customerCode']=pur_i.get('store_code')   #门店编码
        data['warehouseCode']=warehouseCode   #仓库编码
        data['includeTax']='false'
        data['userCode']=userCode   #经手人
        data['departmentCode']=departmentCode   #部门编码
        data['outerCode']=pur_i.get('order_code')   #单号
        data['remark']=boci  #备注信息
        #开始获得订单单身信息
        pur_shens=Purchase_Del.objects.filter(order_code=pur_i.get('order_code'),boci=boci,status='待下发').values('item_code','unit','num','note')
        shen_json = [] #初始化单身结果装载集
        for shen_i in pur_shens:
            shen_json.append(shen_i)
        for pur_j in shen_json:  #循环单身信息
            dict= {} #记录空集合
            dict['goodsCode'] = pur_j.get('item_code')#商品编码
            dict['goodsUnitName'] = pur_j.get('unit') #单位
            dict['goodsQuantity'] = pur_j.get('num') #数量
            dict['goodsRemark'] = pur_j.get('note') #备注
           # dict['goodsUnitPrice'] = 0    #默认单价,单价去掉
            dict['goodsisGift'] = 'false'
            detailList.append(dict)   #装入集合
        data['detailList'] = detailList  #单身信息装载入集合
        #逐个订单开始传输
        data = str(data)
        bizData =data +partnerKey
        bizData=bizData.encode(encoding='UTF-8')   #转换为UTF8
        sign=hashlib.md5(bizData).hexdigest()  #生成签名,md5算法

        login_data={"serviceType":serviceType,"partnerID":partnerID,"sign":sign,"bizData":data}  #生产传输数据
        #print(login_data)

        response=requests.post(url=api_url,data=login_data,headers=headers)   #传输数据   params 改成data
        result=response.json()  #获得下发反馈结果
        if result.get('result') == False:  #标识先发失败
            notes = SO_First_API(order_code=pur_i.get('order_code'),boci=boci,date=date_new,status='失败',detial=result.get('errorDescription'),type='下发')#存放日志里面
            notes.save() #保存
        elif result.get('result') == True:  #标识先发失败
            notes = SO_First_API(order_code=pur_i.get('order_code'), boci=boci, date=date_new, status='成功',
                                 detial=result.get('errorDescription'),type='下发')  # 存放日志里面
            notes.save()  # 保存
            #更新订单状态
            Purchase_order_tou.objects.filter(boci=boci,order_code=pur_i.get('order_code')).update(status='已下发')
            Purchase_Del.objects.filter(boci=boci,order_code=pur_i.get('order_code')).update(status='已下发')
            Boci.objects.filter(boci=boci).update(status='已下发')

    return ('OK')#标识全部下发完成

def SO_API_One(order_code):  #订单信息传输--单个订单
    serviceType = 'CREATE_SALES_ORDER'  # 单据类型
    #读取对应的订单信息--第一次采购订单下发
    tou_json=[] #初始化查询结果集
    pur_tous=Purchase_order_tou.objects.filter(order_code=order_code,status='待下发').values()
    for user_i in pur_tous:
        tou_json.append(user_i)
    #逐个订单开始下发
    for pur_i in tou_json:
        date_new = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
        data = {}  # 初始化数据对象
        detailList=[] #订单明细记录集合
        data['orderDate']=tans_time(pur_i.get('create_time')) #日期
        data['deliveryDate']=tans_time(pur_i.get('create_time')) #送货预约时间
        data['customerCode']=pur_i.get('store_code')   #门店编码
        data['warehouseCode']=warehouseCode   #仓库编码
        data['includeTax']='false'
        data['userCode']=userCode   #经手人
        data['departmentCode']=departmentCode   #部门编码
        data['outerCode']=order_code  #单号
        data['remark']=pur_i.get('boci')   #备注信息
        #开始获得订单单身信息
        pur_shens=Purchase_Del.objects.filter(order_code=pur_i.get('order_code'),status='待下发').values('item_code','unit','num','note')
        shen_json = [] #初始化单身结果装载集
        for shen_i in pur_shens:
            shen_json.append(shen_i)
        for pur_j in shen_json:  #循环单身信息
            dict= {} #记录空集合
            dict['goodsCode'] = pur_j.get('item_code')#商品编码
            dict['goodsUnitName'] = pur_j.get('unit') #单位
            dict['goodsQuantity'] = pur_j.get('num') #数量
            dict['goodsRemark'] = pur_j.get('note') #备注
            #dict['goodsUnitPrice'] = 0.001    #默认单价
            dict['goodsisGift'] = 'false'
            detailList.append(dict)   #装入集合
        data['detailList'] = detailList  #单身信息装载入集合
        #逐个订单开始传输
        data = str(data)
        bizData =data +partnerKey
        bizData=bizData.encode(encoding='UTF-8')   #转换为UTF8
        sign=hashlib.md5(bizData).hexdigest()  #生成签名,md5算法

        login_data={"serviceType":serviceType,"partnerID":partnerID,"sign":sign,"bizData":data}  #生产传输数据
        #print(login_data)

        response=requests.post(url=api_url,data=login_data,headers=headers)   #传输数据   params 改成data
        result=response.json()  #获得下发反馈结果
        if result.get('result') == False:  #标识先发失败
            notes = SO_First_API(order_code=pur_i.get('order_code'),boci=pur_i.get('boci'),date=date_new,status='失败',detial=result.get('errorDescription'),type='下发')#存放日志里面

            notes.save() #保存
        elif result.get('result') == True:  #标识先发失败
            notes = SO_First_API(order_code=pur_i.get('order_code'), boci=pur_i.get('boci'), date=date_new, status='成功',
                                 detial=result.get('errorDescription'),type='下发')  # 存放日志里面
            notes.save()  # 保存
            #更新订单状态
            Purchase_order_tou.objects.filter(order_code=order_code).update(status='已下发')
            Purchase_Del.objects.filter(order_code=order_code).update(status='已下发')

    return ('OK')#标识全部下发完成

def SALE_API(boci):  #订单信息传输
    serviceType = 'CREATE_SALES_ORDER'  # 单据类型
    #读取对应的订单信息--第一次采购订单下发
    tou_json=[] #初始化查询结果集
    pur_tous=Sale_order_tou.objects.filter(boci=boci,status='待下发').values()
    for user_i in pur_tous:
        tou_json.append(user_i)
    #逐个订单开始下发
    for pur_i in tou_json:
        date_new = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
        data = {}  # 初始化数据对象
        detailList=[] #订单明细记录集合
        data['orderDate']=tans_time(date_new) #日期
        data['deliveryDate']=tans_time(date_new) #送货预约时间
        data['customerCode']=pur_i.get('store_code')   #门店编码
        data['warehouseCode']=warehouseCode   #仓库编码
        data['includeTax']='false'
        data['userCode']=userCode   #经手人
        data['departmentCode']=departmentCode   #部门编码
        data['outerCode']=pur_i.get('order_code')   #单号
        data['remark']=boci  #备注信息
        #开始获得订单单身信息
        pur_shens=Sale_Del.objects.filter(order_code=pur_i.get('order_code'),boci=boci,status='待下发').values('item_code','unit','sure_num','note')
        shen_json = [] #初始化单身结果装载集
        for shen_i in pur_shens:
            shen_json.append(shen_i)
        for pur_j in shen_json:  #循环单身信息
            dict = {}  # 记录空集合
            print(pur_j)
            if pur_j.get('sure_num') > 0:  #数量大于0才下发
                dict['goodsCode'] = pur_j.get('item_code')#商品编码
                dict['goodsUnitName'] = pur_j.get('unit') #单位
                dict['goodsQuantity'] = pur_j.get('sure_num') #数量
                dict['goodsRemark'] = pur_j.get('note') #备注
                #dict['goodsUnitPrice'] = 0.001    #默认单价
                dict['goodsisGift'] = 'false'
                detailList.append(dict)   #装入集合
        data['detailList'] = detailList  #单身信息装载入集合
        #逐个订单开始传输
        data = str(data)
        bizData =data +partnerKey
        bizData=bizData.encode(encoding='UTF-8')   #转换为UTF8
        sign=hashlib.md5(bizData).hexdigest()  #生成签名,md5算法

        login_data={"serviceType":serviceType,"partnerID":partnerID,"sign":sign,"bizData":data}  #生产传输数据
        #print(login_data)

        response=requests.post(url=api_url,data=login_data,headers=headers)   #传输数据   params 改成data
        result=response.json()  #获得下发反馈结果
        if result.get('result') == False:  #标识先发失败
            notes = SALE_First_API(order_code=pur_i.get('order_code'),boci=boci,date=date_new,status='失败',detial=result.get('errorDescription'),type='下发')#存放日志里面
            notes.save() #保存
        elif result.get('result') == True:  #标识先发失败
            notes = SALE_First_API(order_code=pur_i.get('order_code'), boci=boci, date=date_new, status='成功',
                                 detial=result.get('errorDescription'),type='下发')  # 存放日志里面
            notes.save()  # 保存
            #更新订单状态
            Sale_order_tou.objects.filter(boci=boci,order_code=pur_i.get('order_code')).update(status='已下发')
            Sale_Del.objects.filter(boci=boci,order_code=pur_i.get('order_code')).update(status='已下发')

    return ('OK')#标识全部下发完成
def SALE_API_One(order_code):  #订单信息传输--单个订单
    serviceType = 'CREATE_SALES_ORDER'  # 单据类型
    #读取对应的订单信息--第一次采购订单下发
    tou_json=[] #初始化查询结果集
    pur_tous=Sale_order_tou.objects.filter(order_code=order_code,status='待下发').values()
    for user_i in pur_tous:
        tou_json.append(user_i)
    #逐个订单开始下发
    for pur_i in tou_json:
        date_new = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
        data = {}  # 初始化数据对象
        detailList=[] #订单明细记录集合
        data['orderDate']=tans_time(date_new) #日期
        data['deliveryDate']=tans_time(date_new) #送货预约时间
        data['customerCode']=pur_i.get('store_code')   #门店编码
        data['warehouseCode']=warehouseCode   #仓库编码
        data['includeTax']='false'
        data['userCode']=userCode   #经手人
        data['departmentCode']=departmentCode   #部门编码
        data['outerCode']=order_code  #单号
        data['remark']=pur_i.get('boci')   #备注信息
        #开始获得订单单身信息
        pur_shens=Sale_Del.objects.filter(order_code=pur_i.get('order_code'),status='待下发').values('item_code','unit','sure_num','note')
        shen_json = [] #初始化单身结果装载集
        for shen_i in pur_shens:
            shen_json.append(shen_i)
        for pur_j in shen_json:  #循环单身信息
            dict= {} #记录空集合
            if pur_j.get('sure_num') > 0:
                dict['goodsCode'] = pur_j.get('item_code')#商品编码
                dict['goodsUnitName'] = pur_j.get('unit') #单位
                dict['goodsQuantity'] = pur_j.get('sure_num') #数量
                dict['goodsRemark'] = pur_j.get('note') #备注
                #dict['goodsUnitPrice'] = 0.001    #默认单价
                dict['goodsisGift'] = 'false'
                detailList.append(dict)   #装入集合
        data['detailList'] = detailList  #单身信息装载入集合
        #逐个订单开始传输
        data = str(data)
        bizData =data +partnerKey
        bizData=bizData.encode(encoding='UTF-8')   #转换为UTF8
        sign=hashlib.md5(bizData).hexdigest()  #生成签名,md5算法

        login_data={"serviceType":serviceType,"partnerID":partnerID,"sign":sign,"bizData":data}  #生产传输数据
        #print(login_data)

        response=requests.post(url=api_url,data=login_data,headers=headers)   #传输数据   params 改成data
        result=response.json()  #获得下发反馈结果
        if result.get('result') == False:  #标识先发失败
            notes = SO_First_API(order_code=pur_i.get('order_code'),boci=pur_i.get('boci'),date=date_new,status='失败',detial=result.get('errorDescription'),type='下发')#存放日志里面

            notes.save() #保存
        elif result.get('result') == True:  #标识先发失败
            notes = SALE_First_API(order_code=pur_i.get('order_code'), boci=pur_i.get('boci'), date=date_new, status='成功',
                                 detial=result.get('errorDescription'),type='下发')  # 存放日志里面
            notes.save()  # 保存
            #更新订单状态
            Sale_order_tou.objects.filter(order_code=order_code).update(status='已下发')
            Sale_Del.objects.filter(order_code=order_code).update(status='已下发')

    return ('OK')#标识全部下发完成