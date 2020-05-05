# delivery/urls.py

from django.urls import path
from delivery.views import (
    IndexView,
    CategoryFoodView,
    DetailFoodView,
    
    )
from delivery import views

app_name = 'delivery'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('delivery/<int:pk>/', PostDetailView.as_view(), name='delivery_detail'),
    path('categories/<str:category_slug>/',
         CategoryFoodView.as_view(), name='category_food'),
    # path('tags/', TagListView.as_view(), name='tag_list'),
    path('foods/<str:food_name>/',
         DetailFoodView.as_view(), name='detail_food'),
    path('create/', views.InvoiceCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.InvoiceUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.InvoiceDeleteView.as_view(), name='delete'),
]
