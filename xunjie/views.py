from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse,FileResponse  #引入json响应
import json,requests
import os,django,time,xlrd,datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")# project_name 项目名称   #出现报错
django.setup()
from django.middleware.csrf import get_token
from xunjie.models import User,quanxian,SKU,Roles,Roles_Del,Store,Purchase_order_tou,Purchase_Del,SO_First_API,Stock,Sale_Del,Sale_order_tou,SALE_First_API,Boci
from django.core.paginator import Paginator   #导入分页器
from django.db.models import Q
from xjdjango.settings import MEDIA_ROOT  #文件地址
import  hashlib,xlwt
from xunjie.sql import  pysql,pysql_update
from xunjie.API import SKU_API,SO_API,STOCK_API,SO_API_One,SALE_API,SALE_API_One   #调取SKU接口,全部抓取
from  django.utils.encoding import escape_uri_path
# Create your views here.
def login(request):
    post_data=request.body
    post_data=json.loads(post_data)
    login_user=User.objects.filter(name=post_data.get('form_data').get('username'),password=post_data.get('form_data').get('password'))
    if login_user:
    #判断登录号是否存在:
        token=get_token(request)  #得到token
        request.session['token']=token
        return HttpResponse('OK')
    else:
        return HttpResponse('404')
def quanxian_get(request):    #获取权限
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('name')
    quanxian_list = [] #先定义
    if name:
        role=User.objects.filter(name=name).values('role')  #获得角色名称
        quanxian_list = Roles_Del.objects.filter(role_name=role[0].get('role')).values().order_by('jon_code')
    quanxian_json = []
    for quanxian_i in quanxian_list:
        quanxian_json.append(quanxian_i)
    dict = {}
    list = []  # 最终结果集合
    chiid_dict={}  #子菜单
    chiid_list=[]  #子菜单

    for quanxian_j in quanxian_json:
        #print(quanxian_j)
        if quanxian_j.get('level') == '0':  #一级菜单
            dict['id']=quanxian_j.get('jon_code')
            dict['name']=quanxian_j.get('job_name')
            for quanxian_h in quanxian_json:
                if int(quanxian_h.get('jon_code')[0]) == int(quanxian_j.get('jon_code')) and quanxian_h.get('jon_code') != quanxian_j.get('jon_code') and quanxian_h.get('level') == '1':
                    chiid_dict['id']=quanxian_h.get('jon_code')
                    chiid_dict['name']=quanxian_h.get('job_name')
                    chiid_list.append(chiid_dict)   #完成子集合
                    chiid_dict={}  #完成清空
            dict['children']=chiid_list
            chiid_list=[]   #完成清空
            list.append(dict)
            dict={}    #清空结果集合
    return JsonResponse(data=list,safe=False)
