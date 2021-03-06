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
from project.cart.views import *
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required

urlpatterns = [
    path('list/',login_required(ShoppingOfferListView.as_view(),login_url=reverse_lazy('cubasells:login')),name='cart_list'),
    path('create/<int:offer_id>',login_required(ShoppingOfferCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='cart_create'),
    path('delete/<int:pk>',login_required(ShoppingOfferDeleteView.as_view(),login_url=reverse_lazy('cubasells:login')),name='cart_delete'),
    path('update/<int:pk>',login_required(ShoppingOfferUpdateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='cart_update'),
]
