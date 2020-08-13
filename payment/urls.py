from django.urls import path

from payment import views


urlpatterns = [
    path('payment/stripeInvoice/', views.my_webhook_view),
]