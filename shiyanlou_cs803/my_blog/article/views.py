from django.shortcuts import render
from django.http import HttpResponse
from article.models import Article
from datetime import datetime
from django.http import Http404
from django.views.decorators.cache import cache_page

# Create your views here.
def home(request):
    post_list = Article.objects.all()
    return render(request, 'home.html', {'post_list': post_list})

@cache_page(60 * 15)
def detail(request, my_args):
    print(my_args)
    post = Article.objects.get(id=int(my_args))
    return render(request, 'post.html', {'post': post})