def user(request):    #获取用户信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=User.objects.all().values()
    else:
        user_list = User.objects.filter(Q(name__icontains=post_data.get('serch'))|Q(nameid__icontains=post_data.get('serch'))).values()
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def user_status(request):
    post_data = request.body
    post_data = json.loads(post_data)
    try:
        user_updade=User.objects.filter(name=post_data.get('name')).update(status=post_data.get('status_c'))
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def add_user(request):
    post_data=request.body
    post_data=json.loads(post_data).get('form_data')
    #print(post_data)
    try:
        user_add=User(name=post_data.get('username'),nameid=post_data.get('password'),password='88888888',email=post_data.get('email'),iphone=post_data.get('iphone'),address=post_data.get('address'),role=post_data.get('role'))
        user_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def user_up_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('id')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=User.objects.filter(name=name).values()
        for user_i in user_list :
            user_json['name']=user_i.get('name')
            user_json['nameid']=user_i.get('nameid')
            user_json['email']=user_i.get('email')
            user_json['iphone']=user_i.get('iphone')
            user_json['address']=user_i.get('address')
            user_json['role']=user_i.get('role')
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')
def user_update(request):
    post_data = request.body
    post_data = json.loads(post_data).get('data')
    try:
        User.objects.filter(name=post_data.get('name')).update(nameid=post_data.get('nameid'),email=post_data.get('email'),iphone=post_data.get('iphone'),address=post_data.get('address'),role=post_data.get('role'))
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def delete_user(request): #删除用户
    post_data = request.body
    name = json.loads(post_data).get('name')
    try:
        User.objects.filter(name=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def roles(request): #一级菜单
    role=Roles.objects.all().values()
    role_json = []
    for role_i in role:
        role_json.append(role_i)
    return JsonResponse(data=role_json,safe=False)
def quanxian_list_all(request):    #三级菜单
    quanxian_list=quanxian.objects.all().values()
    quanxian_json = []
    for quanxian_i in quanxian_list:
        quanxian_json.append(quanxian_i)
    dict = {}
    list = []  # 最终结果集合
    chiid_dict={}  #子菜单
    chiid_list=[]  #子菜单

    button_dict = {}  # 三级子菜单
    button_list = []  # 三级子菜单

    for quanxian_j in quanxian_json:
        #print(quanxian_j)
        if quanxian_j.get('level') == '0':  #一级菜单
            dict['id']=quanxian_j.get('jon_code')
            dict['name']=quanxian_j.get('job_name')
            for quanxian_h in quanxian_json:
                if int(quanxian_h.get('jon_code')[0]) == int(quanxian_j.get('jon_code')) and quanxian_h.get('jon_code') != quanxian_j.get('jon_code') and quanxian_h.get('level') == '1':
                    chiid_dict['id']=quanxian_h.get('jon_code')
                    chiid_dict['name']=quanxian_h.get('job_name')
                    for quanxian_b in quanxian_json:
                        if quanxian_b.get('code_name') == quanxian_h.get('jon_code') and quanxian_b.get('level') == '2':
                            button_dict['id'] = quanxian_b.get('jon_code')
                            button_dict['name'] = quanxian_b.get('job_name')
                            button_list.append(button_dict)  #集合三级菜单
                            button_dict={}  #清空按钮
                    chiid_dict['children']=button_list
                    button_list=[]  #清空三级节点
                    chiid_list.append(chiid_dict)   #完成子集合
                    chiid_dict={}  #完成清空
            dict['children']=chiid_list
            chiid_list=[]   #完成清空
            list.append(dict)
            dict={}    #清空结果集合
    return JsonResponse(data=list,safe=False)

def role_check(request):
    post_data = request.body
    post_data = json.loads(post_data)
    role_name=post_data.get('role') #得到角色的名称
    role_check_all = Roles_Del.objects.filter(role_name=role_name,level='2').values('jon_code') #获得本角色的所有内容

    role_list=[]
    for role_i in role_check_all:
        role_list.append(role_i.get('jon_code'))
    return JsonResponse(data=role_list, safe=False)
def role_save(request):
    post_data = request.body
    post_data = json.loads(post_data)
    role_name = post_data.get('role')  # 得到角色的名称
    keys = post_data.get('keys')  # 得到具体的角色列表
    #执行第一步将目前该角色的所有权限清空
    Roles_Del.objects.filter(role_name=role_name).delete()
    #执行第二部,清空之后重新新增
    for key_i in keys:
        roles_save=Roles_Del(role_name=role_name,jon_code=key_i)
        roles_save.save()
    #更新额外字段到角色表
    pysql_update("update xunjie_roles_del set code_name=B.code_name,job_name=B.job_name,level=B.level from xunjie_roles_del A inner join xunjie_quanxian B on A.jon_code = B.jon_code where A.role_name = '{}'".
                 format(role_name))
    return HttpResponse('OK')
def role_new(request):
    post_data = request.body
    post_data = json.loads(post_data)
    data = post_data.get('form_data')  # 得到角色的名称
    name=data.get('name')
    name_del=data.get('name_del')
    if Roles.objects.filter(role_name=name):
        return HttpResponse('cuzai')
    else: 
        role=Roles(role_name=name,role_explain=name_del)
        role.save()
        return HttpResponse('OK')
def role_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('role')  #获得前段的用户编号字段
    user_json=[]  #返回信息
    if name:
        user_list=Roles.objects.filter(role_name__icontains=name).values('role_name')
    else:
        user_list = Roles.objects.all().values('role_name')
    for user_i in user_list:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def update_role_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name = post_data.get('name')  # 获得前段的用户编号字段
    roles_get = Roles.objects.filter(role_name=name).values()
    user_json={}
    for user_i in roles_get:
        user_json['name'] = user_i.get('role_name')
        user_json['name_del'] = user_i.get('role_explain')
    return JsonResponse(data=user_json, safe=False)
def role_up_save(request):
    post_data = request.body
    post_data = json.loads(post_data)
    upform = post_data.get('upform')  # 获得前段的用户编号字段
    Roles.objects.filter(role_name=upform.get('name')).update(role_explain=upform.get('name_del'))
    return HttpResponse('OK')
def delete_role(request):
    post_data = request.body
    post_data = json.loads(post_data)
    role_name = post_data.get('role_name')  # 获得前段的用户编号字段
    Roles.objects.filter(role_name=role_name).delete()
    Roles_Del.objects.filter(role_name=role_name).delete()
    return HttpResponse('OK')
def get_role(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name = post_data.get('user_name')  #得到用户账号
    #print(name)
    if name :
        role = User.objects.filter(name=name).values('role')  # 获得角色名称

        role_name = post_data.get('role')  # 得到角色的名称
        role_check_all = Roles_Del.objects.filter(role_name=role[0].get('role'), level='2').values('jon_code')  # 获得本角色的所有内容

        role_list = []
        for role_i in role_check_all:
            role_list.append(role_i.get('jon_code'))
        #print(role_list)
        return JsonResponse(data=role_list, safe=False)
def sku_api(request):
    sku=SKU_API()
    return HttpResponse('OK')
def sku(request):    #获取sku信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=SKU.objects.all().values()
    else:
        user_list = SKU.objects.filter(Q(id__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))).values()
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['sku_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def store(request):    #获取门店信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=Store.objects.all().values()
    else:
        user_list = Store.objects.filter(Q(code__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))).values()
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['store_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def add_store(request):
    post_data=request.body
    post_data=json.loads(post_data).get('form_data')
    if Store.objects.filter(code=post_data.get('code')):  #表示信息已经存在了
        return HttpResponse(401)
    try:
        user_add=Store(code=post_data.get('code'),name=post_data.get('name'),city_name=post_data.get('city_name'),city_code=post_data.get('city_code'),level=post_data.get('level'))
        user_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def store_status(request):
    post_data = request.body
    post_data = json.loads(post_data)
    try:
        user_updade=Store.objects.filter(code=post_data.get('name')).update(status=post_data.get('status_c'))
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def store_up_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    code=post_data.get('code')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=Store.objects.filter(code=code).values()
        for user_i in user_list :
            user_json['code']=user_i.get('code')
            user_json['name']=user_i.get('name')
            user_json['city_code']=user_i.get('city_code')
            user_json['city_name']=user_i.get('city_name')
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')
def stroe_update(request):
    post_data = request.body
    post_data = json.loads(post_data).get('data')
    #try:
    Store.objects.filter(code=post_data.get('code')).update(name=post_data.get('name'),city_name=post_data.get('city_name'),city_code=post_data.get('city_code'),level=post_data.get('level'))
    return HttpResponse('OK')
def purchase(request):    #获取订单信息
    post_data = request.body
    post_data = json.loads(post_data)
    boci = post_data.get('boci') #a\获得波次信息
    print(boci)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=Purchase_order_tou.objects.filter(boci=boci).values().order_by('-id')
    else:
        user_list = Purchase_order_tou.objects.filter(boci=boci).values()
        user_list = user_list.filter(Q(order_code__icontains=post_data.get('serch'))|Q(store_name__icontains=post_data.get('serch'))|Q(store_code__icontains=post_data.get('serch'))|Q(note__icontains=post_data.get('serch'))).values().order_by('-id')
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def boci(request):    #获取所有的波次信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=Boci.objects.all().values().order_by('-id')
    else:
        user_list = Boci.objects.filter(Q(create_time__icontains=post_data.get('serch'))|Q(boci__icontains=post_data.get('serch'))|Q(note__icontains=post_data.get('serch'))).values().order_by('-id')
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def sale(request):    #获取订单信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=Sale_order_tou.objects.all().values().order_by('-id')
    else:
        user_list = Sale_order_tou.objects.filter(Q(order_code__icontains=post_data.get('serch'))|Q(date__icontains=post_data.get('serch'))|Q(boci__icontains=post_data.get('serch'))|Q(note__icontains=post_data.get('serch'))).values().order_by('-id')
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def delete_pur(request):
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)
    name=post_data.get('name')
    Purchase_order_tou.objects.filter(order_code=name).delete()
    Purchase_Del.objects.filter(order_code=name).delete()
    return HttpResponse('OK')
def delete_sale(request):
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)
    name=post_data.get('name')
    Sale_order_tou.objects.filter(order_code=name).delete()
    Sale_Del.objects.filter(order_code=name).delete()
    return HttpResponse('OK')
def order_store(request):    #获取sku信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_list = Store.objects.filter(Q(code__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))|Q(city_name__icontains=post_data.get('serch'))).values()
    user_page = Paginator(user_list, 700).page(1)
    for user_i in user_page:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def pur_order(request):    #抓取采购
    chache=pysql("exec PROC_NumIndent ")
    pysql_update("insert into num VALUES ('{}')".format(chache[0][0]))    #单号插入记录表
    return JsonResponse(data=chache, safe=False)
