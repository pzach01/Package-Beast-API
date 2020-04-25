from django.urls import path
from boxes import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('boxes/', views.BoxList.as_view()),
    path('boxes/<int:pk>/', views.BoxDetail.as_view())
]
