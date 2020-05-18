from rest_framework import serializers
from items.models import Item

class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        ref_name = 'myItems'
        fields = ['id', 'sku', 'description', 'height', 'width', 'length', 'volume']
        read_only_fields = ['volume']

    def create(self, validated_data):
        item = Item.objects.create(**validated_data)
        item.volume = validated_data['height']*validated_data['width']*validated_data['length']
        item.save()
        return box

    def update(self, instance, validated_data):
        instance.sku = validated_data.get('sku', instance.height)
        instance.description = validated_data.get('description', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.width = validated_data.get('width', instance.width)
        instance.length = validated_data.get('length', instance.length)
        instance.volume = instance.length * instance.width * instance.height
        instance.save()
        return instance