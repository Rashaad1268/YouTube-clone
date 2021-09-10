import django_filters
from django_filters import CharFilter

from .models import Video

class VideoFilter(django_filters.FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    
    class Meta:
        model = Video
        fields = ("title",)