def order_sku(request):    #获取sku信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_list = SKU.objects.filter(Q(id__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))|Q(type__icontains=post_data.get('serch'))).values()
    user_page = Paginator(user_list,200).page(1)
    for user_i in user_page:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def order_boci(request):    #获取订单中的波次信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch'):
        user_list = Purchase_order_tou.objects.filter(Q(boci__icontains=post_data.get('serch')),status='待下发').values('boci').distinct()
    else:
        user_list = Purchase_order_tou.objects.filter(status='待下发').values('boci').distinct()
    user_page = Paginator(user_list, 7).page(1)
    for user_i in user_page:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def pur_boci(request):    #获取订单中的波次信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch'):
        user_list = Boci.objects.filter(Q(boci__icontains=post_data.get('serch'))).values('boci')
    else:
        user_list = Boci.objects.all().values('boci')
        print(user_list)
    user_page = Paginator(user_list, 50).page(1)
    for user_i in user_page:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def sale_boci(request):    #获取订单中的波次信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch'):
        user_list = Sale_order_tou.objects.filter(Q(boci__icontains=post_data.get('serch'))).values('boci').distinct()
    else:
        user_list = Sale_Del.objects.all().values('boci').distinct()
    user_page = Paginator(user_list, 7).page(1)
    for user_i in user_page:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def sale_boci(request):    #获取订单中的波次信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch'):
        user_list = Sale_order_tou.objects.filter(Q(boci__icontains=post_data.get('serch')),status='待下发').values('boci').distinct()
    else:
        user_list = Sale_order_tou.objects.filter(status='待下发').values('boci').distinct()
    user_page = Paginator(user_list, 7).page(1)
    for user_i in user_page:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def pur_save(request):   #采购订单保存
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)

    order_tou=post_data.get('order_tou')
    order_shen=post_data.get('order_shen')

    order_tou_save=Purchase_order_tou(order_code=order_tou.get('order_code'),date=order_tou.get('date'),note=order_tou.get('note'),boci=order_tou.get('boci'),create_time=date,store_code=order_tou.get('store_code'),store_name=order_tou.get('store_name'))

    for order_i in order_shen:
        order_shen_save=Purchase_Del(order_code=order_tou.get('order_code'),item_code=order_i.get('item_code'),item_name=order_i.get('item_name'),item_gg=order_i.get('item_gg'),
                                  unit=order_i.get('unit'),num=order_i.get('num'),note=order_i.get('note'),date=order_tou.get('date'),boci=order_tou.get('boci'),
                                     store_code=order_tou.get('store_code'), store_name=order_tou.get('store_name') )
        order_shen_save.save()
    order_tou_save.save()
    return HttpResponse('OK')
def sale_save(request):   #配送订单保存
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)

    order_tou=post_data.get('order_tou')
    order_shen=post_data.get('order_shen')

    order_tou_save=Sale_order_tou(order_code=order_tou.get('order_code'),date=order_tou.get('date'),note=order_tou.get('note'),boci=order_tou.get('boci'),create_time=date,store_code=order_tou.get('store_code'),store_name=order_tou.get('store_name'))

    for order_i in order_shen:
        order_shen_save=Sale_Del(order_code=order_tou.get('order_code'),item_code=order_i.get('item_code'),item_name=order_i.get('item_name'),item_gg=order_i.get('item_gg'),
                                  unit=order_i.get('unit'),sure_num=order_i.get('sure_num'),note=order_i.get('note'),date=order_tou.get('date'),boci=order_tou.get('boci'),
                                     store_code=order_tou.get('store_code'), store_name=order_tou.get('store_name') )
        order_shen_save.save()
    order_tou_save.save()
    return HttpResponse('OK')
def excel_analysis(request):
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    file_name=post_data.get('file_name')  #获得excel的名字
    path = os.path.join(MEDIA_ROOT, file_name + '.xls')  # 此处自定义文件名
    path = path.replace('\\', '/')
    data = xlrd.open_workbook(path)  # 打开文件
    sheet = data.sheet_by_index(0)  # 默认每次就来发第一个sheet
    # rows=sheet.nrows  #总行数
    cols = sheet.ncols  # 总列数
    cols_list = []  # 记录列内容
    sure_list = []  # 记录需要列的下标识,记住标识是小一号的
    for i in range(cols):  # 列循环
        cols_list.append(sheet.cell(0, i).value.replace(' ', ''))
        name = sheet.cell(0, i).value.replace(' ', '')

    if '站点' in cols_list and '站点名称' in cols_list and '商品' in cols_list and '商品名称' in cols_list and '销售数量' in cols_list and '期末数量' in cols_list:
        return HttpResponse('OK')
    else:
        return HttpResponse('NOT OK')

