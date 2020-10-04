from rest_framework import serializers
from items.models import Item
from django.http import Http404


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'container', 'arrangement', 'sku', 'description', 'length', 'width', 'height', 'xDim',
                  'yDim', 'zDim', 'volume', 'xCenter', 'yCenter', 'zCenter', 'units', 'masterItemId']
        read_only_fields = ['container', 'arrangement',
                            'volume', 'xCenter', 'yCenter', 'zCenter', 'xDim', 'yDim', 'zDim', 'masterItemId']

    def create(self, validated_data):
        userSubscription=Subscription.objects.filter(owner=validated_data['owner'])[0]
        if not(userSubscription.userCanCreateItem):
            raise Http404
        item = Item.objects.create(**validated_data)

        item.volume = validated_data['length'] * 
            validated_data['width']*validated_data['height']
        item.masterItemId = item.id
        item.save()
        return item

    def update(self, instance, validated_data):
        instance.sku = validated_data.get('sku', instance.sku)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.length = validated_data.get('length', instance.length)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.volume = instance.length * instance.width * instance.height
        instance.units = validated_data.get('units', instance.units)
        instance.save()
        return instance

class ItemSerializerWithId(ItemSerializer):
    id = serializers.IntegerField(required=True)

    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields+['id']