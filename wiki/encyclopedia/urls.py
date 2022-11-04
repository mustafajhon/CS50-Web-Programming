from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("searchResults/<str:searchedTitle>", views.searchResults, name="searchResults"),
    path("newPage", views.newPage, name="newPage"),
    path("edit/<str:title>", views.edit, name="editPage"),
    path("randomPage", views.random, name="randomPage")
]
