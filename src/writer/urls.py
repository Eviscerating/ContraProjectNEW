from django.urls import path 
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='writer-dashboard'),
    path('create-article/', views.create_article, name='create-article'),
    path('my-articles/', views.my_articles, name='my-articles'),
]