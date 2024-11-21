from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import user_login
from django.urls import path
from .views import custom_logout


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('create/', views.create_form, name='create_form'),
    path('list/', views.form_list, name='form_list'),
    path('verify/<int:form_id>/', views.verify_form, name='verify_form'),
    path('edit/<int:form_id>/', views.edit_form, name='edit_form'),
    path('revert/<int:form_id>/<int:version_number>/', views.revert_version, name='revert_version'),
    path('send/<int:form_id>/', views.send_form, name='send_form'),
    path('send_to_manager/<int:form_id>/<int:manager_id>/', views.send_form_to_manager, name='send_form_to_manager'),
    path('login/', user_login, name='login'),
    path('managers/', views.user_list, name='user_list'),  # URL for your manager list view
    path('assigned-forms/', views.assigned_forms_view, name='assigned_forms'),
    path('forms/assigned-to-manager/', views.forms_assigned_to_manager, name='forms_assigned_to_manager'),
    path('logout/', custom_logout, name='logout'),  # Add this path with the name 'logout'
    path('form/<int:form_id>/', views.form_detail, name='form_detail'),
    path('my-forms/', views.my_forms, name='my_forms'),  # Define the 'my_forms' route


    




]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)