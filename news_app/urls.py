
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('POST/<int:id>/', views.post_detail, name='post_detail'),
    #code cuar Truyền ở đây
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    #==============================================================
]