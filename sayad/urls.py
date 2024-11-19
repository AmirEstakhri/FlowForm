from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL for login
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  
    
    # URLs for forms
    path('forms/', views.form_list, name='forms'),  # List of forms
    path('create_form/', views.create_form, name='create_form'),
    path('form_list/', views.form_list, name='form_list'),
    path('send_form/<int:form_id>/', views.send_form, name='send_form'),

    # Profile URLs
    path('userprofile/', include('userprofile.urls')),  # Include the userprofile app's URLs
    
    # Admin URL
    path('admin/', admin.site.urls),
    
    # Include the URLs of the 'app' app, should be placed at the end
    path('', include('app.urls')),  # This links the app's URLs (homepage and others)
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
