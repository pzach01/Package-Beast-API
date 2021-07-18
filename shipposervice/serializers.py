from rest_framework import serializers
from shipposervice.models import ShippoTransaction

class ShippoTransactionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = ShippoTransaction
        depth = 1 #this setting expands the depth of the serialized fields
        fields = ['id', 'owner', 'label_url', 'quote','objectState','status','objectCreated','objectUpdated','objectId','objectOwner','test','shippoRateId']
        read_only_fields = ['owner']