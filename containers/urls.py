from django.urls import path
from containers import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('containers/', views.ContainerList.as_view()),
    path('containers/<int:pk>/', views.ContainerDetail.as_view())
]
