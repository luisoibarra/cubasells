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
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import login_required
# from project import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(('project.urls','project'),'cubasells')),
    path("store/",include(('project.store.urls','store'),'store')),
    path("offer/",include(('project.offer.urls','offer'),'offer')),
    path("suboffer/",include(('project.suboffer.urls','suboffer'),'suboffer')),
    path("product/",include(('project.product.urls','product'),'product')),
    path('other/',include(('project.other.urls','other'),'other')),
    path('cart/',include(('project.cart.urls','cart'),'cart')),
    path('buy/',include(('project.buy.urls','buy'),'buy')),
    path('bank/',include(('project.bank.urls','bank'),'bank')),
    path('auction/',include(('project.auction.urls','auction'),'auction')),
    path('chat/',include(('project.chat.urls','chat'),'chat')),
    
]
