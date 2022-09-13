from shipposervice.serializers import ShippoTransactionSerializer
from rest_framework import serializers
from quotes.models import Quote, ServiceLevel
from arrangements.serializers import ArrangementSerializer, SimpleArrangementSerializer

class ServiceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLevel
        fields = ['name','token','terms']

class SimpleQuoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    arrangement=SimpleArrangementSerializer(required=False, read_only=True)
    shippoTransaction=ShippoTransactionSerializer(required=False, read_only=True)
    serviceLevel=ServiceLevelSerializer(required=False, read_only=True)
    class Meta:
        model = Quote
        depth = 1 #this setting expands the depth of the serialized fields
        fields = ['id', 'owner', 'created', 'carrier', 'cost', 'daysToShip','serviceDescription', 'scheduledDeliveryTime','arrangement', 'shipment','shippoRateId', 'shippoTransaction','serviceLevel']
        read_only_fields = ['owner', 'created']

class QuoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    arrangement=ArrangementSerializer(required=False, read_only=True)
    shippoTransaction=ShippoTransactionSerializer(required=False, read_only=True)
    serviceLevel=ServiceLevelSerializer(required=False, read_only=True)
    class Meta:
        model = Quote
        depth = 1 #this setting expands the depth of the serialized fields
        fields = ['id', 'owner', 'created', 'carrier', 'cost', 'daysToShip','serviceDescription', 'scheduledDeliveryTime','arrangement', 'shipment','shippoRateId', 'shippoTransaction','serviceLevel']
        read_only_fields = ['owner', 'created']