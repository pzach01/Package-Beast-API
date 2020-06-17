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
        fields = ['id', 'owner', 'multiBinPack', 'created',
                  'containers', 'items']

    def create(self, validated_data):
        containers = validated_data.pop('containers')
        items = validated_data.pop('items')
        arrangement = Arrangement.objects.create(**validated_data)
        multiBinPack = arrangement.multiBinPack

        # this string formatting will be replaced with something less stupid
        containerStrings = []
        itemStrings = []
        for container in containers:
            l, w, h = container['xDim'], container['yDim'], container['zDim']
            containerStrings.append(str(l)+'x'+str(w)+'x'+str(h))
        for item in items:
            l, w, h = item['xDim'], item['yDim'], item['zDim']
            itemStrings.append(str(l)+'x'+str(w)+'x'+str(h))

        from .Box_Stuff_Python3_Only import box_stuff2 as bp
        timeout = 0
        apiObjects = bp.master_calculate_optimal_solution(
            containerStrings, itemStrings, timeout,multiBinPack)
        # print(apiObjects[0].to_string())

        # This is where we can call calculate optimal soution, passing in items and containers.
        # Note, items and containers are both ordered dictionary lists now, not strings.
        # Their length, width, height, x, y, z, and the item's container need to be modified before
        # creating in database with .create method as shown below
        # See model definitions in items.models and containers.models for additional info
        containerList = []
        index = 0
        for container in containers:
            xDim = apiObjects[index].xDim
            yDim = apiObjects[index].yDim
            zDim = apiObjects[index].zDim
            volume = apiObjects[index].volume
            sku = container['sku']
            description = container['description']
            units = container['units']
            containerList.append(Container.objects.create(arrangement=arrangement, xDim=xDim, yDim=yDim, zDim=zDim, volume=volume,
                                                          owner=validated_data['owner'], sku=sku, description=description, units=units))
            index += 1

        index = 0
        for container in apiObjects:
            for item in container.boxes:
                xDim = item.xDim
                yDim = item.yDim
                zDim = item.zDim
                volume = item.volume
                xCenter = item.x
                yCenter = item.y
                zCenter = item.z
                sku = items[index]['sku']
                description = items[index]['description']
                units = items[index]['units']
                Item.objects.create(xDim=xDim, yDim=yDim, zDim=zDim, volume=volume, container=containerList[container.id], arrangement=arrangement,
                                    owner=validated_data['owner'], xCenter=xCenter, yCenter=yCenter, zCenter=zCenter, sku=sku, description=description, units=units)
                index += 1
        return arrangement

    def update(self, instance, validated_data):

        # This doesn't work but I will fix it once we have the create method working

        instance.save()
        return instance
