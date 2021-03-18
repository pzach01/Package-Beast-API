from rest_framework import serializers
from shipments.models import Shipment
from django.http import Http404
from subscription.models import Subscription
from containers.serializers import ContainerSerializer
from items.serializers import ItemSerializerWithId
from containers.models import Container
from items.models import Item

class ShipmentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    containers = ContainerSerializer(many=True)
    items = ItemSerializerWithId(many=True)
    class Meta:
        model = Shipment
        fields = ['id', 'owner', 'created', 'title', 'lastSelectedQuoteId', 'items', 'containers', 'multiBinPack', 'arrangementPossible', 'timeout']
        read_only_fields = ['owner', 'created', 'arrangementPossible', 'timeout']
    def create(self, validated_data):
        containers = validated_data.pop('containers')
        items = validated_data.pop('items')
        shipment = Shipment.objects.create(**validated_data)
        for container in containers:
            volume = container['xDim']*container['yDim']*container['zDim']
            Container.objects.create(shipment = shipment, xDim=container['xDim'], yDim=container['yDim'], zDim=container['zDim'], volume=volume, owner=validated_data['owner'], sku=container['sku'], description=container['description'], units=container['units'])
        for item in items:
            Item.objects.create(shipment = shipment, owner=validated_data['owner'], xCenter=0, yCenter=0, zCenter=0, sku=item['sku'], description=item['description'], units=item['units'], width=item['width'], length=item['length'], height=item['height'])

        return shipment
