from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from project.forms import *
from project.models import *
from project.custom.views import *
from django.contrib.auth.models import Group
from project.filters import *

# Create your views here.

def index(request):
    return render(request,'index.html')

def success_view(request):
    return render(request,'success.html')

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

class UserCreateView(CreateView):
    model = MyUser
    template_name = "user/create.html"
    form_class = MyUserCreateForm
    success_url = reverse_lazy('cubasells:login')
    
    def post(self, request, *args, **kwargs):
        self.object = None
        p_return = super().post(request, *args, **kwargs)
        if self.object:
            group = Group.objects.get(name='UserGroup')
            group.user_set.add(self.object)
        return p_return

class UserDeleteView(AuthenticateDeleteView):
    model = MyUser
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_myuser'
    
    def other_condition(self, request,*args, **kwargs):
        return self.kwargs['pk'] == request.user.id

class UserUpdateView(AuthenticateUpdateView):
    model = MyUser
    form_class = MyUserCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_myuser'
    
    def other_condition(self, request,*args, **kwargs):
        return self.kwargs['pk'] == request.user.id

class TagCreateView(AuthenticateCreateView):
    model = Tag
    template_name = "tag/create.html"
    form_class = TagCreateForm
    success_url = reverse_lazy('cubasells:tag_list')
    permission = 'project.add_tag'

class TagListView(FilterOrderAuthenticateListView):
    model = Tag
    template_name='tag/list.html'
    paginate_by = 5
    permission = 'project.view_tag'
    form_filter = TagFilter
    form_order = TagOrderForm
    

class TagDetailView(AuthenticateDetailView):
    model = Tag
    template_name = "tag/view.html"
    permission = 'project.view_tag'

class TagDeleteView(AuthenticateDeleteView):
    model = Tag
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_tag'
    
class TagUpdateView(AuthenticateUpdateView):
    model = Tag
    form_class = TagCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_tag'


class ImageCreateView(AuthenticateCreateView):
    model = Image
    template_name = "image/create.html"
    form_class = ImageCreateForm
    success_url = reverse_lazy('cubasells:image_list')
    permission = 'project.add_image'

class ImageListView(FilterOrderAuthenticateListView):
    model = Image
    template_name='image/list.html'
    paginate_by = 5
    permission = 'project.view_image'
    form_order = ImageOrderForm
    form_filter = ImageFilter

class ImageDetailView(AuthenticateDetailView):
    model = Image
    template_name = "image/view.html"
    permission = 'project.view_image'

class ImageDeleteView(AuthenticateDeleteView):
    model = Image
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_image'
    
class ImageUpdateView(AuthenticateUpdateView):
    model = Image
    form_class = ImageCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_image'


class SubOfferCreateView(AuthenticateCreateView):
    model = SubOffer
    template_name = "suboffer/create.html"
    form_class = SubOfferCreateForm
    success_url = reverse_lazy('cubasells:offer_list')
    permission = 'project.add_suboffer'


    def update_extra_context(self,extra):
        if self.extra_context is None:
            self.extra_context = extra
        else:
            self.extra_context.update(extra)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        try:
            self.form_class.base_fields['Product_offer'].queryset = Product.objects.filter(Store__id = self.kwargs['store_id'])#forms.ModelMultipleChoiceField(queryset=Product.objects.filter(Store__id = self.kwargs['store_id']))
        except KeyError:
            context.update({'error':'Missing parameter store_id in url'})
        return context
    
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
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

class SubOfferListView(FilterOrderAuthenticateListView):
    model = SubOffer
    template_name='suboffer/list.html'
    paginate_by = 5
    permission = 'project.view_suboffer'
    form_order = SubOfferOrderForm
    form_filter = SubOfferFilter
    
    
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

class SubOfferDetailView(AuthenticateDetailView):
    model = SubOffer
    template_name = "suboffer/view.html"
    permission = 'project.view_suboffer'

