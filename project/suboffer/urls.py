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
from project.suboffer.views import *
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required

urlpatterns = [
    # Suboffer
    path('list/',SubOfferListView.as_view(),name='suboffer_list'),
    path('<int:pk>/view/',SubOfferDetailView.as_view(),name='suboffer_view'),
    path('<int:pk>/delete/',login_required(SubOfferDeleteView.as_view(),login_url=reverse_lazy('cubasells:login')),name='suboffer_delete'),
    path('<int:pk>/update/',login_required(SubOfferUpdateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='suboffer_update'),

]
