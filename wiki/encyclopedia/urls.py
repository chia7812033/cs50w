from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.new_page, name="newpage"),
    path("fault=<int:state>", views.fault, name="fault"),
    path("edit", views.editpage, name="editpage"),
    path("<str:title>", views.entry, name="entry")
]
