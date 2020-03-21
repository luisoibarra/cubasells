from django.shortcuts import render,reverse
from django.views.generic import  ListView,CreateView,UpdateView,DeleteView
from project.bank.models import  BankAccount
from django.urls import reverse_lazy

# Create your views here.

class BankAccountListView(ListView):
    model = BankAccount
    template_name='bank/list.html'

class BankAccountCreateView(CreateView):
    model = BankAccount
    template_name = "bank/create.html"
    success_url = reverse_lazy('bank:list')
    fields = '__all__'
    
class BankAccountUpdateView(UpdateView):
    model = BankAccount
    template_name = "update.html"
    success_url = reverse_lazy('bank:list')
    fields = '__all__'
    
class BankAccountDeleteView(DeleteView):
    model = BankAccount
    template_name = "delete.html"
    success_url = reverse_lazy('bank:list')
    