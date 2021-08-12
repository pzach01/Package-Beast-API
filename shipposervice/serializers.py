from rest_framework import serializers
from shipposervice.models import ShippoRefund, ShippoTransaction, ShippoMessage

class ShippoMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippoMessage
        fields = ['code', 'source', 'text']

class ShippoRefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippoRefund
        fields = ['id', 'owner', 'objectId', 'status', 'objectCreated', 'objectUpdated', 'objectOwner', 'test', 'transaction']

class ShippoTransactionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    messages = ShippoMessageSerializer(many=True, read_only=True)
    refund = ShippoRefundSerializer(many=False, read_only=True)

    class Meta:
        model = ShippoTransaction
        depth = 1 #this setting expands the depth of the serialized fields
        fields = ['id', 'owner', 'label_url', 'messages', 'quote','objectState','status','objectCreated','objectUpdated','objectId','objectOwner', 'rate', 'trackingNumber', 'trackingStatus', 'trackingUrlProvider', 'test','shippoRateId', 'refund']
        read_only_fields = ['owner']

