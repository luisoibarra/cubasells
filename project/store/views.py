from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render, resolve_url, redirect
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
from django.db.models import QuerySet,Sum,F,FloatField
# Create your views here.
import plotly.offline as opy
import plotly.graph_objs as go
from project.other.forms import ImageCreateForm


class Graph(AuthenticateDetailView):
    model = Store
    template_name = 'store/stats.html'
    permission = 'project.view_store'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)
        q = BuyOffer.objects.filter(Offer_id__Store_id=context['store'].id).values(
            'Offer_id', 'Offer_id__Offer_name').annotate(tamount=Sum('Amount')).order_by('-tamount')
        #Para probar los graficos quitar a partir del punto de filter hasta el punto antes de value
        #la tienda que cree no tiene ventas ni nada asi q por eso no sale nada
        q2 = BuyOffer.objects.filter(Offer_id__Store_id=context['store'].id).values(
            'Offer_id', 'Offer_id__Offer_name').annotate(
                tprice=Sum(F('Offer_id__Price') * F('Amount'),output_field=FloatField())).order_by('-tprice')

        OfferNameP=[]
        OfferNameA=[]
        TPrice=[]
        TAmount=[]

        for i in q:
            _,t2,t3=i.values()
            OfferNameA.append(t2)
            TAmount.append(t3)
        for i in q2:
            _, t2, t3 = i.values()
            OfferNameP.append(t2)
            TPrice.append(t3)
        

        data=[
            go.Bar(
                x=OfferNameP,
                y=TPrice,
                name='Precio total de ventas por oferta'
            )
            ,
            go.Bar(
                x=OfferNameA,
                y=TAmount,
                name='Cantidad de ventas por oferta'
            )
        ]
        data1=[
            go.Pie(
                labels=OfferNameP,
                values=TPrice,
                name='Precio total de ventas por oferta',
                domain={'x': [0, .50]},
                hole=.5,
                #textposition='inside',
                #hoverinfo='label+percent+name'
            )
            ,
            go.Pie(
                labels=OfferNameA,
                values=TAmount,
                name='Cantidad de ventas por oferta',
                domain={'x': [.50, 1]},
                hole=.5,
                #textposition='inside',
                #hoverinfo='label+percent+name'
            )
        ]

        layout = go.Layout(title="Bar Graphs", xaxis={
                           'title': 'Ofertas'}, yaxis={'title': 'Ventas'})
        figure=go.Figure(data=data,layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
        context['graph'] = div

        layout1 = go.Layout(title='Pie Graphs',
            annotations=[
                {
                    "font":{"size":16},
                    "showarrow":False,
                    "text": '''Precio total de <br> ventas por oferta''',
                    "x":0.185,
                    "y":0.5
                },
                {
                    "font": {"size": 16},
                    "showarrow": False,
                    "text": '''Cantidad de <br> ventas por oferta''',
                    "x": 0.815,
                    "y": 0.5
                }
            ]
        )
        figure1 = go.Figure(data=data1, layout=layout1)
        div1 = opy.plot(figure1, auto_open=False, output_type='div')
        context['graph1'] = div1

        return context

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
        context['image_form'] = ImageCreateForm()
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
                store = form.save()
                image_form = ImageCreateForm(request.POST, request.FILES)
                if image_form.is_valid():
                    image_form.instance.Owner_id = request.user.id
                    image = image_form.save()
                    store.Images.add(image)
                store.save()
                return redirect(resolve_url('store:store_list'),permanent=True)
            else:
                return self.form_invalid(form)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

class StoreListView(FilterOrderAuthenticateListView):
    model = Store
    template_name = "store/list.html"
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
        f1.fields['Images'].queryset = Image.objects.filter(Owner__id=self.request.user.id)
        f3 = SubOfferSelectForm(None)
        f4 = ImageCreateForm()
        context = self.get_context(form1=f1,form2=f2,form3=f3, image_form=f4, store_id=kwargs['store_id'])
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
        
        image_form = ImageCreateForm(request.POST, request.FILES)
        
        if '_save_offer' in request.POST and f1.is_valid():
            f1.instance.Store = store
            image = None
            if image_form.is_valid():
                image_form.instance.Owner_id = request.user.id
                image = image_form.save()
            offer = f1.save()
            offer.Suboffer.set(f3.fields['suboffers'].queryset)
            if image:
                offer.Images.add(image)
            offer.save()
            return redirect(resolve_url('store:store_offer_list',kwargs['store_id']),permanent=True)
        
        context = self.get_context(form1=f1,form2=f2,form3=f3,image_form=image_form,store_id=kwargs['store_id'])

        return render(request,self.template_name,context=context)

    def get_context(self,**kwargs):
        context = {}
        context.update(kwargs)
        return context

    def other_condition(self, request,*args, **kwargs):
        user = request.user
        store = Store.objects.get(id=kwargs['store_id'])
        return store.Owner.id == user.id

class StoreTagFilterView(TagFilterView):
    model = Store
    template_name = 'store/list.html'
    permission = 'project.view_store'
    form_order = StoreOrderForm
    form_filter = StoreFilter
