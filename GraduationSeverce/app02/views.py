from django.shortcuts import render,render_to_response
from django.http import HttpResponse
# Create your views here.

import json


def Auth(request):
    print request.GET
    user,passwd = request.GET['username'],request.GET['passwd']

    if user=='lishishuang' and passwd == '0925':
        return HttpResponse('welcome user %s login our website'%user)
    else:
        return HttpResponse('wrong username or passwd rang')

def Index(request):
    print  'hshhahah',request
    return HttpResponse('<h1>Hello world !</h1>')
def Login(request):

    return render_to_response('index.html')

def Menu(request):
    region_dic = {
        'ShanDong':{'Jinan':['JiNing',
                             'YunCheng'],'DeZhou':['LeLing','Nanjing']},
        'HeNan': {'xinyang': ['JiNing',
                               'YunCheng'], 'DeZhou': ['LeLing', 'Nanjing']},
    }

    return HttpResponse(json.dump(region_dic))