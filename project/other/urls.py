"""Cubasells URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from project.other.views import *
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required

urlpatterns = [
    # Image
    path('images/list/',ImageListView.as_view(),name='image_list'),
    path('images/view/<int:pk>/',ImageDetailView.as_view(),name='image_view'),
    path('images/create/',ImageCreateView.as_view(),name='image_create'),
    path('images/delete/<int:pk>/',ImageDeleteView.as_view(),name='image_delete'),
    path('images/update/<int:pk>/',ImageUpdateView.as_view(),name='image_update'),
    
    # Tag
    path('tag/list/',TagListView.as_view(),name='tag_list'),
    path('tag/view/<int:pk>/',TagDetailView.as_view(),name='tag_view'),
    path('tag/create/',TagCreateView.as_view(),name='tag_create'),
    path('tag/delete/<int:pk>/',TagDeleteView.as_view(),name='tag_delete'),
    path('tag/update/<int:pk>/',TagUpdateView.as_view(),name='tag_update'),
]
