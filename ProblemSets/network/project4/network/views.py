from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,NewPost,PostLike
from .forms import NewPostForm
from datetime import datetime

def index(request,userpage='authenticatedUser'):
    if request.method == "POST":
        newPost = NewPost(newPost=request.POST["newPost"], user=request.user, username= request.user.username, likes = 0, postDate = datetime.now())
        #newPost = NewPost(newPost=request.POST["newPost"])
        newPost.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        if userpage == 'authenticatedUser':
            username=request.user.username
            userpage = username
        elif User.objects.get(username=userpage):
            username = userpage
        newPost = NewPostForm()        
        posts = NewPost.objects.all().filter(username=username)
        return render(request, "network/index.html",{'newPost':newPost,'posts':posts, 'userpage':userpage})
        


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        birthday = request.POST["birthday"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password,birthday)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        except ValidationError:
            return render(request, "network/register.html", {
                "message": "Please fill all necessary data"
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def edit(request):
    

    if request.method == "POST":
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        birthday = request.POST["birthday"]
        email = request.POST["email"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to update data

        user = User.objects.get(username=request.user)
        user.password = password;
        user.confirmation = confirmation;
        user.email=email;
        user.birthday = birthday;
        user.save()
        return HttpResponseRedirect(reverse("edit"))
    else:
        user = request.user
        return render(request, "network/edit.html",{"user":user})

def showPostLikes(request):
    if NewPost.objects.exists():
        post_id = request.GET['post_id']
        postLikes =  PostLike.objects.get(post=post_id)
        print(postLikes)

def addPostLike(request):
    user = request.user
    #add new like to the post model
    post_id = request.GET['post_id'] 
    post =  NewPost.objects.get(post=post_id)
    post.likes = post.likes+1
    post.save()
    print(post.likes)
    #add new user in post Like model
    postLikes =  PostLike.objects.get(post=post_id)
    postLikes.user.add(user.id)
    postLikes.save()
    print(postLikes.user.all())
    
    return HttpResponse(post.likes)



def search(request,searchedEntry):
    if request.method == "POST":
        #searchedEntry = request.POST['q']
        filteredEntriesList = User.objects.filter(username__contains=searchedEntry)
        return render(request, "network/search.html", {
        "entries":filteredEntriesList,"query":searchedEntry
    })
    

