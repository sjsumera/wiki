from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("new", views.new, name="new"),
    path("newsubmit", views.newsubmit, name="newsubmit"),
    path("edit", views.edit, name="edit"),
    path("saveedit", views.saveedit, name="saveedit"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random")
]
