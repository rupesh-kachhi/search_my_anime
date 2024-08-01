from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.login, name="login"),
     path("signup/", views.signup, name="signup"),
    path("anime/id=<int:anime_id>", views.index_two, name="anime-view"),
    path("api-proxy/<str:search_query>", views.index_three, name="api-proxy")
]