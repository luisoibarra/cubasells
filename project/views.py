from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from project.models import *
from project.forms import *
# Create your views here.

def index(request):
    return render(request,'index.html')


class UserCreateView(CreateView):
    model = MyUser
    template_name = "user/create.html"
    form_class = MyUserCreateForm
    success_url = reverse_lazy('cubasells:login')

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

from django.core.exceptions import ObjectDoesNotExist
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