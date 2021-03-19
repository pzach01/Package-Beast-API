from rest_framework import serializers
from containers.models import Container
from django.http import Http404
from subscription.models import Subscription


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['id', 'arrangement', 'sku', 'description',
                  'xDim', 'yDim', 'zDim', 'volume', 'units', 'shipment']
        read_only_fields = ['arrangement', 'volume', 'shipment']

    def create(self, validated_data):
        userSubscription=Subscription.objects.filter(owner=validated_data['owner'])[0]
        if not(userSubscription.getUserCanCreateContainer()):
            raise Http404('user doesnt have right to create container')
        container = Container.objects.create(**validated_data)
        container.volume = validated_data['xDim'] * \
            validated_data['yDim']*validated_data['zDim']
        container.save()
        return container

    def update(self, instance, validated_data):
        instance.sku = validated_data.get('sku', instance.sku)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.xDim = validated_data.get('xDim', instance.xDim)
        instance.yDim = validated_data.get('yDim', instance.yDim)
        instance.zDim = validated_data.get('zDim', instance.zDim)
        instance.volume = instance.xDim * instance.yDim * instance.zDim
        instance.units = validated_data.get('units', instance.units)
        instance.save()
        return instance
