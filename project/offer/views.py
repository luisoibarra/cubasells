from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from project.models import *
from project.offer.forms import *
from project.custom.views import *
from django.contrib.auth.models import Group
from project.offer.filters import *

# Create your views here.



class OfferCreateView(AuthenticateCreateView):
    model = Offer
    template_name = "offer/create.html"
    form_class = OfferCreateForm
    success_url = reverse_lazy('store:store_index') # idealmente quiero que te deje en la tienda q le vas a agregar el producto
    permission = 'project.add_offer'
 
    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        try:
            self.form_class.base_fields['Suboffer'].queryset = SubOffer.objects.filter(Product_offer__Store__id = self.kwargs['store_id'])#forms.ModelMultipleChoiceField(queryset=Product.objects.filter(Store__id = self.kwargs['store_id']))
        except KeyError:
            context.update({'error':'Missing parameter store_id in url'})
        return context
    
    def update_extra_context(self,extra):
        if self.extra_context is None:
            self.extra_context = extra
        else:
            self.extra_context.update(extra)
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            form = self.get_form()
            try:
                store = Store.objects.get(id=kwargs['store_id'])
                if store.Owner.id == request.user.id:
                    form.instance.Store = store
                    self.success_url = reverse_lazy('store:store_offer_list',kwargs={'store_id':store.id})
                else:
                    extra = {'error':'User not authorized to create an offer in this store, must be its owner'}
                    self.update_extra_context(extra)
                    return self.form_invalid(form)
            except ObjectDoesNotExist:
                extra = {'error':'Store doesnt exist'}
                self.update_extra_context(extra)
                return self.form_invalid(form)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def other_condition(self, request,*args, **kwargs):
        if 'store_id' in kwargs:
            user = request.user
            store = Store.objects.get(id=kwargs['store_id'])
            return store.Owner.id == user.id
        else:
            return True

class OfferListView(FilterOrderAuthenticateListView):
    model = Offer
    template_name = "offer/list.html"
    paginate_by = 5
    permission = 'project.view_offer'
    form_order = OfferOrderForm
    form_filter = OfferFilter
    
    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            try:
                queryset = self.model.objects.filter(Store__id=self.kwargs['store_id'])
            except KeyError:
                queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

class OfferDetailView(AuthenticateDetailView):
    model = Offer
    template_name = "offer/view.html"
    permission = 'project.view_offer'

class OfferDeleteView(AuthenticateDeleteView):
    model = Offer
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_offer'
    
    def other_condition(self, request,*args, **kwargs):
        user = request.user
        offer = Offer.objects.get(id=kwargs['pk'])
        return offer.Store.Owner.id == user.id

class OfferUpdateView(AuthenticateUpdateView):
    model = Offer
    form_class = OfferCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_offer'

    def other_condition(self, request,*args, **kwargs):
        user = request.user
        offer = Offer.objects.get(id=kwargs['pk'])
        return offer.Store.Owner.id == user.id
