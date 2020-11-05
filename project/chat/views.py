from django.shortcuts import render,redirect
from project.custom.views import *
from project.models import Chat
from django.db.models import Q
from project.chat.forms import *
from project.chat.filters import *
from django.urls import reverse_lazy,reverse
from django.db.models import Max, QuerySet
from project.chat.chat_utils import get_last_chats, get_users_chats
# Create your views here.

class ChatCreateView(AuthenticateCreateView):
    model = Chat
    template_name = "chat/create.html"
    form_class = ChatCreateForm
    permission = 'project.add_chat'
    
    @auth
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            form.instance.sender_user = request.user.myuser
            form.instance.receiver_user = MyUser.objects.get(id=kwargs['recv']) 
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse('chat:chat_list',None,[self.kwargs['recv']])

class ChatedUserListView(FilterOrderAuthenticateListView):
    model = Chat
    template_name = 'chat/index.html'
    permission = 'project.view_chat'
    form_order = ChatOrderForm
    form_filter = ChatFilter
    form_user_search = UserSearchForm
    form_send = ChatCreateForm
    
    def get_queryset(self):
        qs = super().get_queryset()
        message = get_last_chats(self.request.user.id)
        return message 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_searcher'] = self.form_user_search(self.request.POST)
        context["send_form"] = self.form_send(self.request.POST)
        if 'recv' in self.kwargs:
            context['chat_user'] = MyUser.objects.get(id=self.kwargs['recv'])
            context['user_conversation'] = get_users_chats(self.kwargs['recv'],self.request.user.id)
        return context
    
    @auth
    def post(self, request, *args, **kwargs):
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
        if 'recv' in self.kwargs:
            qs = get_users_chats(self.request.user.id, self.kwargs['recv'])
        return qs
    
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
