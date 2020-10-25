from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from project.models import *
from project.offer.forms import *
from project.custom.views import *
from project.custom.forms import *
from django.contrib.auth.models import Group
from project.offer.filters import *
from project.other.forms import ImageCreateForm
from django.db.models import QuerySet, F ,Min
# from excel_response import ExcelView

# Create your views here.



class OfferCreateView(AuthenticateCreateView):
    model = Offer
    template_name = "offer/create.html"
    form_class = OfferCreateForm
    success_url = reverse_lazy('store:store_index') # idealmente quiero que te deje en la tienda q le vas a agregar el producto
    permission = 'project.add_offer'
    image_form_class = ImageCreateForm
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        try:
            context['form'].fields['Images'].queryset = Image.objects.filter(Owner__id=self.request.user.id)
            self.form_class.base_fields['Suboffer'].queryset = SubOffer.objects.filter(Product_offer__Store__id = self.kwargs['store_id'])#forms.ModelMultipleChoiceField(queryset=Product.objects.filter(Store__id = self.kwargs['store_id']))
            context['image_form'] = self.image_form_class()
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
            image_form = self.image_form_class(request.POST, request.FILES)
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
            if form.is_valid() and image_form.is_valid():
                image = image_form.save()
                form.instance.Images.add(image)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

        
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
    permission = 'project.view_offer'
    
    form_order = OfferOrderForm
    form_filter = OfferFilter
    queryset=None
    
    def anotate_available(qs_fun):
        def qs_fun(self):
            q = Offer.Suboffer.through.objects.values(
                "offer_id", "suboffer_id").annotate(
                available=F(
                    "suboffer_id__Product_offer_id__Store_Amount")/F(
                    "suboffer_id__Amount")).values("offer_id").annotate(available=Min("available"))


            queryset = q.values("available",
                            Price=F("offer_id__Price"),
                            Offer_name=F("offer_id__Offer_name"),
                            Offer_description=F("offer_id__Offer_description"),
                            Store_id=F("offer_id__Store_id"),
                            Store=F("offer_id__Store_id__Name"),
                            id=F("offer_id"))

            ordering = self.get_ordering()
            if ordering:
                if isinstance(ordering, str):
                    ordering = (ordering,)
                queryset = queryset.order_by(*ordering)
            return queryset
        return qs_fun

    @anotate_available
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
                queryset = self.model.objects.all()   
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['Images'].queryset = Image.objects.filter(Owner__id=self.request.user.id)
        return context
 


    def other_condition(self, request,*args, **kwargs):
        user = request.user
        offer = Offer.objects.get(id=kwargs['pk'])
        return offer.Store.Owner.id == user.id

class OfferTagFilterView(TagFilterView):
    model = Offer
    template_name = 'offer/list.html'
    paginate_by = 5
    permission = 'project.view_offer'
    form_order = OfferOrderForm
    form_filter = OfferFilter

# class OfferExportView(ExcelView,OfferListView):
#     header_font = None
#     data_font = None
#     output_filename = "OffersData.xlsx"
#     worksheet_name = "OffersData"
#     force_csv = False
#     paginate_by = None
