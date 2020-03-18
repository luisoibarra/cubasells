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
from django.db.models import QuerySet
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
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['Bank_Account'].queryset = BankAccount.objects.filter(MyUser__id=self.request.user.id)
        context['form'].fields['Images'].queryset = Image.objects.filter(Owner__id=self.request.user.id)
        return context
    
    
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['Images'].queryset = Image.objects.filter(Owner__id=self.request.user.id)
        return context

    def other_condition(self, request,*args, **kwargs):
        user = request.user
        store = Store.objects.get(id=kwargs['pk'])
        return store.Owner.id == user.id

class StoreUserCreateView(AuthenticateView):
    
    permission = 'project.add_offer'
    permission_denied_template = 'error.html'
    template_name = 'offer/user_create.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            return self._get(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})
  
    def _get(self, request, *args, **kwargs):
        store_id = kwargs['store_id']
        store = Store.objects.all().get(id=store_id)
        f1 = OfferUserCreateForm()
        f2 = SubOfferCreateForm()
        f2.fields['Product_offer'].queryset = Product.objects.all().filter(Store__id = store_id)
        f3 = SubOfferSelectForm(None)
        context = self.get_context(form1=f1,form2=f2,form3=f3,store_id=kwargs['store_id'])
        return render(request,self.template_name,context=context)

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            return self._post(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

    def _post(self, request, *args, **kwargs):
        
        store_id = kwargs['store_id']
        store = Store.objects.all().get(id=store_id)
        f1 = OfferUserCreateForm(request.POST)
        f2 = SubOfferCreateForm(request.POST)
        f2.fields['Product_offer'].queryset = Product.objects.all().filter(Store__id = store_id)
        
        subof2 =[x for x in request.POST.lists()]
        subof = [x for x in subof2 if x[0] == 'suboffers']
        
        default = SubOffer.objects.none()
        if subof:
            default = SubOffer.objects.all().filter(id__in=subof[0][1])
        initial = {}
        for sub in default:
            initial[sub.id] = True
        f3 = SubOfferSelectForm(default,{'suboffers':initial})
        
        if '_add_suboffer' in request.POST and f2.is_valid():
            suboffer = f2.save(False)
            equal_sub = SubOffer.objects.all().filter(Product_offer__id=suboffer.Product_offer.id).filter(Amount=suboffer.Amount)
            if equal_sub:
                f3.fields['suboffers'].queryset |= equal_sub
                f3.data['suboffers'][equal_sub.first().id] = True
            else:
                suboffer.save(force_insert=True)
                to_add = SubOffer.objects.all().filter(id=suboffer.id)
                f3.fields['suboffers'].queryset |= to_add
                f3.data['suboffers'][suboffer.id] = True
                
        if '_remove_suboffer' in request.POST:
            pass
            
        if '_save_offer' in request.POST and f1.is_valid():
            offer = f1.save(False)
            offer.Store = store
            offer.save()
            offer.Suboffer.set(f3.fields['suboffers'].queryset)
            offer.save()
        
        context = self.get_context(form1=f1,form2=f2,form3=f3,store_id=kwargs['store_id'])

        return render(request,self.template_name,context=context)

    def get_context(self,**kwargs):
        context = {}
        context.update(kwargs)
        return context

    def other_condition(self, request,*args, **kwargs):
        user = request.user
        store = Store.objects.get(id=kwargs['store_id'])
        return store.Owner.id == user.id
