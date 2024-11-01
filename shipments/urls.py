from django.urls import path
from shipments import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('shipments/', views.ShipmentList.as_view()),
    path('simpleshipments/', views.SimpleShipmentList.as_view()),
    path('shipments/<int:pk>/', views.ShipmentDetail.as_view()),
    path('simpleshipments/<int:pk>/', views.SimpleShipmentQuotesDetail.as_view())
]