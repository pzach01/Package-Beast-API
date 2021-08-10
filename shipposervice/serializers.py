from rest_framework import serializers
from shipposervice.models import ShippoTransaction, ShippoMessage

class ShippoMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippoMessage
        fields = ['code', 'source', 'text']

class ShippoTransactionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    messages = ShippoMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ShippoTransaction
        depth = 1 #this setting expands the depth of the serialized fields
        fields = ['id', 'owner', 'label_url', 'messages', 'quote','objectState','status','objectCreated','objectUpdated','objectId','objectOwner', 'rate', 'trackingNumber', 'trackingStatus', 'test','shippoRateId']
        read_only_fields = ['owner']