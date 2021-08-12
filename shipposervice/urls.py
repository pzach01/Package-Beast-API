from django.urls import path
from shipposervice import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('shippo-oauth-access-token/',views.generate_shippo_oauth_token),
    path('shippo-transaction/',views.generate_shippo_transaction),
    path('refund-shippo-transaction/',views.refund_shippo_transaction)
]