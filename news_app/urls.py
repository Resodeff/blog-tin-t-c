from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("post/new/", views.post_create, name="post_create"),
    path("post/<int:id>/", views.post_detail, name="post_detail"),
    path("POST/<int:id>/", views.post_detail),
    path("post/<int:id>/edit/", views.post_update, name="post_update"),
    path("post/<int:id>/delete/", views.post_delete, name="post_delete"),
]
