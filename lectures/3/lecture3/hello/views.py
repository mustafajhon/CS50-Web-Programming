from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def pawel(request):
    return HttpResponse("Hello, Pawel!")

#def username(request,username):
#    return HttpResponse("Hello, " + username.capitalize())


def greet(request,name):
    return render(request,"hello/greet.html",{"name": name.capitalize()})