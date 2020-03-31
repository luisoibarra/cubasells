from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView,View)
from django.shortcuts import render

from project.other.forms import *
from project.models import *

from excel_response import ExcelResponse

class AuthenticateView(View):
    permission = None
    permission_denied_template = 'error.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            return super().get(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})
    
    def other_condition(self, request,*args, **kwargs):
        return True       
    
    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            return super().post(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})


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
    
    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            return super().post(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

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

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            return super().post(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})
        
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

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            return super().post(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

class FilterOrderAuthenticateListView(AuthenticateListView):

    form_order = None
    
    form_filter = None
    
    def get_ordering(self,data = None):
        """Return the field or fields to use for ordering the queryset."""
        if data:
            sort_by = [x for x in data if data[x]]
            sort_by = {x:data[f'{x}_decrease'] for x in sort_by if not x.endswith('_decrease') }
            self.ordering = [ (f"-{x}" if sort_by[x] else x) for x in sort_by]
        return self.ordering
    
    def get_context_data(self, object_list=None,**kwargs):
        context = super().get_context_data(object_list=object_list,**kwargs)
        try:
            context["order"] = kwargs['form']
            context["filter"] = kwargs['form2']
        except KeyError:
            pass
        return context
    
    def get_form(self,request,get=True):
        if get:
            return self.form_order(request.GET)
        return self.form_order(request.POST)
    
    def get_form_cleaned_data(self,form):
        form.full_clean()
        return form.cleaned_data

    def get(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            form_order = self.get_form(request)
            if form_order.is_valid():
                form_data = self.get_form_cleaned_data(form_order)
                self.get_ordering(form_data)
                self.object_list = self.get_queryset()
                form_filter = self.form_filter(request.GET,self.object_list)
                self.object_list = form_filter.qs
                context = self.get_context_data(object_list=self.object_list,form=form_order,form2=form_filter,**kwargs)
                if not form_filter.is_valid():
                    return render(request,self.template_name,context)
            else:
                context = self.get_context_data(form=form_order,form2=form_filter,**kwargs)
                return render(request,self.template_name,context)
            
            allow_empty = self.get_allow_empty()
            if not allow_empty:
                # When pagination is enabled and object_list is a queryset,
                # it's better to do a cheap query than to load the unpaginated
                # queryset in memory.
                if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = not self.object_list
                if is_empty:
                    raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                        'class_name': self.__class__.__name__,
                    })
            return self.render_to_response(context)
        else:
            return render(request,'error.html',{'error':'You dont have authorization for this action'})

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            form_order = self.get_form(request,False)
            if form_order.is_valid():
                form_data = self.get_form_cleaned_data(form_order)
                self.get_ordering(form_data)
                self.object_list = self.get_queryset()
                form_filter = self.form_filter(request.POST,self.object_list)
                self.object_list = form_filter.qs
                context = self.get_context_data(object_list=self.object_list,form=form_order,form2=form_filter,**kwargs)
                if not form_filter.is_valid():
                    return render(request,self.template_name,context)
            else:
                context = self.get_context_data(form=form_order,form2=form_filter,**kwargs)
                return render(request,self.template_name,context)
            
            allow_empty = self.get_allow_empty()
            if not allow_empty:
                # When pagination is enabled and object_list is a queryset,
                # it's better to do a cheap query than to load the unpaginated
                # queryset in memory.
                if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = not self.object_list
                if is_empty:
                    raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                        'class_name': self.__class__.__name__,
                    })
            if "export" in request.POST:
                return ExcelResponse(self.object_list)
            return self.render_to_response(context)
        else:
            return render(request,'error.html',{'error':'You dont have authorization for this action'})

class TagFilterView(FilterOrderAuthenticateListView):



    def get(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            form_order = self.get_form(request)
            if form_order.is_valid():
                form_data = self.get_form_cleaned_data(form_order)
                self.get_ordering(form_data)
                self.object_list = self.get_queryset()
            ##############################
                taglist = Tag.objects.all()
                f1 = MultiSelectSTagForm(taglist,request.GET)
            #############################
                form_filter = self.form_filter(request.GET,self.object_list)
                self.object_list = form_filter.qs
                context = self.get_context_data(object_list=self.object_list,form=form_order,form1=f1,form2=form_filter,**kwargs)
                if not form_filter.is_valid():
                    return render(request,self.template_name,context)
            else:
                context = self.get_context_data(form=form_order,form1=f1,form2=form_filter,**kwargs)
                return render(request,self.template_name,context)
            
            allow_empty = self.get_allow_empty()
            if not allow_empty:
                # When pagination is enabled and object_list is a queryset,
                # it's better to do a cheap query than to load the unpaginated
                # queryset in memory.
                if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = not self.object_list
                if is_empty:
                    raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                        'class_name': self.__class__.__name__,
                    })
            return self.render_to_response(context)
        else:
            return render(request,'error.html',{'error':'You dont have authorization for this action'})


    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            form_order = self.get_form(request,False)
            if form_order.is_valid():
                form_data = self.get_form_cleaned_data(form_order)
                self.get_ordering(form_data)
                self.object_list = self.get_queryset()
                ##########################
                taglist = Tag.objects.all()
                f1 = MultiSelectSTagForm(taglist,request.POST)
                ##########################
                form_filter = self.form_filter(request.POST,self.object_list)
                if f1.is_valid():
                    self.object_list = form_filter.qs.filter(Tags__id=int(f1.data['tags'][0]))
                else:
                    self.object_list = form_filter.qs

                context = self.get_context_data(object_list=self.object_list,form=form_order,form1=f1,form2=form_filter,**kwargs)
                if not form_filter.is_valid():
                    return render(request,self.template_name,context)
            else:
                context = self.get_context_data(form=form_order,form1=f1,form2=form_filter,**kwargs)
                return render(request,self.template_name,context)
            
            allow_empty = self.get_allow_empty()
            if not allow_empty:
                # When pagination is enabled and object_list is a queryset,
                # it's better to do a cheap query than to load the unpaginated
                # queryset in memory.
                if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = not self.object_list
                if is_empty:
                    raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                        'class_name': self.__class__.__name__,
                    })
            return self.render_to_response(context)
        else:
            return render(request,'error.html',{'error':'You dont have authorization for this action'})


    def other_condition(self, request,*args, **kwargs):
        return True

