from django.urls import path

from payment import views


urlpatterns = [
    path('payment/stripeInvoice/', views.my_webhook_view),
    path('payment/createStripeSubscription/', views.create_stripe_subscription),
    path('payment/retryStripeSubscription/', views.retry_stripe_subscription),
    path('payment/userHasStripeSubscription',views.user_has_stripe_subscription)
]
