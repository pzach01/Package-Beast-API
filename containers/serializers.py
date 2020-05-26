from rest_framework import serializers
from containers.models import Container


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['id', 'arrangement', 'sku', 'description',
                  'height', 'width', 'length', 'volume', 'units']
        read_only_fields = ['arrangement', 'volume']

    def create(self, validated_data):
        container = Container.objects.create(**validated_data)
        container.volume = validated_data['height'] * \
            validated_data['width']*validated_data['length']
        container.save()
        return container

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
