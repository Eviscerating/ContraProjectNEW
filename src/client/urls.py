from django.urls import path 
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='client-dashboard'),
    path('browse-articles/', views.browse_articles, name='browse-articles'),
    path('subscribe-plan/', views.subscribe_plan, name='subscribe-plan'),
    path('update-user/', views.update_user, name = 'update-client'),
    
    path('create-subscription/<str:sub_id>/<str:plan_code>', 
         views.create_subscription, 
         name = 'create-subscription'
    ),
    path('cancel-subscription/<int:id>', 
         views.cancel_subscription, 
         name = 'cancel-subscription'
    ),
    path('update-subscription/<int:id>', 
         views.update_subscription, 
         name = 'update-subscription'
    ),
    
    path('update-subscription-confirmed/', 
         views.update_subscription_confirmed, 
         name = 'update-subscription-confirmed'
    ),
    path('delete-user/', views.delete_user, name='client-delete-user'),
    path('change-password/', views.change_password, name='client-change-password'),
]