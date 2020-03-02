from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from project.store.forms import *
from project.suboffer.forms import *
from project.offer.forms import *
from project.product.forms import *
from project.models import *
from project.custom.views import *
from django.contrib.auth.models import Group
from project.store.filters import *
# Create your views here.

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
    success_url = reverse_lazy('store:store_list')
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

class MultiCreateView(AuthenticateView):
    
    permission = 'project.add_offer'
    permission_denied_template = 'error.html'
    template_name = 'test.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            return self._get(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})
  
    def _get(self, request, *args, **kwargs):
        store_id = kwargs['store_id']
        store = Store.objects.all().get(id=store_id)
        f1 = OfferCreateForm()
        f1.fields['Suboffer'].queryset = SubOffer.objects.all().filter(Product_offer__Store__id = store_id)
        f2 = SubOfferCreateForm()
        f2.fields['Product_offer'].queryset = Product.objects.all().filter(Store__id = store_id)
        # f3 = ProductCreateForm()
        f4 = SubOfferSelectForm(SubOffer.objects.all().filter(Product_offer__Store__id=store_id))
        context = self.get_context(form1=f1,form2=f2,form4=f4,store_id=kwargs['store_id'])
        return render(request,self.template_name,context=context)

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            return self._post(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

    def _post(self, request, *args, **kwargs):
        store_id = kwargs['store_id']
        store = Store.objects.all().get(id=store_id)
        f1 = OfferCreateForm(request.POST)
        f1.fields['Suboffer'].queryset = SubOffer.objects.all().filter(Product_offer__Store__id = store_id)
        f2 = SubOfferCreateForm(request.POST)
        f2.fields['Product_offer'].queryset = Product.objects.all().filter(Store__id = store_id)
        # f3 = ProductCreateForm(request.POST)
        
        f4 = SubOfferSelectForm(SubOffer.objects.all().filter(Product_offer__Store__id=store_id))
        
        f1.instance.Store = store
        # f3.instance.Store = store
        context = self.get_context(form1=f1,form2=f2,form4=f4,store_id=kwargs['store_id'])
        if '_save_offer' in request.POST and f1.is_valid():
            f1.save()
            context['offer_msg'] = 'Success'
        if '_save_suboffer_new' in request.POST and f2.is_valid():
            suboffer = f2.save(commit=False)
            f1.fields['Suboffer'].queryset.add(suboffer)
            context['suboffer_msg'] = 'Success'
        if '_save_suboffer_old' in request.POST and f4.is_valid():
            suboffer = f4.save()
            f1.fields['Suboffer'].queryset.add(suboffer)
            context['product_msg'] = 'Success'
        return render(request,self.template_name,context=context)

    def get_context(self,**kwargs):
        context = {}
        context.update(kwargs)
        return context

    def other_condition(self, request,*args, **kwargs):
        user = request.user
        store = Store.objects.get(id=kwargs['store_id'])
        return store.Owner.id == user.id
