"""fault_report_system01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from knowlage01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^app02/',include('app02.urls')),

    url(r'^check_code/',views.check_code),
    url(r'^all/(?P<type_id>\d+)/',views.index),
    url(r'^login/',views.login),
    url(r'register/',views.register),
    url(r'register1/',views.register1),
    url(r'exit/',views.exit),

    url(r'^admin.html$',views.admin),
    url(r'^admin-(?P<type>\d+)-(?P<classfiy_id>\d+)-(?P<article_tag__tag_id>\d+).html$',views.admin),

    url(r'^new_article.html$',views.new_article),
    url(r'^upload_img.html$',views.upload_img),
    url(r'^see_article.html$',views.see_article),


    url(r'^up.html$',views.up),
    url(r'^comment.html$',views.comment),
    url(r'^(?P<site>\w*).html$',views.home,name='index'),
    url(r'^(?P<site>\w+)/(?P<typename>\d+).html$',views.article,name='article'),
    url(r'^(?P<site>\w+)/(?P<type>((tag)|(classfiy)|(datetime)))/(?P<typename>\w+-*\w*).html$',views.home,name='filter'),



    url(r'^',views.index),
]
