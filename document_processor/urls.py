"""
URL configuration for document_processor app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    
    # Document views
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<uuid:pk>/', views.document_detail, name='document_detail'),
    path('documents/<uuid:pk>/process/', views.document_process, name='document_process'),
    path('documents/<uuid:pk>/delete/', views.document_delete, name='document_delete'),
    path('documents/<uuid:pk>/download/', views.document_download, name='document_download'),
    
    # API endpoints
    path('api/documents/<uuid:pk>/process/', views.document_process_api, name='document_process_api'),
] 