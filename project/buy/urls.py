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


from django.urls import path,include
from project.buy.views import *
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required

from project.buy.buy import *


urlpatterns = [
    path('accounts/',login_required(BankAccountListView.as_view(),login_url=reverse_lazy('cubasells:login')),name='bankaccount_list'),
    path('accounts/<int:pk>/delete/',login_required(BankAccountDeleteView.as_view(),login_url=reverse_lazy('cubasells:login')),name='bankaccount_delete'),
    path('accounts/<int:pk>/update/',login_required(BankAccountUpdateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='bankaccount_update'),
    path('accounts/create/',login_required(BankAccountCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='bankaccount_create'),
    path('cart/',login_required(BuyCartView.as_view(),login_url=reverse_lazy('cubasells:login')),name='buy_cart'),
]
