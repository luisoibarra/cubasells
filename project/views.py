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
    model = User
    model2 = MyUser
    template_name = "user/create.html"
    form_class = UserCreateForm
    form_class2 = MyUserCreateForm
    success_url = reverse_lazy('cubasells:login')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.form_class2(self.request.GET)
        
        return context
            
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.form_class2(request.POST)
        
        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            user.myuser = form2.save()
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form,form2=form2))


class MyLoginView(LoginView):
    template_name ='login.html'

class MyLogoutView(LogoutView):
    template_name = 'login.html'

def index_user(request):
    return render(request,'user/index.html',{'user': request.user})
