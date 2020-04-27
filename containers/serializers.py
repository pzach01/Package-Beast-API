from rest_framework import serializers
from containers.models import Container

class ContainerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        ref_name = 'myContainers'
        fields = ['id', 'height', 'width', 'length', 'volume']
        read_only_fields = ['volume']

    def create(self, validated_data):
        a_bin = Container.objects.create(**validated_data)
        a_bin.volume = validated_data['height']*validated_data['width']*validated_data['length']
        return a_bin

    def update(self, instance, validated_data):
        instance.height = validated_data.get('height', instance.height)
        instance.width = validated_data.get('width', instance.width)
        instance.length = validated_data.get('length', instance.length)
        instance.volume = instance.length * instance.width * instance.height
        return instance