from django.urls import path
from arrangements import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('arrangements/', views.ArrangementList.as_view()),
    path('arrangements/<int:pk>/', views.ArrangementDetail.as_view())
]
