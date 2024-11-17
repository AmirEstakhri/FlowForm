"""
URL configuration for sayad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# sayad/sayad/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views  # Import views from the current module


urlpatterns = [
    # URL for login
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  
    
    # URLs for forms
    path('forms/', views.form_list, name='forms'),  # List of forms
    path('create_form/', views.create_form, name='create_form'),
    path('form_list/', views.form_list, name='form_list'),
    path('send_form/<int:form_id>/', views.send_form, name='send_form'),
    
    # Admin URL
    path('admin/', admin.site.urls),
    
    # Include the URLs of the 'app' app, should be placed at the end
    path('', include('app.urls')),  # This links the app's URLs (homepage and others)

]
