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
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required

from project.store.views import *
from project.product.views import *
from project.offer.views import *
from project.suboffer.views import *

urlpatterns = [
    # Store
    path('',store_index,name='store_index'),
    path('list/',StoreListView.as_view(),name='store_list'),
    path('create/',login_required(StoreCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_create'),
    path('<int:pk>/delete/',login_required(StoreDeleteView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_delete'),
    path('<int:pk>/update/',login_required(StoreUpdateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_update'),

    path('<int:pk>/',StoreDetailView.as_view(),name='store_view'),
    path('<int:store_id>/product/',ProductListView.as_view(),name='store_product_list'),
    path('<int:store_id>/product/create/',login_required(ProductCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_product_create'),

    path('<int:store_id>/offer/',OfferListView.as_view(),name='store_offer_list'),
    path('<int:store_id>/offer/adm_create/',login_required(OfferCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_offer_create'),    

    path('<int:store_id>/suboffer/list/',login_required(SubOfferListView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_suboffer_list'),
    path('<int:store_id>/suboffer/adm_create/',login_required(SubOfferCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_suboffer_create'),
    
    # Test
    path('<int:store_id>/offer/create',login_required(StoreUserCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_offer_create_user'),
    path('tags/', StoreTagFilterView.as_view(),name='store_tags_view'),
    
]
