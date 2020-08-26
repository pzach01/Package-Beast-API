from django.urls import path

from payment import views


urlpatterns = [
    path('payment/stripeInvoice/', views.my_webhook_view),
    path('payment/createStripeSubscription/', views.create_stripe_subscription),
]
