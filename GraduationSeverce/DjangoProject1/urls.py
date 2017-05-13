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
   # url(r'^index/(\d*)',views.Login()),
    url(r'^login',views.login),
    url(r'^register',views.register),
    url(r'^homeData', views.homeData),
    url(r'^allBallMessage', views.allBallMessage),
    url(r'^resertBallTable',views.resertBallTable),
    url(r'^resertBallMessage', views.resertBallMessage),
    url(r'^ballEnroll', views.ballEnroll),
    url(r'^searchBallEnroll', views.searchBallEnroll),
    url(r'^cancelBallEnroll', views.cancelBallEnroll),
    url(r'^allAboutBall', views.allAboutBall),
    url(r'^deleteAboutBall', views.deleteAboutBall),
    url(r'^auditAbout', views.auditAbout),
    url(r'^postUserImage', views.postUserImage)

    #url(r'^(?P<view>\w*)/(?P<index>\d*)', views.List, {'view': 'list','id':1})
]
