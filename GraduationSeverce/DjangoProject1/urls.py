from django.conf.urls import url
from django.contrib import admin
from DjangoProject1 import views
urlpatterns = [
    #url(r'^login/',views.Login),
   # url(r'^index/', views.Index),
   # url(r'^auth/$',views.Auth),
    #url(r'^getRegion/$',views.Menu),

    #url(r'^userlist/',views.List)
    #url(r'^userlist/(\d*)', views.List),
    url(r'^index/(\d*)',views.List),
    url(r'^home/username(\w+)password(.+)/$',views.Home),
    #url(r'^(?P<view>\w*)/(?P<index>\d*)', views.List, {'view': 'list','id':1})
]
