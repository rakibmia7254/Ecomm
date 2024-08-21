from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.Search.as_view(), name="search"),
    path("subscribe/", views.subscribe, name="subscribe"),
]