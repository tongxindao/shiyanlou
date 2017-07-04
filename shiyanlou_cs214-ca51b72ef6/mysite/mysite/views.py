# _*_ coding: utf-8 _*_

from django.http import HttpResponse

def first_page(request):
    return HttpResponse("<p>世界好</p>")
