from django.urls import path
from .import views

urlpatterns = [
    path("",views.index, name="index"),
    path("pawel",views.pawel, name ="pawel"),
    #path("<str:username>", views.username, name = "username")
    path("<str:name>", views.greet, name = "greet")
]
