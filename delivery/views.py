# delivery/views.py

from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect

from delivery.models import (
    Food,
    Category
    )

class IndexView(ListView):
    model = Food
    template_name = 'delivery/index.html'

class CategoryFoodView(ListView):
    model = Food
    template_name = 'delivery/category_food.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
