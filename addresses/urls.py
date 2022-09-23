from django.urls import path
from addresses import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('addresses/', views.AddressList.as_view()),
    path('addresses/<int:pk>/', views.AddressDetail.as_view())
]