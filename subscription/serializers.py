from rest_framework import serializers
from subscription.models import Subscription

class SubscriptionSerializer(serializers.Serializer):

    class Meta:
        model=Subscription  
        fields=['id','subscriptionType','numRequestsLeft','numItemsCanAdd','numContainersCanAdd','lastUpdateAbsoluteTime', 'itemsUsed']


class InvoiceIdSerializer(serializers.Serializer):
    class Meta:
        model=InvoiceId
        fields=['id','created','stripeInvoiceId']