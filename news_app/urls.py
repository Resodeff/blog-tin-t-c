from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name = 'home'),
    path('POST/<int:id>/', views.post_detail, name = 'post_detail')
]

