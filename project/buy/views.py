from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from project.models import *
from project.buy.forms import *
from project.custom.views import *
from django.contrib.auth.models import Group
from project.buy.filters import *
from project.buy.buy import buy_offers, bank # Mi banco dinamico si algo se hace una BD 'bancaria'
from project.cart.views import ShoppingOfferListView

class BankAccountCreateView(AuthenticateCreateView):
    model = BankAccount
    template_name = "buy/bank_account/create.html"
    form_class = BankAccountCreateForm
    success_url = reverse_lazy('project:user_index')
    permission = 'project.add_bankaccount'
    
    @auth
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.MyUser = request.user.myuser
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class BankAccountListView(FilterOrderAuthenticateListView):
    model = BankAccount
    template_name = "buy/bank_account/list.html"
    paginate_by = 5
    permission = 'project.view_bankaccount'
    form_order = BankAccountOrderForm
    form_filter = BankAccountFilter
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(MyUser__id=self.request.user.id)

class BankAccountDeleteView(AuthenticateDeleteView):
    model = BankAccount
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_bankaccount'

    def other_condition(self, request,*args, **kwargs):
        if request.user.id == BankAccount.objects.get(id=self.kwargs['pk']).MyUser.id:
            return True
        error = "Only the owner of the bank account can update it"
        self.error_msg += error
        return False
  
class BankAccountUpdateView(AuthenticateUpdateView):
    model = BankAccount
    form_class = BankAccountCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_bankaccount'
  
    def other_condition(self, request,*args, **kwargs):
        if request.user.id == BankAccount.objects.get(id=self.kwargs['pk']).MyUser.id:
            return True
        error = "Only the owner of the bank account can update it"
        self.error_msg += error
        return False

class BuyCartView(AuthenticateView):
    permission = 'project.add_buyoffer'
    bank_class = bank
    
    @auth
    def post(self,request,*args,**kwargs):
        password = request.POST['password']
        account = BankAccount.objects.get(id=int(request.POST['account']))
        shop_offers = ShoppingOffer.objects.filter(Cart__myuser__id=request.user.id)
        buy_offer = buy_offers(account,password,shop_offers)
        if 'error' in buy_offer:
            return render(request,'error.html',buy_offer)
        shop_offers.delete()
        context = self.get_context_data(**kwargs)
        context.update(buy_offer)
        return redirect(reverse_lazy('project:success'))

    def get_context_data(self, **kwargs):
        context = {}
        return context
    