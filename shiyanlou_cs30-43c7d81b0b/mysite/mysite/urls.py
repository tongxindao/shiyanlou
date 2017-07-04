"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/', views.hello, name="hello"),
    url(r'^now/$', views.current_datetime, name="current_datetime"),
    url(r'^now/plus/(\d{1,2})/$', views.hours_ahead, name="hours_ahead"),
    url(r'^nowtemplate/$', views.current_datetime_template, name="current_datetime_template"),
    url(r'^datetemplate/$', views.datetime_template, name="datetime_template"),
    url(r'^templatedate/$', views.template_datetime, name="templatedate"),
    url(r'^books/', include('books.urls')),   
]
