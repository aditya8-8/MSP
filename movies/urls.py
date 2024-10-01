from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin, name='admin'),
    path('', views.home, name='home'),
    path('movie/<int:id>/', views.details, name='details'),
    path('search/', views.search, name='search'),
    path('predict/', views.predict, name='predict'),

]