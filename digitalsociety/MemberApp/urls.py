"""digitalsociety URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    #path('', views.home, name='home')
    path('m-dashboard/',views.m_dashboard,name='m-dashboard'),
    path('m_all_members/',views.m_all_members,name='m_all_members'),
    path('m-profie/', views.m_profile, name="m-profile"),
    path('upload-pic/', views.upload_pic, name='upload-pic'),
    path('m-add-complain/', views.m_add_complain, name='m-add-complain'),
    
    path('m-all-notice/',views.m_all_notice,name='m-all-notice'),
    path('m-all-notice-details/<int:pk>/',views.m_all_notice_details,name='m-all-notice-details'),    
    path('m-all-event/',views.m_all_event,name='m-all-event'),
    path('m-all-event-details/<int:pk>/',views.m_all_event_details,name='m-all-event-details'),
    
    path('like-notice/', views.like_notice, name='like-notice'),
    path('dislike-notice/', views.dislike_notice, name='dislike-notice'),
    path('like-event/', views.like_event, name='like-event'),
    path('dislike-event/', views.dislike_event, name='dislike-event'),
    
    path('all-maintenance/',views.all_maintenance,name='all-maintenance'),
    path('initiate_payment/<int:pk>',views.initiate_payment,name="initiate_payment"),
    path('callback/',views.callback,name="callback"),

]

