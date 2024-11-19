from django.urls import path
from . import views

app_name = 'userprofile'  # Add this line to define the namespace

urlpatterns = [
    path('', views.view_profile, name='view_profile'),  # Default profile view
    path('view/', views.view_profile, name='view_profile'),
    path('update-picture/', views.update_profile_picture, name='update_profile_picture'),
]
