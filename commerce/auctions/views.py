from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from datetime import datetime, time
from django.contrib.auth import authenticate, login, logout,get_user
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse



from .models import Bid, Listings, User, Watchlist


def index(request):
    return render(request, "auctions/index.html", {"listings": Listings.objects.all()})

    
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method =="POST":
        
# get data from form         
        _title = request.POST["title"]
        _description = request.POST["description"]
        _imageUrl = request.POST["imageUrl"]
        _currentPrice = request.POST["currentPrice"]
        _seller = get_user(request)

# check data if are valid 
        createSet = {_title,_currentPrice}      
        for element in createSet:
            if len(element) == 0:
                return render(request,"auctions/create.html",
                {
                    "message":"Please correct Yours data"
                })

# create Listing
        Listings.objects.create(title = _title, description = _description,askingPrice = _currentPrice, imageUrl=_imageUrl,seller =_seller )    
        

    return render(request,"auctions/create.html")
    
def categories(request):

    print(Listings.objects.all().values_list())
    return render(request,"auctions/categories.html")

def watchlist(request):
    user = get_user(request)

    if request.method =="POST":        
        if "listingToWatchlist" in request.POST:
            listing = Listings.objects.get(pk=request.POST["listing_id"])
            if Watchlist.objects.filter(user = user, listing = listing).exists():
                message = "Object already on the watchlist"
                userWatchlist = Watchlist.objects.filter(user=user).all()
                return render(request,"auctions/watchlist.html",{
                    "watchlist":userWatchlist,"message":message
                })
            else:
                Watchlist.objects.create(user = user, listing = listing)
        if "removeFromWatchlist" in request.POST:
            print(request.POST["listing_id"])
            listingToDelete = Watchlist.objects.get(pk=request.POST["listing_id"])
            listingToDelete.delete()
            #Watchlist.objects.
        return HttpResponseRedirect(reverse("watchlist"))

    userWatchlist = Watchlist.objects.filter(user=user).all()
    print(userWatchlist)
    return render(request,"auctions/watchlist.html",{
        "watchlist":userWatchlist
    })


def listing(request,listing_id):    
    if request.method =="POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        
        requestedListing = Listings.objects.get(pk=listing_id)
        if float(requestedListing.currentPrice) < float(request.POST["bidPrice"]):
            requestedListing.currentPrice = request.POST["bidPrice"] 
            newBid = Bid.objects.create(bidPrice =request.POST["bidPrice"],buyer = get_user(request), listing = requestedListing )

        #return render(request,"auctions/listing.html",
        #    {
        #        "listing":requestedListing, "highest_bid":highest_bid
        #    })



    listing = Listings.objects.get(pk=listing_id)
    highest_bid = Bid.objects.filter(listing=listing).order_by('-bidPrice').first()
    print(highest_bid)
    return render(request,"auctions/listing.html",
    {
        "listing":listing, "highest_bid":highest_bid
    })