class SubOfferDeleteView(AuthenticateDeleteView):
    model = SubOffer
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_suboffer'
    
    def other_condition(self, request,*args, **kwargs):
        user = request.user
        suboffer = SubOffer.objects.get(id=kwargs['pk'])
        return suboffer.Product_offer.Store.Owner.id == user.id

class SubOfferUpdateView(AuthenticateUpdateView):
    model = SubOffer
    form_class = SubOfferCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_suboffer'

    def other_condition(self, request,*args, **kwargs):
        user = request.user
        suboffer = SubOffer.objects.get(id=kwargs['pk'])
        return suboffer.Product_offer.Store.Owner.id == user.id


class OfferCreateView(AuthenticateCreateView):
    model = Offer
    template_name = "offer/create.html"
    form_class = OfferCreateForm
    success_url = reverse_lazy('cubasells:store_index') # idealmente quiero que te deje en la tienda q le vas a agregar el producto
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
                    self.success_url = reverse_lazy('cubasells:store_offer_list',kwargs={'store_id':store.id})
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


class ProductCreateView(AuthenticateCreateView):
    model = Product
    template_name = "product/create.html"
    form_class = ProductCreateForm
    success_url = reverse_lazy('cubasells:store_index') 
    permission = 'project.add_product'

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
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

class ProductListView(FilterOrderAuthenticateListView):
    model = Product
    template_name='product/list.html'
    paginate_by = 5
    permission = 'project.view_product'
    form_order = ProductOrderForm
    form_filter = ProductFilter
    
    def get_context_data(self,object_list=None,**kwargs):
        context = super().get_context_data(object_list,**kwargs)
        try:
            context['store_id'] = kwargs['store_id']
            context['store'] = Store.objects.get(id=kwargs['store_id'])
        except:
            pass
        return context
    
    def get(self,request,*args, **kwargs):
        return super().get(request,*args, **kwargs)
    
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
    
class ProductDetailView(AuthenticateDetailView):
    model = Product
    template_name = "product/view.html"
    permission = 'project.view_product'

class ProductDeleteView(AuthenticateDeleteView):
    model = Product
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_product'
    
    def other_condition(self, request,*args, **kwargs):
        user = request.user
        product = Product.objects.get(id=kwargs['pk'])
        return product.Store.Owner.id == user.id

class ProductUpdateView(AuthenticateUpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_product'

    def other_condition(self, request,*args, **kwargs):
        user = request.user
        product = Product.objects.get(id=kwargs['pk'])
        return product.Store.Owner.id == user.id


def store_index(request):
    context = {'stores':Store.objects.all()}
    return render(request,'store/index.html',context=context)

class StoreDetailView(AuthenticateDetailView):
    model = Store
    template_name = 'store/view.html'
    permission = 'project.view_store'

class StoreCreateView(AuthenticateCreateView):
    model = MyUser
    template_name = "store/create.html"
    form_class = StoreCreateForm
    success_url = reverse_lazy('cubasells:store_list')
    permission = 'project.add_store'
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            form = self.get_form()
            form.instance.Owner = MyUser.objects.get(id=request.user.id) 
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

class StoreListView(FilterOrderAuthenticateListView):
    model = Store
    template_name = "store/list.html"
    paginate_by = 5
    permission = 'project.view_store'
    form_order = StoreOrderForm
    form_filter = StoreFilter
 
class StoreDeleteView(AuthenticateDeleteView):
    model = Store
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_store'
    
    def other_condition(self, request,*args, **kwargs):
        user = request.user
        store = Store.objects.get(id=kwargs['pk'])
        return store.Owner.id == user.id

class StoreUpdateView(AuthenticateUpdateView):
    model = Store
    form_class = StoreCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_store'

    def other_condition(self, request,*args, **kwargs):
        user = request.user
        store = Store.objects.get(id=kwargs['pk'])
        return store.Owner.id == user.id
