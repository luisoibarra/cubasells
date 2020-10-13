from django.shortcuts import render,redirect
from project.custom.views import *
from project.models import Chat
from django.db.models import Q
from project.chat.forms import *
from project.chat.filters import *
from django.urls import reverse_lazy,reverse
# Create your views here.


class ChatCreateView(AuthenticateCreateView):
    model = Chat
    template_name = "chat/create.html"
    form_class = ChatCreateForm
    permission = 'project.add_chat'
    
    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            return self._post(request, *args, **kwargs)
        else:
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

    def get_success_url(self):
        return reverse('chat:chat_list',None,[self.kwargs['recv']])

    def _post(self,request,*args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.sender_user = request.user.myuser
            form.instance.receiver_user = MyUser.objects.get(id=kwargs['recv']) 
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        
    def other_condition(self,request,*args, **kwargs):
        return True

class ChatedUserListView(FilterOrderAuthenticateListView):
    model = MyUser
    template_name = 'chat/index.html'
    permission = 'project.view_chat'
    form_order = ChatUserOrderForm
    form_filter = ChatUserFilter
    form_user_search = UserSearchForm
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs1 = qs.filter(id__in=[obj.receiver_user.id for obj in Chat.objects.filter(sender_user__id=self.request.user.id)])
        qs2 = qs.filter(id__in=[obj.sender_user.id for obj in Chat.objects.filter(receiver_user__id=self.request.user.id)])
        return qs1 | qs2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_searcher'] = self.form_user_search(self.request.POST)
        return context
    
    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission) and self.other_condition(request,*args,**kwargs):
            self.object = None
            form_order = self.get_form(request,False)
            self.object_list = self.get_queryset()
            form_filter = self.form_filter(request.POST,self.object_list)
            context = self.get_context_data(object_list=self.object_list,form=form_order,form2=form_filter,**kwargs)
            if 'user_searcher' in request.POST:
                user_search = self.form_user_search(self.request.POST)
                if user_search.is_valid():
                    return redirect('chat:chat_list',permanent=True,recv=user_search.cleaned_data['username'])
                else:
                    return self.render_to_response(context)
            
            if form_order.is_valid():
                form_data = self.get_form_cleaned_data(form_order)
                self.get_ordering(form_data)
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
            return render(request,self.permission_denied_template,{'error':'You dont have authorization for this action'})

    
    
class ChatListView(FilterOrderAuthenticateListView):
    model = Chat
    template_name='chat/list.html'
    permission = 'project.view_chat'
    form_order = ChatOrderForm
    form_filter = ChatFilter
    paginate_by = 5
    form_send = ChatCreateForm
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = Q(sender_user__id = self.request.user.id) | Q(receiver_user__id = self.request.user.id)
        qs = qs.filter(q)
        if 'recv' in self.kwargs:
            q = Q(sender_user__id = self.kwargs['recv']) | Q(receiver_user__id = self.kwargs['recv'])
            qs = qs.filter(q)
        return qs.order_by('-Date') # Messages more recent on the top
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["send_form"] = self.form_send(self.request.POST)
        return context
    
        
class ChatDetailView(AuthenticateDetailView):
    model = Chat
    template_name = "chat/view.html"
    permission = 'project.view_chat'

class ChatDeleteView(AuthenticateDeleteView):
    model = Chat
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_chat'
    
    def other_condition(self, request,*args, **kwargs):
        user = request.user
        msg = Chat.objects.get(id=kwargs['pk'])
        return msg.sender_user.id == user.id

class ChatUpdateView(AuthenticateUpdateView):
    model = Chat
    form_class = ChatCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_chat'

    def other_condition(self, request,*args, **kwargs):
        user = request.user
        msg = Chat.objects.get(id=kwargs['pk'])
        return msg.sender_user.id == user.id

