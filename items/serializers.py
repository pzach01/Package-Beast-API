from rest_framework import serializers
from items.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'container', 'arrangement', 'sku', 'description', 'height',
                  'width', 'length', 'volume', 'xCenter', 'yCenter', 'zCenter', 'units']
        read_only_fields = ['container', 'arrangement',
                            'volume', 'xCenter', 'yCenter', 'zCenter']

    def create(self, validated_data):
        item = Item.objects.create(**validated_data)
        item.volume = validated_data['height'] * \
            validated_data['width']*validated_data['length']
        item.save()
        return item

    def update(self, instance, validated_data):
        instance.sku = validated_data.get('sku', instance.height)
        instance.description = validated_data.get(
            'description', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.width = validated_data.get('width', instance.width)
        instance.length = validated_data.get('length', instance.length)
        instance.volume = instance.length * instance.width * instance.height
        instance.save()
        return instance
