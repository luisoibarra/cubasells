import django_filters as dfil
from project.models import *

class TagFilter(dfil.FilterSet):
    class Meta:
        model = Tag
        fields = {
            'Tag':['icontains'],
        }

class ImageFilter(dfil.FilterSet):
    class Meta:
        model = Image
        fields = {
            'ImageName':['icontains'],
        }