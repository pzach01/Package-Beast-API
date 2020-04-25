from django.urls import path
from bins import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('bins/', views.BinList.as_view()),
    path('bins/<int:pk>/', views.BinDetail.as_view())
]
