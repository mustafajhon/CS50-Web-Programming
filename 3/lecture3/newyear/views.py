from datetime import date

from django.shortcuts import render

# Create your views here.

def index(request):
    
    if( date.today().day ==1 and date.today().month ==1):
        checkedDate = True
    else:
        checkedDate = False

    return render(request,"newyear/index.html",{"checkedDate":checkedDate})
