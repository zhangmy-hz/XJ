from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse,FileResponse  #引入json响应
import json,requests
import os,django,time,xlrd,datetime
from django.middleware.csrf import get_token
import  hashlib
from xunjie.sql import  pysql,pysql_update


aa=pysql("delete num")