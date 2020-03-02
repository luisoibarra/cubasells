from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from project.other.forms import *
from project.models import *
from project.custom.views import *
from django.contrib.auth.models import Group
from project.other.filters import *

# Create your views here.


class TagCreateView(AuthenticateCreateView):
    model = Tag
    template_name = "tag/create.html"
    form_class = TagCreateForm
    success_url = reverse_lazy('other:tag_list')
    permission = 'project.add_tag'

class TagListView(FilterOrderAuthenticateListView):
    model = Tag
    template_name='tag/list.html'
    paginate_by = 5
    permission = 'project.view_tag'
    form_filter = TagFilter
    form_order = TagOrderForm
   

class TagDetailView(AuthenticateDetailView):
    model = Tag
    template_name = "tag/view.html"
    permission = 'project.view_tag'

class TagDeleteView(AuthenticateDeleteView):
    model = Tag
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_tag'
    
class TagUpdateView(AuthenticateUpdateView):
    model = Tag
    form_class = TagCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_tag'


class ImageCreateView(AuthenticateCreateView):
    model = Image
    template_name = "image/create.html"
    form_class = ImageCreateForm
    success_url = reverse_lazy('other:image_list')
    permission = 'project.add_image'
    
    def other_condition(self,request,*args, **kwargs):
        return True
        
class ImageListView(FilterOrderAuthenticateListView):
    model = Image
    template_name='image/list.html'
    paginate_by = 5
    permission = 'project.view_image'
    form_order = ImageOrderForm
    form_filter = ImageFilter

class ImageDetailView(AuthenticateDetailView):
    model = Image
    template_name = "image/view.html"
    permission = 'project.view_image'

class ImageDeleteView(AuthenticateDeleteView):
    model = Image
    template_name = "delete.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.delete_image'
    
class ImageUpdateView(AuthenticateUpdateView):
    model = Image
    form_class = ImageCreateForm
    template_name = "update.html"
    success_url = reverse_lazy('project:success')
    permission = 'project.change_image'

