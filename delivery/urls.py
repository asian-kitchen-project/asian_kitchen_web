# delivery/urls.py

from django.urls import path
from delivery.views import (
    IndexView,
    CategoryFoodView,
    DetailFoodView
    )

app_name = 'delivery'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('delivery/<int:pk>/', PostDetailView.as_view(), name='delivery_detail'),
    path('categories/<str:category_slug>/',
         CategoryFoodView.as_view(), name='category_food'),
    # path('tags/', TagListView.as_view(), name='tag_list'),
    path('foods/<str:food_name>/',
         DetailFoodView.as_view(), name='detail_food'),
]
