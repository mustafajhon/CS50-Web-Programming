from ast import Pass
from logging import exception
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from flights.forms import NewPassengerForm
from flights.models import Flight, Passenger



# Create your views here.
def index(request):
    return render(request, "flights/index.html",{"flights":Flight.objects.all})

def flight (request,flight_id):
    flight = Flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", { 
        "flight": flight, 
        "passengers":flight.passengers.all()

        }  )

def book(request, flight_id):
    if request.method =="POST":
        if "passengerType" in request.POST:
            passengerTypeVal = request.POST["passengerType"]
            return HttpResponse({"passengerTypeVal":passengerTypeVal})
        else:
            #flight = Flight.objects.get(pk=flight_id)
            flight_id2 = int(request.POST["flight_id"])
            flight = Flight.objects.get(pk=flight_id2)
            try:
                passenger= Passenger.objects.get(pk=int(request.POST["passenger"]))
            except KeyError:
                passenger = Passenger.objects.create(first = request.POST["first"],last = request.POST["last"])

            #passenger = Passenger(request.POST)
            passenger.flights.add(flight)
            #return HttpResponseRedirect(reverse("flight",args=(flight_id)))
            return HttpResponseRedirect(reverse("flight",args=(flight_id2,)))
    else:
        flight = Flight.objects.get(pk=flight_id)
        
        return render(request, "flights/book.html",{
            "flight": flight, 
            "newPassengerForm":NewPassengerForm(),
            "non_passengers": Passenger.objects.exclude(flights = flight).all(),
            "passengerTypeVal":0
            })