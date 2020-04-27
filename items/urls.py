from django.urls import path
from items import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('items/', views.ItemList.as_view()),
    path('items/<int:pk>/', views.ItemDetail.as_view())
]
