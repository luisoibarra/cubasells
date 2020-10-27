from project.models import *
from project.auction.forms import *
from project.custom.views import *
from project.auction.filters import *
from project.auction.manager import auction_manager
from project.auction.watcher import auction_watcher
from django.urls import reverse_lazy
from django.template import RequestContext

# Create your views here.

class AuctionCreateView(AuthenticateCreateView):
    model = Auction
    template_name = "auction/create.html"
    form_class = AuctionCreateForm
    success_url = reverse_lazy('auction:auction_list') 
    permission = 'project.add_auction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['Offered'].queryset = Offer.objects.filter(Store__id=self.kwargs['store_id'])
        return context
    
    def other_condition(self,request,*args, **kwargs):
        return 'store_id' in self.kwargs and request.user.id == Store.objects.get(id=self.kwargs['store_id']).Owner.id
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.Deposit = Store.objects.get(id=self.kwargs['store_id']).Bank_Account
        messages = auction_manager.can_book_auction(form.cleaned_data['Offered'])
        if 'Auction was saved' in messages:
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form,messages=messages))


class AuctionListView(FilterOrderAuthenticateListView):
    model = Auction
    template_name = "auction/list.html"
    permission = 'project.view_auction'
    form_order = AuctionOrderForm
    form_filter = AuctionFilter
    
    def get_queryset(self):
        qs = super().get_queryset()
        if 'store_id' in self.kwargs:
            qs = qs.filter(Offered__Store__id=self.kwargs['store_id'])
            return qs.order_by('-Initial_Date')
        return qs.order_by('-Initial_Date')
    
class AuctionDetailView(AuthenticateDetailView):
    model = Auction
    template_name = "auction/view.html"
    permission = 'project.view_auction'
    form_class = AuctionPushForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not 'push_form' in context:
            form = self.form_class()
            form.fields['account'].queryset = form.fields['account'].queryset.filter(MyUser__id=self.request.user.id) 
            context['push_form'] = form
        return context
    
    
    def post(self,request,*args, **kwargs):
        auction_manager.check_auctions()
        
        if '_push' in request.POST:
            form = self.form_class(request.POST)
            self.object = Auction.objects.get(id=self.kwargs['pk'])
            if form.is_valid():
                messages = auction_manager.push(self.object,form.cleaned_data['account'],form.cleaned_data['money'],form.cleaned_data['password'])
                context = self.get_context_data(messages=messages,push_form=form)
                return render(request,self.template_name,context)
            else:
                context = self.get_context_data(mesagges=['Invalid form'],push_form=form)
                return render(request,self.template_name,context)
        
class AuctionDeleteView(AuthenticateDeleteView):
    model = Auction
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_auction'
    
    def other_condition(self,request,*args, **kwargs):
        delete = Auction.objects.get(id=kwargs['pk'])
        from django.utils import timezone
        if delete.Initial_Date < timezone.now() < delete.Final_Date or request.user.id != delete.Offered.Store.Owner.id:
            return False
        return True
        
class AuctionUpdateView(AuthenticateUpdateView):
    model = Auction
    form_class = AuctionCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_auction'

    def other_condition(self,request,*args, **kwargs):
        update = Auction.objects.get(id=kwargs['pk'])
        from django.utils import timezone
        if update.Initial_Date < timezone.now() or request.user.id != update.Offered.Store.Owner.id:
            return False
        return True
 
