
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:userpage>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit", views.edit, name="edit"),
    path(r"^showPostLikes/$",views.showPostLikes, name="showPostLikes"),
    path(r"^addPostLike/$",views.addPostLike, name="addPostLike"),

]
