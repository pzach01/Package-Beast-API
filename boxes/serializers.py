from rest_framework import serializers
from boxes.models import Box

class BoxListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        ref_name = 'myBoxes'
        fields = ['id', 'height', 'width', 'length', 'volume']
        read_only_fields = ['volume']

    def create(self, validated_data):
        box = Box.objects.create(**validated_data)
        box.volume = validated_data['height']*validated_data['width']*validated_data['length']
        return box

    def update(self, instance, validated_data):
        instance.height = validated_data.get('height', instance.height)
        instance.width = validated_data.get('width', instance.width)
        instance.length = validated_data.get('length', instance.length)
        instance.volume = instance.length * instance.width * instance.height
        return instance