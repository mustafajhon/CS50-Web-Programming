from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import NewTaskForm

# tasks=["foo","bar","baz"]
# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    if request.method == "POST":
        form = request.POST.getlist('taskList')

        request.session["tasks"].remove(form)

    else:            
        return render(request,"tasks/index.html",{
            "tasks":request.session["tasks"]
        })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["newTask"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request,"tasks/add.html",{"form":form})

    return render(request,"tasks/add.html",{"form":NewTaskForm()})


def delete(request,item_id=None):
    post_to_delete=Post.objects.get(id=item_id)
   
    post_to_delete.delete()
    return HttpResponseRedirect(reverse("tasks:index"))