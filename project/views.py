from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from project.forms import *
from project.models import *

# Create your views here.

def index(request):
    return render(request,'index.html')


class UserCreateView(CreateView):
    model = MyUser
    template_name = "user/create.html"
    form_class = MyUserCreateForm
    success_url = reverse_lazy('cubasells:login')


class SubOfferCreateView(CreateView):
    model = SubOffer
    template_name = "suboffer/create.html"
    form_class = SubOfferCreateForm
    success_url = reverse_lazy('cubasells:offer_list')

    def update_extra_context(self,extra):
        if self.extra_context is None:
            self.extra_context = extra
        else:
            self.extra_context.update(extra)
    
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        self.object = None
        context = self.get_context_data()
        try:
            self.form_class.base_fields['Product_offer'].queryset = Product.objects.filter(Store__id = self.kwargs['store_id'])#forms.ModelMultipleChoiceField(queryset=Product.objects.filter(Store__id = self.kwargs['store_id']))
        except KeyError:
            context.update({'error':'Missing parameter store_id in url'})
        return self.render_to_response(context)

    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None
        
        form = self.get_form()
        try:
            store = Store.objects.get(id=kwargs['store_id'])
            if store.Owner.id == request.user.id:
                self.success_url = reverse_lazy('cubasells:store_suboffer_list',kwargs={'store_id':store.id})
            else:
                extra = {'error':'User not authorized to create an offer in this store, must be its owner'}
                self.update_extra_context(extra)
                return self.form_invalid(form)
        except ObjectDoesNotExist:
            extra = {'error':'Store doesnt exist'}
            self.update_extra_context(extra)
            return self.form_invalid(form)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class SubOfferListView(ListView):
    model = SubOffer
    template_name='suboffer/list.html'
    paginate_by = 5

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
                queryset = self.model.objects.filter(Product_offer__Store__id=self.kwargs['store_id'])
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

    
class OfferCreateView(CreateView):
    model = Offer
    template_name = "offer/create.html"
    form_class = OfferCreateForm
    success_url = reverse_lazy('cubasells:store_index') # idealmente quiero que te deje en la tienda q le vas a agregar el producto

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        self.object = None
        context = self.get_context_data()
        try:
            self.form_class.base_fields['Suboffer'].queryset = SubOffer.objects.filter(Product_offer__Store__id = self.kwargs['store_id'])#forms.ModelMultipleChoiceField(queryset=Product.objects.filter(Store__id = self.kwargs['store_id']))
        except KeyError:
            context.update({'error':'Missing parameter store_id in url'})
        return self.render_to_response(context)


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
        
        form = self.get_form()
        try:
            store = Store.objects.get(id=kwargs['store_id'])
            if store.Owner.id == request.user.id:
                form.instance.Store = store
                self.success_url = reverse_lazy('cubasells:store_offer_list',kwargs={'store_id':store.id})
            else:
                extra = {'error':'User not authorized to create an offer in this store, must be its owner'}
                self.update_extra_context(extra)
                return self.form_invalid(form)
        except ObjectDoesNotExist:
            extra = {'error':'Store doesnt exist'}
            self.update_extra_context(extra)
            return self.form_invalid(form)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class OfferListView(ListView):
    model = Offer
    template_name = "offer/list.html"
    paginate_by = 5

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

class OfferDetailView(DetailView):
    model = Offer
    template_name = "offer/view.html"


class ProductCreateView(CreateView):
    model = Product
    template_name = "product/create.html"
    form_class = ProductCreateForm
    success_url = reverse_lazy('cubasells:store_index') # idealmente quiero que te deje en la tienda q le vas a agregar el producto

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
        
        form = self.get_form()
        try:
            store = Store.objects.get(id=kwargs['store_id'])
            if store.Owner.id == request.user.id:
                form.instance.Store = store
                self.success_url = reverse_lazy('cubasells:store_product_list',kwargs={'store_id':store.id})
            else:
                extra = {'error':'User not authorized to create a product in this store, must be its owner'}
                self.update_extra_context(extra)
                return self.form_invalid(form)
        except ObjectDoesNotExist:
            extra = {'error':'Store doesnt exist'}
            self.update_extra_context(extra)
            return self.form_invalid(form)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class ProductListView(ListView):
    model = Product
    template_name='product/list.html'
    paginate_by = 5
    
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
    
class ProductDetailView(DetailView):
    model = Product
    template_name = "product/view.html"


def store_view(request,store_id = -1):
    context = {'store_id':store_id}
    
    try:
        context.update({'store':Store.objects.get(id = store_id)})
    except ObjectDoesNotExist:
        context.update({'errors':['Store id doesnt exist']})
        
    return render(request,'store/view.html',context=context)

def store_index(request):
    context = {'stores':Store.objects.all()}
    return render(request,'store/index.html',context=context)

class StoreCreateView(CreateView):
    model = MyUser
    template_name = "store/create.html"
    form_class = StoreCreateForm
    success_url = reverse_lazy('cubasells:store_list')
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None
        
        form = self.get_form()
        form.instance.Owner = MyUser.objects.get(id=request.user.id) 
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class StoreListView(ListView):
    model = Store
    template_name = "store/list.html"
    paginate_by = 5


class MyLoginView(LoginView):
    template_name ='login.html'

class MyLogoutView(LogoutView):
    template_name = 'login.html'

def user_index(request):
    context = {'user': request.user}
    context.update({'tags':request.user.myuser.Tags.all()})
    context.update({'images':request.user.myuser.Images.all()})
    context.update({'accounts':request.user.myuser.Accounts.all()})

    return render(request,'user/index.html',context=context)
