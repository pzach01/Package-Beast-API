from rest_framework import serializers
from arrangements.models import Arrangement
from django.utils.timezone import now
from arrangements.Box_Stuff_Python3_Only import box_stuff2 as optimize

from users.models import User
from users.serializers import UserSerializer
from containers.serializers import ContainerSerializer
from items.serializers import ItemSerializer, ItemSerializerWithId
from items.models import Item
from containers.models import Container
from .Box_Stuff_Python3_Only import box_stuff2 as bp
from subscription.models import Subscription
from django.http import Http404



class ArrangementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    containers = ContainerSerializer(many=True)
    items = ItemSerializerWithId(many=True)
    timeoutDuration = serializers.IntegerField(write_only=True, min_value=1, max_value=55)

    class Meta:
        model = Arrangement
        fields = ['id', 'created', 'owner', 'arrangementPossible', 'timeout', 'multiBinPack', 'timeoutDuration', 'containers', 'items']
        read_only_fields = ['arrangementPossible', 'timeout']       
    def format_as_dimensions(self,x,y,z):
        return str(x)+'x'+str(y)+'x'+str(z)
    def convert_to_inches(self,x,y,z,units):
        if units == "in":
            return x,y,z,"in"
        if units == "mm":
            return x/25.4, y/25.4, z/25.4, "in"
        if units == "cm":
            return x/2.54, y/2.54, z/2.54, "in"

    def create(self, validated_data):
        userSubscription=Subscription.objects.filter(owner=validated_data['owner'])[0]
        if not(userSubscription.userCanCreateArrangment):
            raise Http404

        containers = validated_data.pop('containers')
        items = validated_data.pop('items')
        timeoutDuration = validated_data.pop('timeoutDuration')
        arrangement = Arrangement.objects.create(**validated_data)
        multiBinPack = arrangement.multiBinPack

        containerStrings = []
        itemStrings = []
        itemIds=[]
        for container in containers:
            x,y,z = container['xDim'], container['yDim'], container['zDim']
            as_string=self.format_as_dimensions(x,y,z)

            containerStrings.append(as_string)
        for item in items:
            item['height'], item['length'], item['width'], item['units'] = self.convert_to_inches(item['height'], item['length'], item['width'], item['units'])
            item['xDim'],item['yDim'],item['zDim'] = item['height'],item['length'],item['width']
            x,y,z= item['xDim'], item['yDim'], item['zDim']
            as_string=self.format_as_dimensions(x,y,z)

            itemStrings.append(as_string)
            itemIds.append(item['id'])
        #increment the amount of shipments the user has used
        userSubscription.increment_shipment_requests()
        apiObjects,timedout,arrangementPossible = bp.master_calculate_optimal_solution(
            containerStrings, itemStrings, timeoutDuration, multiBinPack,itemIds)
        
        arrangement.timeout = timedout
        arrangement.arrangementPossible = arrangementPossible

        containerList = []
        index=0
        for container in containers:
            if (not arrangementPossible) or timedout:
                xDim = container['xDim']
                yDim = container['yDim']
                zDim = container['zDim']
            else:
                xDim = apiObjects[index].xDim
                yDim = apiObjects[index].yDim
                zDim = apiObjects[index].zDim
                index+=1
            sku = container['sku']
            description = container['description']
            units = container['units']
            volume = xDim*yDim*zDim
            containerList.append(Container.objects.create(arrangement=arrangement, xDim=xDim, yDim=yDim, zDim=zDim, volume=volume,
                                                        owner=validated_data['owner'], sku=sku, description=description, units=units))
        index = 0


        if not timedout and arrangementPossible:
            for container in apiObjects:
                for item in container.boxes:
                    xDim = item.xDim
                    yDim = item.yDim
                    zDim = item.zDim
                    volume = item.xDim*item.yDim*item.zDim
                    xCenter = item.x
                    yCenter = item.y
                    zCenter = item.z
                    # fields we don't want to expose to optimization code are reinitialized here
                    itemId = item.id

                    foundItem=None
                    for lowerItem in items:
                        if lowerItem['id']==itemId:
                            foundItem=lowerItem
                            break
                    if foundItem==None:
                        raise Exception("clearly a bug")
                    assert(itemId==foundItem['id'])

                    masterItemId=foundItem['id']
                    height = foundItem['height']
                    width = foundItem['width']
                    length = foundItem['length']
                    sku = foundItem['sku']
                    description = foundItem['description']
                    units = foundItem['units']
                    Item.objects.create(xDim=xDim, yDim=yDim, zDim=zDim, volume=volume, container=containerList[container.id], arrangement=arrangement,
                                        owner=validated_data['owner'], xCenter=xCenter, yCenter=yCenter, zCenter=zCenter, sku=sku, description=description, units=units, masterItemId=masterItemId, width=width, length=length, height=height)
                    index += 1
        else:
            for item in items:
                volume = item['width']*item['length']*item['height']
                Item.objects.create(xDim=item['width'], yDim=item['length'], zDim=item['height'], volume=volume,container=None, arrangement=arrangement, owner=validated_data['owner'], xCenter=0, yCenter=0, zCenter=0, sku=item['sku'], description=item['description'], units=item['units'], width=item['width'], length=item['length'], height=item['height'])

        return arrangement

    def update(self, instance, validated_data):

        # This doesn't work but I will fix it once we have the create method working

        instance.save()
        return instance
