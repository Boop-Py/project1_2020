from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("<str:title>/edit/", views.edit, name="edit"),
    path("todolist", views.todolist),
    path("random", views.randomise, name="randomise"),
    path("<str:title>/", views.result, name="title")
    
]
 