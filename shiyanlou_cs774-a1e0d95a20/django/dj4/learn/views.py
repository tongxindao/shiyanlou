# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .forms import AddForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))
    else:
        form = AddForm()

    return render(request, 'index.html', {'form': form})

def home(request):
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    return render(request, 'home.html', {'TutorialList': TutorialList})

def add(request):
    a = request.GET.get('a', 0)
    b = request.GET.get('b', 0)
    a = int(a)
    b = int(b)
    c = a + b
    return HttpResponse(str(c))
