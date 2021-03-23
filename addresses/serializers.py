from rest_framework import serializers
from addresses.models import Address

class AddressSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Address
        # depth = 1 #this setting expands the depth of the serialized fields
        fields = ['id', 'owner', 'addressLine1', 'addressLine2', 'city', 'stateProvince', 'postalCode']
        read_only_fields = ['owner', 'created']