from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.



from django.shortcuts import render_to_response

from DjangoProject1   import  models

data = ['lishihsung','wangfanhai','wanghah']
def List(request,index):
    if index:
        print 'lishishuang',index
        result = data[int(index)]
        return HttpResponse('<h1>'+result+'</h1>')
    result = '<br/>'.join(data)
    return HttpResponse('<h1>'+result+'</h1>')




def Home(request,username,password):
    print username,password
    p = models.Personpaiming(Name = username,Gender=password)
    p.save()

    return render_to_response('index.html',{'key1':'lihsishuang'})