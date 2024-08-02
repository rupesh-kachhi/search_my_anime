from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.login, name="login"),
    path("logout/",views.logout, name="lgout"),
    path("signup/", views.signup, name="signup"),
    path("postSignIn", views.postSignIn, name="postSignIn"),
    path("postSignUp", views.postSignUp, name="postSignUp"),
    path("anime/id=<int:anime_id>", views.index_two, name="anime-view"),
    path("api-proxy/<str:search_query>", views.index_three, name="api-proxy")
]