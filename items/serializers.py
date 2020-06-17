from rest_framework import serializers
from items.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'container', 'arrangement', 'sku', 'description', 'xDim',
                  'yDim', 'zDim', 'volume', 'xCenter', 'yCenter', 'zCenter', 'units']
        read_only_fields = ['container', 'arrangement',
                            'volume', 'xCenter', 'yCenter', 'zCenter']

    def create(self, validated_data):
        item = Item.objects.create(**validated_data)

        item.volume = validated_data['xDim'] * \
            validated_data['yDim']*validated_data['zDim']
        item.save()
        return item

    def update(self, instance, validated_data):
        instance.sku = validated_data.get('sku', instance.sku)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.xDim = validated_data.get('xDim', instance.xDim)
        instance.yDim = validated_data.get('yDim', instance.yDim)
        instance.zDim = validated_data.get('zDim', instance.zDim)
        instance.volume = instance.xDim * instance.yDim * instance.zDim
        instance.save()
        return instance
