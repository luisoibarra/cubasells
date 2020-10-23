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
from project.chat.views import *
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required

urlpatterns = [
    # Chat
    path('',ChatedUserListView.as_view(),name='chat_index'),
    path('<int:recv>/',ChatedUserListView.as_view(),name='chat_list'),
    path('view/<int:pk>/',ChatDetailView.as_view(),name='chat_view'),
    path('create/<int:recv>',ChatCreateView.as_view(),name='chat_create'),
    path('delete/<int:pk>/',ChatDeleteView.as_view(),name='chat_delete'),
    path('update/<int:pk>/',ChatUpdateView.as_view(),name='chat_update'),
  
]
