from django.urls import path
from quotes import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('quotes/', views.QuoteList.as_view()),
    path('quotes/<int:pk>/', views.QuoteDetail.as_view())
]