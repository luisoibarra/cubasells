from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.shortcuts import render

class AuthenticateCreateView(CreateView):
    
    permission = None
    permission_denied_template = 'error.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            return super().get(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})
    
    def other_condition(self, request,*args, **kwargs):
        return True       
    
class AuthenticateDeleteView(DeleteView):
    
    permission = None
    permission_denied_template = 'error.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            return super().get(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})
    
    def other_condition(self, request,*args, **kwargs):
        return True
        
class AuthenticateDetailView(DetailView):
    
    permission = None
    permission_denied_template = 'error.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            return super().get(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})
    
    def other_condition(self, request,*args, **kwargs):
        return True    
        
class AuthenticateListView(ListView):
    
    permission = None
    permission_denied_template = 'error.html'
    def get(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            return super().get(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})
    
    def other_condition(self, request,*args, **kwargs):
        return True    

class AuthenticateUpdateView(UpdateView):
    
    permission = None
    permission_denied_template = 'error.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            return super().get(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})
    
    def other_condition(self, request,*args, **kwargs):
        return True
