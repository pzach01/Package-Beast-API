from django.urls import path
from shipments import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('shipments/', views.ShipmentList.as_view()),
    path('shipments/<int:pk>/', views.ShipmentDetail.as_view())
    path('shippo-oauth-access-token/',views.generate_shippo_oauth_token)
]