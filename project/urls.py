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
from project.views import *
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required

urlpatterns = [
    path('',index,name='index'),
    path('success/',success_view,name='success'),
    path('login/',MyLoginView.as_view(),name='login'),
    path('logout/',MyLogoutView.as_view(),name='logout'),

    # User
    path('user/',login_required(user_index,login_url=reverse_lazy('cubasells:login')),name='user_index'),
    path('user/create/',UserCreateView.as_view(),name='user_create'),
    path('user/<int:pk>/delete/',login_required(UserDeleteView.as_view(),login_url=reverse_lazy('cubasells:login')),name='user_delete'),
    path('user/<int:pk>/update/',login_required(UserUpdateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='user_update'),
]