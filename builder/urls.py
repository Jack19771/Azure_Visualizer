from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/resources/', views.get_resources, name='get_resources'),
    path('api/templates/', views.get_resource_templates, name='templates'),
]