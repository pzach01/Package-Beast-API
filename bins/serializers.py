from rest_framework import serializers
from bins.models import Bin

class BinListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        ref_name = 'myBins'
        fields = ['id', 'height', 'width', 'length', 'volume']
        read_only_fields = ['volume']

    def create(self, validated_data):
        a_bin = Bin.objects.create(**validated_data)
        a_bin.volume = validated_data['height']*validated_data['width']*validated_data['length']
        return a_bin

    def update(self, instance, validated_data):
        instance.height = validated_data.get('height', instance.height)
        instance.width = validated_data.get('width', instance.width)
        instance.length = validated_data.get('length', instance.length)
        instance.volume = instance.length * instance.width * instance.height
        return instance