
from random import choices
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from . import util

def index(request):
    
    entriesList = util.list_entries()
    if request.method == "POST":
        searchedTitle = request.POST['q']
        if util.search_entry(searchedTitle,entriesList):
            return HttpResponseRedirect(reverse('title',args = (searchedTitle,)))
        else:           
            return HttpResponseRedirect(reverse('searchResults',args = (searchedTitle,)))
     

    else:
        return render(request, "encyclopedia/index.html", {    
            "entries": entriesList
        })


def title(request, title):
    entry = util.get_entry(title)

    return render(request, "encyclopedia/title.html", {
        "entry":entry, "title":title
    })

def searchResults(request, searchedTitle):
    entriesList = util.list_entries()
    searchResultsSet = util.search_subString(searchedTitle,entriesList)
    return render(request, "encyclopedia/searchResults.html", {
        "foundSet":searchResultsSet,"title":searchedTitle
    })

def newPage(request):
    if request.method == "POST":
        newTitle = request.POST['title']
        newDescription = request.POST['description']
        try:
            open(f"entries/{newTitle}.md","x").close
        except FileExistsError: 
            return render(request, "encyclopedia/newPage.html",{"error":"File "+ newTitle +  " already Exists"})
        else:
            content = "#" + newTitle +"\n" + newDescription
            util.save_entry(newTitle,content)
            return HttpResponseRedirect(reverse('title',args = (newTitle,)))           

    return render(request, "encyclopedia/newPage.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST['description']
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse('title',args = (title,))) 
    
    entry = util.get_entry(title)

    return render(request, "encyclopedia/editPage.html", {
        "entry":entry, "title":title
    })


def random(request):  
    entriesList = util.list_entries()
    randomChoice = choices(entriesList)
    return HttpResponseRedirect(reverse('title',args = (randomChoice),))