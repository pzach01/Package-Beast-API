from rest_framework import serializers
from shipments.models import Shipment
from django.http import Http404
from subscription.models import Subscription
from containers.serializers import ContainerSerializer
from arrangements.serializers import ArrangementSerializer
from items.serializers import ItemSerializerWithId
from containers.models import Container
from arrangements.models import Arrangement
from items.models import Item
from addresses.serializers import AddressSerializer
from addresses.models import Address
from rest_framework import serializers
from addresses.serializers import AddressSerializer
from libs.Box_Stuff_Python3_Only import box_stuff2 as bp
class ShipmentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    containers = ContainerSerializer(many=True, write_only=True)
    items = ItemSerializerWithId(many=True, write_only=True)
    arrangements=ArrangementSerializer(many=True, required=False, read_only=True)
    timeout = serializers.IntegerField(write_only=True, min_value=1, max_value=55)

    class Meta:
        model = Shipment
        depth=1
        fields = ['id', 'owner', 'created', 'title', 'lastSelectedQuoteId', 'items', 'containers','arrangements', 'multiBinPack', 'arrangementPossible', 'timeout', 'shipFromAddress', 'shipToAddress', 'quotes']
        read_only_fields = ['owner', 'created', 'arrangementPossible', 'timeout','arrangements']
    # note that these two methods are found in the arrangments serializer (quite sloppily)
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
        containers = validated_data.pop('containers')
        items = validated_data.pop('items')
        timeoutDuration=validated_data.pop('timeout')
        lastSelectedQuoteId=validated_data.pop('lastSelectedQuoteId')
        # this is actually unused (remove at future date from)
        multiBinPack=validated_data['multiBinPack']
        shipment = Shipment.objects.create(**validated_data)
        
        userSubscription=Subscription.objects.filter(owner=validated_data['owner'])[0]
        if not(userSubscription.getUserCanCreateArrangment()):
            raise Http404('user doesnt have right to create arrangement')

        containerStrings = []
        itemStrings = []
        itemIds=[]
        for container in containers:
            container['xDim'], container['yDim'], container['zDim'], container['units'] = self.convert_to_inches(container['xDim'], container['yDim'], container['zDim'], container['units'])
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
        apiObjects,timedout,arrangementPossible = bp.sieve_containers(
            containerStrings, itemStrings, timeoutDuration, multiBinPack,itemIds)
        shipment.arrangementPossible=arrangementPossible
        if not arrangementPossible:
            raise Http404('No arrangement possible. Try again with bigger containers or smaller items.')

        # similiar to running original arrangments serializer multiple times, but only creates
        # one container per arrangment
        for ele in range(0, len(apiObjects)):
            arrangement = Arrangement.objects.create(**validated_data,shipment=shipment)
            arrangement.timeout = timedout
            arrangement.arrangementPossible = arrangementPossible
            arrangement.shipment=shipment
            arrangement.save()

            containerList = []
            if (len(apiObjects[ele].boxes)>0):
                xDim = apiObjects[ele].xDim
                yDim = apiObjects[ele].yDim
                zDim = apiObjects[ele].zDim

            else:
                xDim = containers[ele]['xDim']
                yDim = containers[ele]['yDim']
                zDim = containers[ele]['zDim']
            # write a test to check this invariant and the one above (ie. containers[ele])
            sku = containers[ele]['sku']
            description = containers[ele]['description']
            units = containers[ele]['units']
            volume = xDim*yDim*zDim
            containerList.append(Container.objects.create(arrangement=arrangement, xDim=xDim, yDim=yDim, zDim=zDim, volume=volume,
                                                        owner=validated_data['owner'], sku=sku, description=description, units=units))


            if (len(apiObjects[ele].boxes)>0):
                for item in apiObjects[ele].boxes:
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
                    Item.objects.create(xDim=xDim, yDim=yDim, zDim=zDim, volume=volume, container=containerList[0], arrangement=arrangement,
                                        owner=validated_data['owner'], xCenter=xCenter, yCenter=yCenter, zCenter=zCenter, sku=sku, description=description, units=units, masterItemId=masterItemId, width=width, length=length, height=height)

            else:
                for item in items:
                    volume = item['width']*item['length']*item['height']
                    Item.objects.create(xDim=item['width'], yDim=item['length'], zDim=item['height'], volume=volume,container=None, arrangement=arrangement, owner=validated_data['owner'], xCenter=0, yCenter=0, zCenter=0, sku=item['sku'], description=item['description'], masterItemId=item['id'], units=item['units'], width=item['width'], length=item['length'], height=item['height'])
        return shipment

