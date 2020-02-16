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

    # Image
    path('image/list/',ImageListView.as_view(),name='image_list'),
    path('image/view/<int:pk>/',ImageDetailView.as_view(),name='image_view'),
    path('image/create/',ImageCreateView.as_view(),name='image_create'),
    path('image/delete/<int:pk>/',ImageDeleteView.as_view(),name='image_delete'),
    path('image/update/<int:pk>/',ImageUpdateView.as_view(),name='image_update'),
    
    # Tag
    path('tag/list/',TagListView.as_view(),name='tag_list'),
    path('tag/view/<int:pk>/',TagDetailView.as_view(),name='tag_view'),
    path('tag/create/',TagCreateView.as_view(),name='tag_create'),
    path('tag/delete/<int:pk>/',TagDeleteView.as_view(),name='tag_delete'),
    path('tag/update/<int:pk>/',TagUpdateView.as_view(),name='tag_update'),

    # User
    path('user/',login_required(user_index,login_url=reverse_lazy('cubasells:login')),name='user_index'),
    path('user/create/',UserCreateView.as_view(),name='user_create'),

    # Store
    path('store/',store_index,name='store_index'),
    path('store/list/',StoreListView.as_view(),name='store_list'),
    path('store/create/',login_required(StoreCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_create'),
    path('store/<int:pk>/delete/',login_required(StoreDeleteView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_delete'),
    path('store/<int:pk>/update/',login_required(StoreUpdateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_update'),

    path('store/<int:pk>/',StoreDetailView.as_view(),name='store_view'),
    path('store/<int:store_id>/product/',ProductListView.as_view(),name='store_product_list'),
    path('store/<int:store_id>/product/create/',login_required(ProductCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_product_create'),

    path('store/<int:store_id>/offer/',OfferListView.as_view(),name='store_offer_list'),
    path('store/<int:store_id>/offer/create/',login_required(OfferCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_offer_create'),    

    path('store/<int:store_id>/suboffer/list/',login_required(SubOfferListView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_suboffer_list'),
    path('store/<int:store_id>/suboffer/create/',login_required(SubOfferCreateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='store_suboffer_create'),
    
    # Product
    path('product/',ProductListView.as_view(),name='product_list'),
    path('product/<int:pk>/view/',ProductDetailView.as_view(),name='product_view'),
    path('product/<int:pk>/delete/',login_required( ProductDeleteView.as_view(),login_url=reverse_lazy('cubasells:login')),name='product_delete'),
    path('product/<int:pk>/update/',login_required( ProductUpdateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='product_update'),

    # Offer
    path('offer/',OfferListView.as_view(),name='offer_list'),
    path('offer/<int:pk>/view/',OfferDetailView.as_view(),name='offer_view'),
    path('offer/<int:pk>/delete/',login_required(OfferDeleteView.as_view(),login_url=reverse_lazy('cubasells:login')),name='offer_delete'),
    path('offer/<int:pk>/update/',login_required(OfferUpdateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='offer_update'),
    
    # Suboffer
    path('suboffer/list/',SubOfferListView.as_view(),name='suboffer_list'),
    path('suboffer/<int:pk>/view/',SubOfferDetailView.as_view(),name='suboffer_view'),
    path('suboffer/<int:pk>/delete/',login_required(SubOfferDeleteView.as_view(),login_url=reverse_lazy('cubasells:login')),name='suboffer_delete'),
    path('suboffer/<int:pk>/update/',login_required(SubOfferUpdateView.as_view(),login_url=reverse_lazy('cubasells:login')),name='suboffer_update'),

]
