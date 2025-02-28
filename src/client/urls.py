from django.urls import path 
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='client-dashboard'),
    path('browse-articles/', views.browse_articles, name='browse-articles'),
    path('subscribe-plan/', views.subscribe_plan, name='subscribe-plan'),
    path('update-user/', views.update_user, name = 'update-client'),
    path('create-subscription/<str:sub_id>/<str:plan>', 
         views.create_subscription, 
         name = 'create-subscription'
    ),
]