def excel_file( request):
    # 获取文件
    if request.method=='POST':
        files = request.FILES
        response = []
        # 取出文件的 key 和 value
        md5 = ''
        for key, value in files.items():
            # 读取文件
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            # 指定文件路径
            path = os.path.join(MEDIA_ROOT, md5 + '.xls')  #此处自定义文件名

            with open(path, 'wb') as f:
                # 保存文件
                f.write(content)

        response = JsonResponse(data=md5, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "DELETE, PUT, POST,GET,OPTIONS"
        response["Access-Control-Max-Age"] = "1800"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def excel_file_test( request):
    # 获取文件
    if request.method=='POST':
        files = request.FILES
        print(files)
        response = []
        # 取出文件的 key 和 value
        md5 = ''
        for key, value in files.items():
            # 读取文件
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            # 指定文件路径
            path = os.path.join(MEDIA_ROOT, md5 + '.xls')

            with open(path, 'wb') as f:
                # 保存文件
                f.write(content)

        response = JsonResponse(data=md5, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "DELETE, PUT, POST,GET,OPTIONS"
        response["Access-Control-Max-Age"] = "1800"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def excel_file_store(request):
    # 获取文件
    if request.method=='POST':
        files = request.FILES
        response = []
        # 取出文件的 key 和 value
        for key, value in files.items():
            # 读取文件
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            # 指定文件路径
            path = os.path.join(MEDIA_ROOT, md5 + '.xls')

            with open(path, 'wb') as f:
                # 保存文件
                f.write(content)
 #读取文件内容,先简单判断文件是否合格;1.判断常规的几列是否存在
            path=path.replace('\\', '/')
            data=xlrd.open_workbook(path)   #打开文件
            sheet =data.sheet_by_index(0)  #默认每次就来发第一个sheet
            #rows=sheet.nrows  #总行数
            cols=sheet.ncols  #总列数
            cols_list=[]    #记录列内容
            sure_list = [] #记录需要列的下标识,记住标识是小一号的
            for i in range(cols): #列循环
                cols_list.append(sheet.cell(0,i).value.replace(' ',''))
            name=sheet.cell(0,i).value.replace(' ','')
            #if name != '站点' and name != '站点名称' and name != '商品' and name != '商品名称' and name != '销售数量' and name != '期末数量':
            # sheet.delete_cols(i) #删除此列

            if '站点编码' in cols_list and '站点名称' in cols_list and '城市代码' in cols_list and '城市名称' in cols_list and '等级' in cols_list:
            #先删除多余的列,为计算增加速度站点编码	站点名称	城市代码	城市名称	等级
                return JsonResponse(data=md5, safe=False)
            else:
                return HttpResponse('nothing')
def auto_pur(request):  #自动计算采购单数据
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    inform=post_data.get('inform')
    boci=inform.get('boci')
    note=inform.get('note')
    date=inform.get('date')
    infile=inform.get('infile')  #上传文件的名字
    ts = str(datetime.datetime.now().timestamp())  #生成时间戳,并转换为字符格式
    create_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间

    path = os.path.join(MEDIA_ROOT, infile + '.xls').replace('\\', '/') #得到路径
    path = path.replace('\\', '/')
    data = xlrd.open_workbook(path)  # 打开文件
    sheet = data.sheet_by_index(0)  # 默认每次就来发第一个sheet
    rows=sheet.nrows  #总行数
    cols = sheet.ncols  # 总列数
    cols_list = []  # 记录列内容
    sure_list = []  # 记录需要列的下标识,记住标识是小一号的
    for i in range(cols):  # 列循环
        cols_list.append(sheet.cell(0, i).value.replace(' ', ''))
    #将需要的几列下标计算出来
    sure_list.append(cols_list.index('站点'))     #0
    sure_list.append(cols_list.index('站点名称'))  #1
    sure_list.append(cols_list.index('商品'))     #2
    sure_list.append(cols_list.index('商品名称'))  #3
    sure_list.append(cols_list.index('销售数量'))  #4
    sure_list.append(cols_list.index('期末数量'))  #5
    sure_list.append(cols_list.index('单位'))  #6
    #开始每一行计算数据结果

    store_qian = '' #记录前一行站点的名字内容
    #1.现将数据库的内容清空
    chache = pysql("exec PROC_NumIndent ")
    pysql_update("insert into num VALUES ('{}')".format(chache[0][0]))  # 单号插入记录表
    order_code = 'A_'+chache[0][0] #先提前获得单号
    order_save_list = []  #数据保存合计
    total_num = 0 #固定周期计数
    for ii in range(1,rows): #行循环,第一行不算
        skus = SKU.objects.filter(id=str(int(sheet.cell(ii,sure_list[2]).value))).values('status','unit','so_min_num','so_multiple_num') #获取SKU的状态
        if skus:  #SKU信息存在时
            sku_status = skus[0].get('status')
            sku_unit = skus[0].get('unit')
            if sheet.cell(ii,sure_list[0]).value.replace(' ','') != '' and str(int(sheet.cell(ii,sure_list[2]).value)) != '' and sku_status:  #商品不为空时继续,并且状态是启用
                #print(ii,sheet.cell(ii,sure_list[4]).value,cols,rows)
            #商品和站点编码为空时跳过
                if ((isinstance(sheet.cell(ii,sure_list[4]).value,int) or isinstance(sheet.cell(ii,sure_list[4]).value,float)) and sheet.cell(ii,sure_list[4]).value > 0) or \
                    (isinstance(sheet.cell(ii,sure_list[4]).value,str) and sheet.cell(ii,sure_list[4]).value != ''  ): #只有销量大于0时才计算
                    #开始插入数据表内容,首先插入单身,其次插入单头
                    if isinstance(sheet.cell(ii,sure_list[5]).value,str) and sheet.cell(ii,sure_list[5]).value == '':
                        order_num = round(int(sheet.cell(ii,sure_list[4]).value)*10/30) - 0    #计算应该补货的数量
                    else:
                        order_num = round(int(sheet.cell(ii,sure_list[4]).value)*10/30) - int(sheet.cell(ii,sure_list[5]).value)   #计算应该补货的数量
                    if order_num > 0: #大于0时才补货
                        #计算起订量和最小采购量之间的关系   sku编码 str(int(sheet.cell(ii,sure_list[2]).value))
                        #sku_num = SKU.objects.filter(id=str(int(sheet.cell(ii,sure_list[2]).value))).values('so_min_num','so_multiple_num') #获得最小起订量和倍数
                        #if sku_num:  #先定义sku信息存在
                        if skus[0].get('so_min_num') and skus[0].get('so_multiple_num'): #标识存在
                            #解释下面公式:计算量/订货倍数,取得整数*订货倍数
                            if order_num < skus[0].get('so_min_num') :#小于最小起订量
                                continue  #跳出循环,不参与了
                            else: #如果大于最小起订量:起订量+(订单量-起订量)/倍数 向下取整  *倍数  ;得到最新的数
                                order_num = skus[0].get('so_min_num') + int((order_num-skus[0].get('so_min_num'))/skus[0].get('so_multiple_num')) * skus[0].get('so_multiple_num')

                        try:
                            if store_qian != sheet.cell(ii,sure_list[0]).value.replace(' ',''): #如果前一行的站点名称不等于本行的站定名称,则单号重新取值
                                chache = pysql("exec PROC_NumIndent ")
                                pysql_update("insert into num VALUES ('{}')".format(chache[0][0]))  # 单号插入记录表
                                order_code = 'A_'+chache[0][0]  #先提前获得单号     #重新取值
                                #这种情况下,新增一次单头就可以
                                order_tou_save = Purchase_order_tou(order_code=order_code, date=date, note=note, boci=boci,
                                                                    create_time=create_date, biaozhi=ts,
                                                                    store_code=sheet.cell(ii, sure_list[0]).value.replace(' ',''),
                                                                    store_name=sheet.cell(ii, sure_list[1]).value.replace(' ',''))
                                order_tou_save.save()

                            order_shen_i = Purchase_Del(order_code=order_code,item_code=str(int(sheet.cell(ii,sure_list[2]).value)),
                                                           item_name=sheet.cell(ii,sure_list[3]).value,
                                                           unit=sku_unit,
                                                           num=order_num,note=note,boci=boci,biaozhi=ts,date=date,
                                                           store_code=sheet.cell(ii,sure_list[0]).value.replace(' ',''),store_name=sheet.cell(ii,sure_list[1]).value.replace(' ',''))
                            order_save_list.append(order_shen_i)
                            if len(order_save_list) == 200 or rows-ii < 200:  #每500行或者最后200行开始保存一次数据库,减少数据库的交互
                                Purchase_Del.objects.bulk_create(order_save_list)
                                #清空内容
                                order_save_list = []
                            #记录前一行计算的内容
                            store_qian = sheet.cell(ii,sure_list[0]).value.replace(' ','')
                        except Exception as ex:
                            Purchase_order_tou.objects.filter(boci=boci).delete()   #删除
                            Purchase_Del.objects.filter(boci=boci).delete()   #删除
                            return HttpResponse(ii+1)   #返回错误的行信息
    #保存整个批次信息
    boci_save=Boci(boci=boci,note=note,create_time=date,status='待下发')
    boci_save.save()
    #返回前端信息
    return HttpResponse('OK')
def auto_store(request):  #自动计算采购单数据
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    inform=post_data.get('inform')
    infile=inform.get('infile')  #上传文件的名字
    ts = str(datetime.datetime.now().timestamp())  #生成时间戳,并转换为字符格式
    create_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间

    path = os.path.join(MEDIA_ROOT, infile + '.xls').replace('\\', '/') #得到路径
    path = path.replace('\\', '/')
    data = xlrd.open_workbook(path)  # 打开文件
    sheet = data.sheet_by_index(0)  # 默认每次就来发第一个sheet
    rows=sheet.nrows  #总行数
    cols = sheet.ncols  # 总列数
    cols_list = []  # 记录列内容
    sure_list = []  # 记录需要列的下标识,记住标识是小一号的
    for i in range(cols):  # 列循环
        cols_list.append(sheet.cell(0, i).value.replace(' ', ''))
    #将需要的几列下标计算出来
    if cols_list[0] =='站点编码' and cols_list[1] =='站点名称' and cols_list[2] =='城市代码' and cols_list[3] =='城市名称' and cols_list[4] =='等级':

        for ii in range(1,rows): #行循环,第一行不算
            if Store.objects.filter(code=str(sheet.cell(ii,0).value).replace(' ','')): #说明编码已经存在了,执行更新
                Store.objects.filter(code=str(sheet.cell(ii,0).value).replace(' ','')).update(name=sheet.cell(ii,1).value.replace(' ',''),
                                city_code=sheet.cell(ii,2).value.replace(' ',''),city_name=sheet.cell(ii,3).value.replace(' ',''),level=sheet.cell(ii,4).value.replace(' ',''))
            else:#标识新增的内容
                store_new=Store(code=str(sheet.cell(ii,0).value).upper().replace(' ',''),name=sheet.cell(ii,1).value.replace(' ',''),
                                city_code=sheet.cell(ii,2).value.replace(' ',''),city_name=sheet.cell(ii,3).value.replace(' ',''),level=sheet.cell(ii,4).value.replace(' ',''))
                store_new.save()
            # 返回前端信息
        return HttpResponse('OK')
    else:
        return HttpResponse(404)

def pur_delete_PL (request):
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    boci=post_data.get('boci')
    Boci.objects.filter(boci=boci,status='待下发').delete()
    Purchase_order_tou.objects.filter(boci=boci,status='待下发').delete() #删除单头
    Purchase_Del.objects.filter(boci=boci,status='待下发').delete()
    return HttpResponse('OK')
def order_del(request):    #订单查询窗口
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    selectForm = post_data.get('serch')
    if selectForm.get('date') or selectForm.get('order_code') or selectForm.get('status') or selectForm.get('boci') or selectForm.get('store_name') or selectForm.get('item_name'):
        user_list=Purchase_Del.objects.all().values()
        if selectForm.get('date'):
            print(selectForm.get('date'))
        if selectForm.get('order_code'):
            user_list=user_list.filter(order_code__contains=selectForm.get('order_code'))
        if selectForm.get('status'):
            user_list=user_list.filter(status=selectForm.get('status'))
        if selectForm.get('boci'):
            user_list=user_list.filter(boci=selectForm.get('boci'))
        if selectForm.get('store_name'):
            user_list=user_list.filter(store_name=selectForm.get('store_name'))
        if selectForm.get('item_name'):
            user_list=user_list.filter(item_name=selectForm.get('item_name'))

    else:
        user_list = Purchase_Del.objects.all().values().order_by('-id')
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list'] = user_json
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def sale_del(request):    #订单查询窗口
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    selectForm = post_data.get('serch')
    if selectForm.get('date') or selectForm.get('order_code') or selectForm.get('status') or selectForm.get('boci') or selectForm.get('store_name') or selectForm.get('item_name'):
        user_list=Sale_Del.objects.all().values()
        if selectForm.get('date'):
            print(selectForm.get('date'))
        if selectForm.get('order_code'):
            user_list=user_list.filter(order_code__contains=selectForm.get('order_code'))
        if selectForm.get('status'):
            user_list=user_list.filter(status=selectForm.get('status'))
        if selectForm.get('boci'):
            user_list=user_list.filter(boci=selectForm.get('boci'))
        if selectForm.get('store_name'):
            user_list=user_list.filter(store_name=selectForm.get('store_name'))
        if selectForm.get('item_name'):
            user_list=user_list.filter(item_name=selectForm.get('item_name'))

    else:
        user_list = Sale_Del.objects.all().values().order_by('-id')
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list'] = user_json
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def page_get(request):  #页面查询和修改初始化
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num=post_data.get('order')   #得到单号
    order_tou=Purchase_order_tou.objects.filter(order_code=order_num).values()
    order_tou=order_tou[0]
    order_shen_json=[]
    order_shen=Purchase_Del.objects.filter(order_code=order_num).values()
    for order_shen_i in order_shen:
        order_shen_json.append(order_shen_i)
    data={}
    data['tou']=order_tou
    data['shen']=order_shen_json
    return JsonResponse(data=data, safe=False)
def pur_update(request):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)

    order_tou = post_data.get('order_tou')
    order_shen = post_data.get('order_shen')
    order_delete = post_data.get('delete_li')  # 记录删除的内容

    order_tou_save = Purchase_order_tou.objects.filter(order_code=order_tou.get('order_code')).update(note=order_tou.get('note'))
    #先删除目前所有的内容
    # 删除前台删除的内容
    for delete_i in order_delete:
        Purchase_Del.objects.filter(id=delete_i).delete()  # 删除本行内容
    #重新创建
    for order_i in order_shen:
        if order_i.get('id'):  # 标识存在
            Purchase_Del.objects.filter(id=order_i.get('id')).update(num=order_i.get('num'), note=order_i.get('note'))
        else:#新增的行
            order_shen_save = Purchase_Del(order_code=order_tou.get('order_code'), item_code=order_i.get('item_code'),
                                           item_name=order_i.get('item_name'), item_gg=order_i.get('item_gg'),
                                           unit=order_i.get('unit'), num=order_i.get('num'), note=order_i.get('note'),
                                           date=order_tou.get('date'), boci=order_tou.get('boci'),
                                           store_code=order_tou.get('store_code'),
                                           store_name=order_tou.get('store_name'))
            order_shen_save.save()
    return HttpResponse('OK')
def pur_api_PL(request):
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    boci = post_data.get('boci')
    SO_API(boci)
    return HttpResponse('OK')#标识已经下发
def sale_api_PL(request):
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    boci = post_data.get('boci')
    SALE_API(boci)
    return HttpResponse('OK')#标识已经下发

def test(request): #用来测试
    order_que = SKU.objects.filter(id='70212266').values('so_min_num','so_multiple_num')
    print(order_que[0])
    return HttpResponse('OK')#标识已经下发


def API_del(request):    #订单查询窗口
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    selectForm = post_data.get('serch')
    if selectForm.get('date') or selectForm.get('order_code') or selectForm.get('status') or selectForm.get('boci'):
        user_list=SO_First_API.objects.all().values().order_by('-id')
        if selectForm.get('date'):
            print(selectForm.get('date'))
        if selectForm.get('order_code'):
            user_list=user_list.filter(order_code__contains=selectForm.get('order_code'))
        if selectForm.get('status'):
            user_list=user_list.filter(status=selectForm.get('status'))
        if selectForm.get('boci'):
            user_list=user_list.filter(boci=selectForm.get('boci'))

    else:
        user_list = SO_First_API.objects.all().values().order_by('-id')
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list'] = user_json
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def excel_out(request): #导出表格
    date_miao = time.strftime('%Y%m%d%H%M%S', time.localtime())  #时间戳
    post_data = request.body
    post_data = json.loads(post_data)
    selectForm = post_data.get('serch')
    user_list = []
    if selectForm.get('date') or selectForm.get('order_code') or selectForm.get('status') or selectForm.get('boci'):
        user_list=SO_First_API.objects.all().values().order_by('-id')
        if selectForm.get('date'):
            print(selectForm.get('date'))
        if selectForm.get('order_code'):
            user_list=user_list.filter(order_code__contains=selectForm.get('order_code'))
        if selectForm.get('status'):
            user_list=user_list.filter(status=selectForm.get('status'))
        if selectForm.get('boci'):
            user_list=user_list.filter(boci=selectForm.get('boci'))

    else:
        user_list = SO_First_API.objects.all().values().order_by('-id')
        #处理表格
    new_excel = xlwt.Workbook(encoding='udf-8')
    new_sheet = new_excel.add_sheet('导出接口日志')  # 创建excel
    new_sheet.write(0, 0, '系统订单号')  # 列头
    new_sheet.write(0, 1, '订货批次')  # 列头
    new_sheet.write(0, 2, '日期')
    new_sheet.write(0, 3, '状态')
    new_sheet.write(0, 4, '性质')
    new_sheet.write(0, 5, '详情')
    #读取数据库的内容化
    i = 1 #定义行数
    if user_list:
        for jt_i in user_list:
            new_sheet.write(i, 0,jt_i.get('order_code'))  # 列头
            new_sheet.write(i, 1, 'boci')  # 列头
            new_sheet.write(i, 2, jt_i.get('date'))
            new_sheet.write(i, 3, jt_i.get('status'))
            new_sheet.write(i, 4, jt_i.get('type'))
            new_sheet.write(i, 5, jt_i.get('detial'))
            #行数加一
            i=i+1
        #保存表格到服务器
        path = os.path.join(MEDIA_ROOT, date_miao + '.xls')
        new_excel.save(r'{}'.format(path))  # 保存表格
        return HttpResponse(date_miao)
    else:
        return HttpResponse('Nothing')
def excel(request):  #上面函数是生成表格,这个是表格下载链接
    md5 = request.GET.get("excel")
    imgfile = os.path.join(MEDIA_ROOT, md5 + '.xls').replace('\\', '/')
    imgfile = imgfile.replace('"', '')
    if os.path.exists(imgfile):
        data = open(imgfile, 'rb').read()

        # update_file_path文件存放位置
        file = open(imgfile, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/vnd.ms-excel'
        response['Content-Disposition'] = f"attachment; filename={escape_uri_path('下发日志.xls')};"
        return response
def SALE_del(request):    #订单查询窗口
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    selectForm = post_data.get('serch')
    if selectForm.get('date') or selectForm.get('order_code') or selectForm.get('status') or selectForm.get('boci'):
        user_list=SALE_First_API.objects.all().values().order_by('-id')
        if selectForm.get('date'):
            print(selectForm.get('date'))
        if selectForm.get('order_code'):
            user_list=user_list.filter(order_code__contains=selectForm.get('order_code'))
        if selectForm.get('status'):
            user_list=user_list.filter(status=selectForm.get('status'))
        if selectForm.get('boci'):
            user_list=user_list.filter(boci=selectForm.get('boci'))

    else:
        user_list = SALE_First_API.objects.all().values().order_by('-id')
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list'] = user_json
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def stock(request):    #获取库存信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=Stock.objects.all().values()
    else:
        user_list = Stock.objects.filter(Q(id__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))).values()
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['sku_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def stock_api(request):
    sku=STOCK_API()
    if sku == 'error':
        return HttpResponse('error')
    else:
        return HttpResponse('OK')
def so_get_api(request):#订单反馈接受接口
    date_new = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
    path = os.path.join(MEDIA_ROOT, '123.txt').replace('\\', '/')  # 得到路径
    f = open(path, 'w')
    f.write('123')
    f.close()
    if request.method == 'POST':

        post_data = request.POST.dict()
        false = "啥也不是"  # 为了转换布尔类型啊,难死了
        bizdata=post_data.get('bizData')
        bizdata=json.loads(bizdata)
        post_data = str(post_data.get('bizData'))
        path = os.path.join(MEDIA_ROOT, 'api.txt').replace('\\', '/')  # 得到路径
        f = open(path, 'w')
        f.write(post_data)
        f.close()
        try:
            if Purchase_order_tou.objects.filter(order_code=bizdata.get('outerCode')) and (
                    1 == bizdata.get('status') or 3 == bizdata.get('status') or 5 == bizdata.get('status')):  # 如果订单号存在
                # 每次更新前先清空,确保每次得到的都是最新的消息,更新未0
                Purchase_Del.objects.filter(order_code=bizdata.get('outerCode')).update(sure_num=0)
                for list in bizdata.get('detailList'):
                    # 判断商品编码是否存在
                    if Purchase_Del.objects.filter(order_code=bizdata.get('outerCode'),item_code=list.get('goodsCode')):  # 存在的修改,不存在的插入
                        Purchase_Del.objects.filter(order_code=bizdata.get('outerCode'),
                                                    item_code=list.get('goodsCode')).update(sure_num=int(list.get('goodsQuantity')))
                    else:  # 不存在时,需要插入一条新数据
                        order_shen_save = Purchase_Del(order_code=bizdata.get('outerCode'),item_code=list.get('goodsCode'), unit=list.get('goodsUnitName'),
                                                       # 商品的名称等信息并没有做更新,最后批量更新一下
                                                       boci=bizdata.get('remark'), sure_num=int(list.get('goodsQuantity')),store_code=bizdata.get( 'customerCode'))  # 门店的名称等信息并没有做更新,最后批量更新一下
                        order_shen_save.save()  # 保存数据表
                        pysql_update(
                            "update xunjie_purchase_del set item_name=name,item_gg=type from xunjie_purchase_del inner join xunjie_sku on item_code = xunjie_sku.id where item_code='{}' and order_code = '{}' and item_name=''".format(
                                list.get('goodsCode'), bizdata.get('outerCode')))
                        pysql_update(
                            "update xunjie_purchase_del set store_name = name from xunjie_purchase_del inner join xunjie_store on store_code = code where item_code='{}' and order_code = '{}' and store_name=''".format(
                                list.get('goodsCode'), bizdata.get('outerCode')))
                   #更新明细航的状态
                    if 1 == bizdata.get('status'):  # 1标识门店审核
                        Purchase_Del.objects.filter(order_code=bizdata.get('outerCode'),item_code=list.get('goodsCode')).update(status='门店审核')
                        # 插入接口状态
                    if 3 == bizdata.get('status'):  # 1标识门店审核
                        Purchase_Del.objects.filter(order_code=bizdata.get('outerCode'),item_code=list.get('goodsCode')).update(status='市审核')
                    if 5 == bizdata.get('status'):  # 1标识门店审核
                        Purchase_Del.objects.filter(order_code=bizdata.get('outerCode'),item_code=list.get('goodsCode')).update(status='省审核')
                        sales=Sale_Del(pur_code=bizdata.get('outerCode'),order_code=bizdata.get('outerCode').replace('A_','B_'),item_code=list.get('goodsCode'), unit=list.get('goodsUnitName'),
                                                       # 商品的名称等信息并没有做更新,最后批量更新一下
                                                       boci=bizdata.get('remark'),status='待下发',num=int(list.get('goodsQuantity')),sure_num=int(list.get('goodsQuantity')),store_code=bizdata.get( 'customerCode'))
                        sales.save()  #订单明细保存
                        pysql_update(
                            "update xunjie_sale_del set item_name=name,item_gg=type from xunjie_sale_del inner join xunjie_sku on item_code = xunjie_sku.id where item_code='{}' and pur_code = '{}'".format(
                                list.get('goodsCode'), bizdata.get('outerCode')))
                        pysql_update(
                            "update xunjie_sale_del set store_name = name from xunjie_sale_del inner join xunjie_store on store_code = code where item_code='{}' and pur_code = '{}'".format(
                                list.get('goodsCode'), bizdata.get('outerCode')))
                if 1 == bizdata.get('status'):  # 1标识门店审核
                    Purchase_order_tou.objects.filter(order_code=bizdata.get('outerCode')).update(sure_status='门店审核')
                    Purchase_Del.objects.filter(order_code=bizdata.get('outerCode')).update(status='门店审核')
                    # 插入接口状态
                    so = SO_First_API(order_code=bizdata.get('outerCode'), boci=bizdata.get('remark'), date=date_new,
                                      status='成功', type='门店审核')
                    so.save()
                if 3 == bizdata.get('status'):  # 1标识门店审核
                    Purchase_order_tou.objects.filter(order_code=bizdata.get('outerCode')).update(sure_status='市审核')
                    Purchase_Del.objects.filter(order_code=bizdata.get('outerCode')).update(status='市审核')
                    so = SO_First_API(order_code=bizdata.get('outerCode'), boci=bizdata.get('remark'), date=date_new,
                                      status='成功', type='市审核')
                    so.save()
                if 5 == bizdata.get('status'):  # 1标识门店审核
                    Purchase_order_tou.objects.filter(order_code=bizdata.get('outerCode')).update(sure_status='省审核')
                    Purchase_Del.objects.filter(order_code=bizdata.get('outerCode')).update(status='省审核')
                    sale=Sale_order_tou(pur_code=bizdata.get('outerCode'),order_code=bizdata.get('outerCode').replace('A_','B_'),boci=bizdata.get('remark'),status='待下发',store_code=bizdata.get('customerCode'))
                    sale.save()
                    pysql_update(
                        "update xunjie_sale_order_tou set store_name = name from xunjie_sale_order_tou inner join xunjie_store on store_code = code where pur_code = '{}'".format( bizdata.get('outerCode')))
                    so = SO_First_API(order_code=bizdata.get('outerCode'), boci=bizdata.get('remark'), date=date_new,
                                      status='成功', type='省审核')
                    so.save()
            result ={'result': True, 'errorCode': '', 'errorDescription': ''}
            return JsonResponse(data=result, safe=False)
        except:
            result ={'result': False, 'errorCode': '8009', 'errorDescription': '接口收到消息,但是处理程序异常'}
            return JsonResponse(data=result, safe=False)
def order_Approval(request):  #单个订单下发
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num=post_data.get('order')
    print(order_num)
    SO_API_One(order_num)
    return HttpResponse('OK')
def sale_Approval(request):  #单个订单下发
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num=post_data.get('order')
    SALE_API_One(order_num)
    return HttpResponse('OK')
def sale_update(request):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)

    order_tou = post_data.get('order_tou')
    order_shen = post_data.get('order_shen')
    order_delete = post_data.get('delete_li')  # 记录删除的内容

    order_tou_save = Sale_order_tou.objects.filter(order_code=order_tou.get('order_code')).update(note=order_tou.get('note'))
    # 先删除目前所有的内容
    # 删除前台删除的内容
    for delete_i in order_delete:
        Sale_Del.objects.filter(id=delete_i).delete()  # 删除本行内容
    # 重新创建
    for order_i in order_shen:
        if order_i.get('id'):  # 标识存在
            Sale_Del.objects.filter(id=order_i.get('id')).update(num=order_i.get('num'), note=order_i.get('note'),sure_num=order_i.get('sure_num'))
        else:
            order_shen_save = Sale_Del(order_code=order_tou.get('order_code'), item_code=order_i.get('item_code'),
                                       item_name=order_i.get('item_name'), item_gg=order_i.get('item_gg'),
                                       unit=order_i.get('unit'), sure_num=order_i.get('sure_num'), note=order_i.get('note'),
                                       date=order_tou.get('date'), boci=order_tou.get('boci'),
                                       store_code=order_tou.get('store_code'),
                                       store_name=order_tou.get('store_name'))
            order_shen_save.save()
    return HttpResponse('OK')
def sale_page_get(request):  #页面查询和修改初始化
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num=post_data.get('order')   #得到单号
    print(order_num)
    order_tou=Sale_order_tou.objects.filter(order_code=order_num).values()
    order_tou=order_tou[0]
    order_shen_json=[]
    order_shen=Sale_Del.objects.filter(order_code=order_num,).values()
    for order_shen_i in order_shen:
        order_shen_json.append(order_shen_i)
    data={}
    data['tou']=order_tou
    data['shen']=order_shen_json
    return JsonResponse(data=data, safe=False)
def store_excel(request):  #门店导出模板
    md5 ='store'
    imgfile = os.path.join(MEDIA_ROOT, md5 + '.xls').replace('\\', '/')
    imgfile = imgfile.replace('"', '')
    if os.path.exists(imgfile):
        data = open(imgfile, 'rb').read()

        # update_file_path文件存放位置
        file = open(imgfile, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/vnd.ms-excel'
        # file_name下载下来保存的文件名字
        response['Content-Disposition'] = f"attachment; filename={escape_uri_path('站点导入模板.xls')};"
        return response
def calculation(request):#分配库存
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    data=post_data.get('data')
    boci=data.get('boci')
    type=data.get('type')
    proportion=data.get('proportion')  #分配比例
    #同步所有库存情况
    #第一步先计算库存充足的,然后判断库存是否足够
    STOCK_API()
    print(boci)
    AA=pysql("exec PROC_FP @boci='{}'".format(boci)) #执行存储过程,计算满足的明细航和状态
    if Store.objects.filter(level='').values(): #标识有商店ABC没填写
        return HttpResponse(404)
    else:#站点没问题
        #1.针对明细航库存缺少的信息,按照ABC优先级进行
        stock_que = Stock.objects.filter(stocks_tatus ='2').values()  # 获得全部库存不满足信息
        stores= Store.objects.all().values('code').order_by('level')  #按照ABC排序的门店信息

        for stock_i in stock_que: #循环信息
            num_ku=stock_i.get('avail_num') #得到本行的可用库存
            item_code=stock_i.get('id')  #sku编码
            #挨个门店开始计算库存信息
            for store_i in stores:
                order_que = Sale_Del.objects.filter(store_code=store_i.get('code'),item_code=item_code,boci=boci).values('num','id')
                if order_que: #如果存在才执行,可能有些有库存,但是不存在明细航
                    for order_i in order_que:  #缺少的订单明细航
                        num_order = order_i.get('num')  # 得到订单的需求量
                        order_id = order_i.get('id')  # 得到订单坐标
                        if type == '1': #标识按照ABC分类
                            if num_order <= num_ku: #如果订单量小于等于库存量,则,更新订单量,更新库存量num_ku
                                Sale_Del.objects.filter(id=order_i).update(sure_num=num_order)
                                num_ku = num_ku- num_order    #更新库存的数量
                            elif num_order > num_ku and num_ku > 0:
                                Sale_Del.objects.filter(id=order_i).update(sure_num=num_ku)  #直接等于剩余库存量
                                num_ku = 0 # 直接赋值为0
                            if num_ku == 0: #已经为0了,可以跳出循环了
                                break;  #跳出循环了
                        elif type ==2 :#按照固定比例分配
                            num_order=int(round(num_order*proportion))   #按照比例四舍五入
                            if num_order <= num_ku:  # 如果订单量小于等于库存量,则,更新订单量,更新库存量num_ku
                                Sale_Del.objects.filter(id=order_i).update(sure_num=num_order)
                                num_ku = num_ku - num_order  # 更新库存的数量
                            elif num_order > num_ku and num_ku > 0:
                                Sale_Del.objects.filter(id=order_i).update(sure_num=num_ku)  # 直接等于剩余库存量
                                num_ku = 0  # 直接赋值为0
                            if num_ku == 0:  # 已经为0了,可以跳出循环了
                                break;  # 跳出循环了
                if num_ku == 0:  # 已经为0了,在跳出一级循环
                    break;
            if num_ku == 0:  # 已经为0了,在跳出一级循环
                break;
    return HttpResponse('OK')  #返回信息

def puhuo(request):
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    data=post_data.get('PH')
    boci=data.get('boci')
    item_code=data.get('item_code')
    item_name=data.get('item_name')
    num=data.get('num')
    order_tou = Sale_order_tou.objects.filter(boci=boci).values()  #得到所有的订单号
    for order_i in order_tou: #循环单号
        order=order_i.get('order_code')
        print(order,boci)
        if Sale_Del.objects.filter(order_code=order,boci=boci,item_code=item_code).values(): #标识已经存在
            print('bucunzai ')
        else:
            sales=Sale_Del(order_code=order,item_code=item_code,sure_num=num,note='铺货',boci=boci,item_name=item_name,
                           store_code=order_i.get('store_code'),store_name=order_i.get('store_name'))
            sales.save()
        #更新包装单位
            pysql_update(
                "update xunjie_sale_del set unit=xunjie_sku.unit,item_gg=type from xunjie_sale_del inner join xunjie_sku on item_code = xunjie_sku.id where item_code='{}' and order_code = '{}'".format(item_code,order))
    return HttpResponse('OK')
def pur_puhuo(request):   #采购铺货
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    data=post_data.get('PH')
    boci=data.get('boci')
    item_code=data.get('item_code')
    item_name=data.get('item_name')
    skus=SKU.objects.filter(id=item_code).values('unit')
    unit = skus[0].get('unit')   #获得单位
    num=data.get('num')
    store_list = Store.objects.all().values('code','name','status')  #获取所有的店铺信息
    for store_i in store_list: #门店开始循环
        if store_i.get('status'):
            ts = str(datetime.datetime.now().timestamp())  # 生成时间戳,并转换为字符格式
            create_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
            if Purchase_order_tou.objects.filter(Q(boci=boci),Q(store_code__icontains=store_i.get('code'))): #如果门店已经存在批次信息里面了
                continue  #跳出循环
            else: #如果门店信息不存在
                #1.增加单头信息,获取单号
                chache = pysql("exec PROC_NumIndent ")
                pysql_update("insert into num VALUES ('{}')".format(chache[0][0]))  # 单号插入记录表
                order_num = 'A_'+chache[0][0]
                order_tou =Purchase_order_tou(order_code=order_num,boci=boci,store_code=store_i.get('code'),store_name=store_i.get('name'),biaozhi=ts,create_time=create_date,note='采购铺货')
                #2.增加单身信息
                order_shen = Purchase_Del(order_code=order_num,item_code=item_code,item_name=item_name,boci=boci,biaozhi=ts,num=num,store_code=store_i.get('code'),store_name=store_i.get('name'),status='待下发',sure_num=0,unit=unit)
                order_shen.save()
                order_tou.save()
    return HttpResponse('OK')
def update_mima(request):
    post_data = request.body
    post_data = json.loads(post_data)
    print(post_data)
    mima_old=User.objects.filter(name=post_data.get('id'),password=post_data.get('password_old'))
    if mima_old:
        User.objects.filter(name=post_data.get('id'),password=post_data.get('password_old')).update(password=post_data.get('password_new'))
        return HttpResponse('OK')
    else:
        return HttpResponse('300')