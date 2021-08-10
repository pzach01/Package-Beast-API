from shipposervice.serializers import ShippoTransactionSerializer
from rest_framework import serializers
from quotes.models import Quote
from arrangements.serializers import ArrangementSerializer

class QuoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    arrangement=ArrangementSerializer(required=False, read_only=True)
    shippoTransaction=ShippoTransactionSerializer(required=False, read_only=True)
    class Meta:
        model = Quote
        depth = 1 #this setting expands the depth of the serialized fields
        fields = ['id', 'owner', 'created', 'carrier', 'cost', 'daysToShip','serviceDescription', 'scheduledDeliveryTime','arrangement', 'shipment','shippoRateId', 'shippoTransaction']
        read_only_fields = ['owner', 'created']