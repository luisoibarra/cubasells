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
    context.update({'accounts':BankAccount.objects.all().filter(MyUser__id=request.user.id)})

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
