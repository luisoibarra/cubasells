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
    form_class = SelectAccountForm

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Cart__myuser__id = self.request.user.id)
        return queryset
    
    def get_context_data(self, object_list=None,**kwargs):
        context = super().get_context_data(object_list=object_list,**kwargs)
        try:
            context['form']=kwargs['form3']
        except KeyError:
            pass
        return context
    
    @auth    
    def get(self,request,*args, **kwargs):
        self.object = None
        form_order = self.get_form(request)
        form = self.form_class(BankAccount.objects.all().filter(MyUser__id=self.request.user.id),request.GET)
        
        if form_order.is_valid():
            form_data = self.get_form_cleaned_data(form_order)
            self.get_ordering(form_data)
            self.object_list = self.get_queryset()
            form_filter = self.form_filter(request.GET,self.object_list)
            self.object_list = form_filter.qs
            context = self.get_context_data(object_list=self.object_list,form=form_order,form2=form_filter,form3=form,**kwargs)
        else:
            context = self.get_context_data(form=form_order,form2=form_filter, form3=form,**kwargs)
            return render(request,self.template_name,context)
        
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        return self.render_to_response(context)
       
    
    @auth    
    def post(sef,request,*args, **kwargs):
        self.object = None
        form_order = self.get_form(request,False)
        form = self.form_class(BankAccount.objects.all().filter(MyUser__id=self.request.user.id),request.POST)
        
        if form_order.is_valid():
            form_data = self.get_form_cleaned_data(form_order)
            self.get_ordering(form_data)
            self.object_list = self.get_queryset()
            form_filter = self.form_filter(request.POST,self.object_list)
            self.object_list = form_filter.qs
            context = self.get_context_data(object_list=self.object_list,form=form_order,form2=form_filter,form3=form,**kwargs)
            if not form_filter.is_valid():
                return render(request,self.template_name,context)
            if not form.is_valid():
                return render(request,self.template_name,context)
            elif '_buy' in request.POST:
                # Comprar los elementos del carrito
                pass
            
        else:
            context = self.get_context_data(form=form_order,form2=form_filter,form3=form,**kwargs)
            return render(request,self.template_name,context)
        
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        return self.render_to_response(context)


class ShoppingOfferCreateView(AuthenticateCreateView):
    model = ShoppingOffer
    template_name = "cart/create.html"
    permission = 'project.add_shoppingoffer'
    success_url = reverse_lazy('cart:cart_list')
    form_class = ShoppingOfferCreateForm
    
    @auth
    def post(self,request,*args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None
        form = self.get_form()
        try:
            offer = Offer.objects.get(id=kwargs['offer_id'])
            form.instance.Offer = offer
            form.instance.Cart = request.user.myuser.Cart
            not_available = []
            if form.is_valid():
                for sub_offer in offer.Suboffer.all():
                    if sub_offer.Product_offer.Store_Amount < form.instance.Amount * sub_offer.Amount:
                        not_available.append(sub_offer)
                if not_available:
                    extra = {'error': "Not enough products in store: " + " ".join([str(x)for x in not_available])}
                    context = self.get_context_data(**extra)
                    return render(request, 'error.html', context)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        except ObjectDoesNotExist:
            extra = {'error':'Offer doesnt exist'}
            self.update_extra_context(extra)
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["offer"] = Offer.objects.all().get(id=self.kwargs['offer_id'])
        return context


class ShoppingOfferUpdateView(AuthenticateUpdateView):
    model = ShoppingOffer
    template_name = "update.html"
    permission = 'project.change_shoppingoffer'
    success_url = reverse_lazy('cart:cart_list')
    form_class = ShoppingOfferCreateForm
    
    def other_condition(self, request, *args, **kwargs):
        if request.user.id == self.model.objects.get(id=kwargs['pk']).Cart.myuser.id:
            return True
        self.error_msg += " Only the owner can update the shopping offer"

class ShoppingOfferDeleteView(AuthenticateDeleteView):
    model = ShoppingOffer
    template_name = "delete.html"
    permission = 'project.delete_shoppingoffer'
    success_url = reverse_lazy('project:success')
    
    def other_condition(self, request, *args, **kwargs):
        if request.user.id == self.model.objects.get(id=kwargs['pk']).Cart.myuser.id:
            return True
        self.error_msg += " Only the owner can delete the shopping offer"