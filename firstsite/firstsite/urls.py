"""firstsite URL Configuration

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
# user django comments system(r'^comments/', include('django.contrib.comments.urls')),
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from firstapp.views import (Help, identification, keeper, main, multi, search, searchResult, single, sitterHelp, sitterInfo, chatroom)
from firstapp.views import (
    Help, forgetpassword, identification, keeper, main, multi, order, pmain,
    search, searchResult, single, sitterHelp, sitterInfo,newarticle,
    identification2,forgetpassword2,forgetpassword3,denglu,mainin,pmess,zhuce,pingjia,digg)


#url(r'^comments/', include('django_comments.urls')),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', main, name='main'),
    path('mainin/', mainin, name='mainin'),
    path('search/', search, name='search'),
    path('searchResult/', searchResult, name='searchResult'),
    path('sitterInfo/', sitterInfo, name='sitterInfo'),
    path('Help/', Help, name='Help'),
    path('sitterHelp/', sitterHelp, name='sitterHelp'),
    path('identification/', identification, name='identification'),
    path('keeper/', keeper),
    path('single/', single, name='single'),
    path('multi/', multi, name='multi'),
    path('forgetpassword/', forgetpassword, name='forgetpassword'),
    path('order/', order, name='order'),
    path('pmain/', pmain, name='pmain'),
    path('newarticle/', newarticle, name='newarticle'),
    path('identification2/', identification2, name='identification2'),
    path('forgetpassword2/', forgetpassword2, name='forgetpassword2'),
    path('forgetpassword3/', forgetpassword3, name='forgetpassword3'),
    path('denglu/', denglu, name='denglu'),
    path(r'chat/<u_id>/<f_id>/', chatroom, name='chat'),
    path('pmess/', pmess, name='pmess'),
    path('zhuce/', zhuce , name='zhuce'),
    path('pingjia/', pingjia , name='pingjia'),
    path('digg/', digg , name='digg'),
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATICFILES_DIRS)

'''
from django.conf.urls import url
from django.contrib import admin

from firstapp.views import first_try, index'''
