from rest_framework import serializers
from arrangements.models import Arrangement
from django.utils.timezone import now
from arrangements.Box_Stuff_Python3_Only import box_stuff2 as optimize

from users.models import User
from users.serializers import UserSerializer
from containers.serializers import ContainerSerializer
from items.serializers import ItemSerializer
from items.models import Item
from containers.models import Container


class ArrangementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    containers = ContainerSerializer(many=True)
    items = ItemSerializer(many=True)

    class Meta:
        model = Arrangement
        fields = ['id', 'owner', 'created', 'containers', 'items']

    def create(self, validated_data):
        containers = validated_data.pop('containers')
        items = validated_data.pop('items')
        arrangement = Arrangement.objects.create(**validated_data)

        # This is where we can call calculate optimal soution, passing in items and containers.
        # Note, items and containers are both ordered dictionary lists now, not strings.
        # Their length, width, height, x, y, z, and the item's container need to be modified before
        # creating in database with .create method as shown below
        # See model definitions in items.models and containers.models for additional info

        for container in containers:
            Container.objects.create(arrangement=arrangement,
                                     owner=validated_data['owner'], **container)

        #also, container=container
        for item in items:
            Item.objects.create(arrangement=arrangement,
                                owner=validated_data['owner'], **item)
        return arrangement

    def update(self, instance, validated_data):

        # This doesn't work but I will fix it once we have the create method working

        instance.save()
        return instance
