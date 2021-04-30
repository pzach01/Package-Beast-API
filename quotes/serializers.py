from rest_framework import serializers
from quotes.models import Quote
from django.http import Http404
from subscription.models import Subscription
from containers.serializers import ContainerSerializer
from arrangements.serializers import ArrangementSerializer
from items.serializers import ItemSerializerWithId
from containers.models import Container
from items.models import Item

class QuoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    arrangement=ArrangementSerializer(required=False, read_only=True)

    class Meta:
        model = Quote
        depth = 1 #this setting expands the depth of the serialized fields
        fields = ['id', 'owner', 'created', 'carrier', 'cost', 'daysToShip','serviceDescription', 'scheduledDeliveryTime','arrangement', 'shipment']
        read_only_fields = ['owner', 'created']