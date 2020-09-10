from django.urls import path

from payment import views


urlpatterns = [
    path('payment/stripeInvoice/', views.my_webhook_view),
    path('payment/createStripeSubscription/', views.create_stripe_subscription),
    path('payment/retryInvoice/', views.retry_invoice),
    path('payment/getSubscriptionInfo/',views.get_subscription_info),
    path('payment/cancelStripeSubscription/',views.cancel_subscription),
    path('payment/updateStripeSubscription/',views.update_stripe_subscription),
]


