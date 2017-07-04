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
from . import views

urlpatterns = [
    # url(r'^form/', views.form, name='form'),
    url(r'^investigate/', views.investigate, name='investigate'),
    url(r'^userlogin/', views.user_login, name='user_login'),
    url(r'^userlogout/', views.user_logout, name='user_logout'),
    url(r'^useronly/', views.user_only, name='user_only'),
    url(r'^diffresponse/', views.diff_response, name='diff_response'),
    url(r'^namecheck/', views.name_check, name='name_check'),
    url(r'^specificuser/', views.specific_user, name='specific_user'),
    url(r'^register/', views.register, name="register"),
]
