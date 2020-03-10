from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from project.models import *
from project.cart.forms import *
from project.custom.views import *
from django.contrib.auth.models import Group
from project.cart.filters import *


class ShoppingOfferListView(FilterOrderAuthenticateListView):
    model = ShoppingOffer
    template_name = "cart/list.html"
    permission = 'project.view_shoppingoffer'
    form_order = ShoppingOfferOrderForm
    form_filter = ShoppingOfferFilter
 

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Cart__myuser__id = self.request.user.id)
        return queryset


class ShoppingOfferCreateView(AuthenticateCreateView):
    model = ShoppingOffer
    template_name = "cart/create.html"
    permission = 'project.add_shoppingoffer'
    success_url = reverse_lazy('cart:cart_list')
    form_class = ShoppingOfferCreateForm
    
    def post(self,request,*args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            form = self.get_form()
            try:
                offer = Offer.objects.get(id=kwargs['offer_id'])
                form.instance.Offer = offer
                form.instance.Cart = request.user.myuser.Cart
                return self.form_valid(form)
            except ObjectDoesNotExist:
                extra = {'error':'Offer doesnt exist'}
                self.update_extra_context(extra)
                return self.form_invalid(form)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["offer"] = Offer.objects.all().get(id=self.kwargs['offer_id'])
        return context


class ShoppingOfferDeleteView(AuthenticateDeleteView):
    model = ShoppingOffer
    template_name = "delete.html"
    permission = 'project.delete_shoppingoffer'
    success_url = reverse_lazy('project:success')