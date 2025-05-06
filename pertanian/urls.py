from django.urls import path
from . import views

app_name = 'pertanian'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plants/', views.plant_list, name='plant_list'),
    path('plants/create/', views.plant_create, name='plant_create'),
    path('plants/<int:pk>/', views.plant_detail, name='plant_detail'),
    path('fields/', views.field_list, name='field_list'),
    path('fields/create/', views.field_create, name='field_create'),
    path('fields/<int:pk>/', views.field_detail, name='field_detail'),
    path('plantings/', views.planting_list, name='planting_list'),
    path('plantings/create/', views.planting_create, name='planting_create'),
    path('plantings/<int:pk>/', views.planting_detail, name='planting_detail'),
    path('plantings/<int:pk>/update-status/', views.planting_update_status, name='planting_update_status'),
]