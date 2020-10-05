"""xjdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from xunjie import views as myviews

urlpatterns = [
    #path('', admin.site.urls),
    path('', myviews.so_get_api),
    #path('admin/', admin.site.urls),
    path('login/',myviews.login),
    path('quanxian_get/',myviews.quanxian_get),
    path('user/',myviews.user),
    path('user_status/',myviews.user_status),
    path('add_user/',myviews.add_user),
    path('user_up_select/',myviews.user_up_select),
    path('user_update/',myviews.user_update),
    path('delete_user/',myviews.delete_user),

    path('roles/',myviews.roles),
    path('quanxian_list_all/',myviews.quanxian_list_all),
    path('role_check/',myviews.role_check),
    path('role_save/',myviews.role_save),
    path('role_new/',myviews.role_new),
    path('role_select/',myviews.role_select),
    path('update_role_select/',myviews.update_role_select),
    path('role_up_save/',myviews.role_up_save),
    path('delete_role/',myviews.delete_role),
    path('get_role/',myviews.get_role),
    path('sku_api/',myviews.sku_api),
    path('sku/',myviews.sku),
    path('store/',myviews.store),
    path('add_store/',myviews.add_store),
    path('store_status/',myviews.store_status),
    path('store_up_select/',myviews.store_up_select),
    path('stroe_update/',myviews.stroe_update),
    path('purchase/',myviews.purchase),
    path('delete_pur/',myviews.delete_pur),
    path('order_store/',myviews.order_store),
    path('pur_order/',myviews.pur_order),
    path('order_sku/',myviews.order_sku),
    path('pur_save/',myviews.pur_save),
    path('excel_file/',myviews.excel_file),
    path('auto_pur/',myviews.auto_pur),
    path('order_boci/',myviews.order_boci),
    path('pur_delete_PL/',myviews.pur_delete_PL),
    path('order_del/',myviews.order_del),
    path('page_get/',myviews.page_get),
    path('pur_update/',myviews.pur_update),
    path('pur_api_PL/',myviews.pur_api_PL),
    path('test/',myviews.test),
    path('API_del/',myviews.API_del),
    path('stock/',myviews.stock),
    path('stock_api/', myviews.stock_api),
    path('get_so/',myviews.so_get_api),
    path('order_Approval/',myviews.order_Approval),
    path('sale/',myviews.sale),
    path('sale_update/',myviews.sale_update),
    path('sale_page_get/',myviews.sale_page_get),
    path('delete_sale/',myviews.delete_sale),
    path('sale_boci/',myviews.sale_boci),
    path('sale_save/',myviews.sale_save),
    path('sale_del/',myviews.sale_del),
    path('pur_boci/',myviews.pur_boci),
    path('sale_boci/',myviews.sale_boci),
    path('store_excel/',myviews.store_excel),
    path('excel_file_store/',myviews.excel_file_store),
    path('auto_store/',myviews.auto_store),
    path('calculation/',myviews.calculation),
    path('puhuo/',myviews.puhuo),
    path('sale_api_PL/',myviews.sale_api_PL),
    path('sale_Approval/',myviews.sale_Approval),
    path('SALE_del/',myviews.SALE_del),
    path('update_mima/',myviews.update_mima),
    path('boci/',myviews.boci),
    path('excel_file_test/',myviews.excel_file_test),
    path('excel/',myviews.excel),
    path('excel_out/',myviews.excel_out),
    path('excel_analysis/',myviews.excel_analysis),
    path('pur_puhuo/',myviews.pur_puhuo),
]
