import django_filters
from .models import *
class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Stock
        fields = ['id_sous_famille']