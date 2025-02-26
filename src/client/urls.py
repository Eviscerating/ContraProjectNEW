from django.urls import path 
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='client-dashboard'),
    path('browse-articles/', views.browse_articles, name='browse-articles'),
]