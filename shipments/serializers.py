from quotes.serializers import QuoteSerializer, SimpleQuoteSerializer
from rest_framework import serializers
from shipments.models import Shipment
from django.http import Http404
from subscription.models import Subscription
from quotes.models import Quote, ServiceLevel
from containers.serializers import ContainerSerializer, AnalysedContainerSerializer
from arrangements.serializers import ArrangementSerializer
from items.serializers import ItemSerializerWithId
from containers.models import Container, AnalysedContainer
from arrangements.models import Arrangement
from items.models import Item
from addresses.serializers import AddressSerializer
from addresses.models import Address
from rest_framework import serializers
from libs.Box_Stuff_Python3_Only import box_stuff2 as bp
from users.models import User
import os
import shippo
import threading
from django.conf import settings


def get_shippo_shipments(SHIPPO_API_KEY, shipmentIds, production):
    import requests
    post_data = {"SHIPPO_API_KEY": SHIPPO_API_KEY, "shipmentIds": shipmentIds, "production": production}
    url = settings.SHIPPO_API_INTERFACE_FETCH_MANY_SHIPMENTS_URI
    headers = { 'content-type': "application/json" }
    response = requests.post(url, json = post_data, headers=headers)    
    import json
    shippo_shipments = json.loads(response.text)
    return shippo_shipments

def make_shippo_shipment_request(SHIPPO_API_KEY, shipFromAddress, shipToAddress, solutionContainers, production):
    import requests
    address_from = {
        "name": shipFromAddress.name,
        "street1": shipFromAddress.addressLine1,
        "street2": "",
        "city": shipFromAddress.city,
        "state": shipFromAddress.stateProvinceCode,
        "zip": shipFromAddress.postalCode,
        "country":"US",
        "phone": shipFromAddress.phoneNumber
    }
    address_to = {
        "name": shipToAddress.name,
        "street1": shipToAddress.addressLine1,
        "street2": "",
        "city": shipToAddress.city,
        "state": shipToAddress.stateProvinceCode,
        "zip": shipToAddress.postalCode,
        "country":"US",
        "phone": shipToAddress.phoneNumber
    }

    parcels = []
    for solutionContainer in solutionContainers:
        parcel = {
        "length": solutionContainer.xDim,
        "width": solutionContainer.yDim,
        "height": solutionContainer.zDim,
        "distance_unit": "in",
        "weight": solutionContainer.weight,
        "mass_unit": "lb"
        }
        parcels.append(parcel)
    
    post_data = {"SHIPPO_API_KEY": SHIPPO_API_KEY, "address_from": address_from, "address_to": address_to, "parcels": parcels, "async":True, "production": production}
    url = settings.SHIPPO_API_INTERFACE_CREATE_SHIPMENTS_URI
    headers = { 'content-type': "application/json" }
    response = requests.post(url, json = post_data, headers=headers)    
    import json
    shippo_shipments = json.loads(response.text)
    return shippo_shipments


class SimpleShipmentsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Shipment
        fields = ['id', 'owner', 'created', 'title', 'validFromAddress', 'validToAddress']

class SimpleShipmentQuotesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    quotes = SimpleQuoteSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Shipment
        depth=1
        fields = ['id', 'owner', 'created', 'title', 'validFromAddress', 'validToAddress', 'quotes']
    
    
class ShipmentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    containers = ContainerSerializer(many=True, write_only=True)
    items = ItemSerializerWithId(many=True, write_only=True)
    arrangements=ArrangementSerializer(many=True, required=False, read_only=True)
    timeoutDuration = serializers.IntegerField(write_only=True, min_value=1, max_value=55)
    shipToAddress = AddressSerializer()
    shipFromAddress = AddressSerializer()
    quotes = QuoteSerializer(many=True, required=False, read_only=True)
    analysedContainers = AnalysedContainerSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Shipment
        depth=1
        fields = ['id', 'analysedContainers', 'owner', 'created', 'title', 'lastSelectedQuoteId', 'items', 'containers','arrangements', 'multiBinPack', 'fitAllArrangementPossibleAPriori','arrangementFittingAllItemsFound', 'timeoutDuration', 'shipFromAddress', 'shipToAddress', 'quotes', 'timeout','timingInformation','validFromAddress','validToAddress','usedAllValidContainers','noValidRequests','noErrorsMakingRequests','activeThreads']
        read_only_fields = ['owner', 'analysedContainers', 'created', 'fitAllArrangementPossibleAPriori','arrangementFittingAllItemsFound', 'timeoutDuration','arrangements', 'timeout','validFromAddress','validToAddress','usedAllValidContainers','noValidRequests','noErrorsMakingRequests','activeThreads']
        

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
    def convert_to_pounds(self, weight, weightUnits):
        if weightUnits=='lb':
            return weight,'lb'
        else:
            return weight*2.205,'lb'
    def create(self, validated_data):
        import time

        startTotal=time.time()
        containers = validated_data.pop('containers')

        items = validated_data.pop('items')
        timeoutDuration=validated_data.pop('timeoutDuration')
        lastSelectedQuoteId=validated_data.pop('lastSelectedQuoteId')
        # this is actually unused (remove at future date from)
        multiBinPack=validated_data['multiBinPack']

        shipFromAddress_data = validated_data.pop('shipFromAddress')
        shipFromAddress=Address.objects.create(owner=validated_data['owner'], **shipFromAddress_data)
        shipToAddress_data = validated_data.pop('shipToAddress')
        shipToAddress=Address.objects.create(owner=validated_data['owner'], **shipToAddress_data)
        if shipFromAddress_data['country']!='United States' or shipToAddress_data['country']!='United States':
            raise serializers.ValidationError({"message":"Can't ship outside of United States. If using the web application, fill in 'United States' as your shipping address and location."})


        shipment = Shipment.objects.create(shipFromAddress=shipFromAddress, shipToAddress=shipToAddress, **validated_data)

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

        totalWeight = 0
        for item in items:
            item['height'], item['length'], item['width'], item['units'] = self.convert_to_inches(item['height'], item['length'], item['width'], item['units'])
            item['weight'], item['weightUnits']=self.convert_to_pounds(item['weight'],item['weightUnits'])
            item['xDim'],item['yDim'],item['zDim'] = item['height'],item['length'],item['width']
            x,y,z= item['xDim'], item['yDim'], item['zDim']
            as_string=self.format_as_dimensions(x,y,z)

            itemStrings.append(as_string)
            itemIds.append(item['id'])
            totalWeight += item['weight']
        
        if totalWeight > 150:
            raise serializers.ValidationError({"message":'shipment total weight exceeds limit of 150 lbs'})

        #increment the amount of shipments the user has used      
        userSubscription.increment_shipment_requests()
        sieveStart=time.time()
        # arrangementPossible= arrangementPossibleAPriori= some item that has lxwxh < some containers LXWxH exists
        # arrangementFittingAllItemsFound= there is a container that can fit all items and the corresponding arrangement has been found


        #TODO: rewire the logic for arrangmentPossible vs arrangementFittingAllItemsFound
        # arrangmenet returns partial fits; sieve doesn't but the flags returned don't indicate this
        # ie. what about when no optimal arrangmeent possible, but 
        apiObjects,timedout,fitAllArrangementPossibleAPriori,arrangementFittingAllItemsFound = bp.sieve_containers(
            containerStrings, itemStrings, timeoutDuration, multiBinPack,itemIds)
        sieveEnd=time.time()
        shipment.fitAllArrangementPossibleAPriori=fitAllArrangementPossibleAPriori
        shipment.arrangementFittingAllItemsFound=arrangementFittingAllItemsFound
        if not fitAllArrangementPossibleAPriori:
            return shipment
        if not arrangementFittingAllItemsFound:
            return shipment


        # create shippo addresses (shipFrom and shipTo)
        addressStartTime=time.time()

        user=User.objects.get(email=validated_data['owner'])
        if user.userHasShippoAccount() and (os.getenv('ENVIRONMENT_TYPE')=='PRODUCTION'):
            production = True
            shippo.config.api_key=user.shippoAccessToken
            SHIPPO_API_KEY =user.shippoAccessToken
        else:
            production = False
            shippo.config.api_key = os.getenv('SHIPPO_API_KEY')
            SHIPPO_API_KEY = os.getenv('SHIPPO_API_KEY')

        addressEndTime=time.time()
        # similiar to running original arrangments serializer multiple times, but only creates
        # one container per arrangment
        forLoopStart=time.time()
        asyncioTotal=0

        maxContainersToUse=20
        nonEmptyAPIObjects=[obj for obj in apiObjects if len(obj.boxes)>0]
        largestContainerUsed=max(nonEmptyAPIObjects, key=lambda l: abs(l.xDim*l.yDim*l.zDim))
        largestVolumeAccepted=abs(largestContainerUsed.xDim*largestContainerUsed.yDim*largestContainerUsed.zDim)
        if len(nonEmptyAPIObjects)>maxContainersToUse:
            nonEmptyAPIObjects=sorted(nonEmptyAPIObjects, key=lambda l: abs(l.xDim*l.yDim*l.zDim))
            largestContainerUsed=nonEmptyAPIObjects[maxContainersToUse-1]
            largestVolumeAccepted=abs(largestContainerUsed.xDim*largestContainerUsed.yDim*largestContainerUsed.zDim)
            shipment.usedAllValidContainers=False
            # filter the api objects so that only the smallest 'n' containers are sent to shippo 
        apiObjects=[obj for obj in apiObjects if abs(obj.xDim*obj.yDim*obj.zDim)<=largestVolumeAccepted]

        solutionContainers = []
        solutionArrangements = []
        for ele in range(0, len(apiObjects)):
            arrangement = Arrangement.objects.create(**validated_data,shipment=shipment)
            arrangement.timeout = timedout
            # later we should tie this to an actual value (per arrangement)
            arrangement.arrangementPossible = True
            arrangement.shipment=shipment
            arrangement.save()

            xDim=0
            yDim=0
            zDim=0
            if (len(apiObjects[ele].boxes)>0):
                xDim = apiObjects[ele].xDim
                yDim = apiObjects[ele].yDim
                zDim = apiObjects[ele].zDim

            else:
                raise Exception('not sure why you are in this code, doesnt necessarily bug besides this line')
                xDim = containers[ele]['xDim']
                yDim = containers[ele]['yDim']
                zDim = containers[ele]['zDim']
            # write a test to check this invariant and the one above (ie. containers[ele])
            sku = containers[ele]['sku']
            description = containers[ele]['description']
            units = containers[ele]['units']
            volume = xDim*yDim*zDim
            container = Container.objects.create(arrangement=arrangement, xDim=xDim, yDim=yDim, zDim=zDim, volume=volume,
                                                        owner=validated_data['owner'], sku=sku, description=description, units=units)
            totalWeight=0
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
                    weight=foundItem['weight']
                    weightUnits=foundItem['weightUnits']
                    Item.objects.create(xDim=xDim, yDim=yDim, zDim=zDim, volume=volume, container=container, arrangement=arrangement,
                                        owner=validated_data['owner'], xCenter=xCenter, yCenter=yCenter, zCenter=zCenter, weight=weight,weightUnits=weightUnits, sku=sku, description=description, units=units, masterItemId=masterItemId, width=width, length=length, height=height)

                    totalWeight+=weight
            else:
                raise Exception('not sure why you are in this code, doesnt necessarily bug besides this line')

            weight=totalWeight

            '''Note: this value is never saved back to the container object.
            We might want to update container model to include weight - Aug 27 2022'''
            container.weight = weight
            solutionContainers.append(container)
            solutionArrangements.append(arrangement)
            assert(not xDim==0)
            assert(not yDim==0)
            assert(not zDim==0)

        forLoopEnd=time.time()
        shipmentsReturnedFromShippo = make_shippo_shipment_request(SHIPPO_API_KEY, shipFromAddress, shipToAddress, solutionContainers, production)
        #print("shipmentsReturnedFromShippo 1: ", shipmentsReturnedFromShippo)
        
        if "messages" in shipmentsReturnedFromShippo:
            if shipmentsReturnedFromShippo['messages'][0]=='error making request':
                shipment.noErrorsMakingRequests=False
                shipment.save()
            if shipmentsReturnedFromShippo['messages'][0]=='error creating shippo Shipment':
                shipment.validFromAddress=False
                shipment.validToAddress=False
                shipment.save()
            if shipmentsReturnedFromShippo['messages'][0]=='invalid from address':
                shipment.validFromAddress=False
                shipment.save()
            if shipmentsReturnedFromShippo['messages'][0]=='invalid to address':
                shipment.validToAddress=False
                shipment.save()
            if shipmentsReturnedFromShippo['messages'][0]=='same from and to addresses':
                shipment.validFromAddress=False
                shipment.validToAddress=False
                shipment.save()
            raise serializers.ValidationError({"message":shipmentsReturnedFromShippo['messages'][0]})

            

        shippoShipmentIds = []

        for shipmentReturnedFromShippo in shipmentsReturnedFromShippo:
            shippoShipmentIds.append(shipmentReturnedFromShippo['object_id'])

        spinlockStart=time.time()
        shipmentsReturnedFromShippo = get_shippo_shipments(SHIPPO_API_KEY, shippoShipmentIds, production)
        #print("shipmentsReturnedFromShippo 2: ", shipmentsReturnedFromShippo)
        spinlockEnd=time.time()

            
        quoteCreationStart=time.time()

        for i, shipmentReturnedFromShippo in enumerate(shipmentsReturnedFromShippo):
            rates = shipmentReturnedFromShippo['rates']
            for rate in rates:
                q=Quote.objects.create(owner=validated_data['owner'],shipment=shipment, arrangement=solutionArrangements[i],carrier=rate['provider'],cost=float(rate['amount']),serviceDescription=rate['servicelevel']['name'],daysToShip=rate['estimated_days'],scheduledDeliveryTime=rate['duration_terms'],shippoRateId=rate['object_id'])
                ServiceLevel.objects.create(name=rate['servicelevel']['name'],token=rate['servicelevel']['token'],terms=rate['servicelevel']['terms'],quote=q)
        quoteCreationEnd=time.time()
        
        endTotal=time.time()
        quoteCreationTotal=quoteCreationEnd-quoteCreationStart
        spinlockTotal=spinlockEnd-spinlockStart
        totalTime=endTotal-startTotal
        sieveTotal=sieveEnd-sieveStart
        addressCreationTotal=addressEndTime-addressStartTime
        forLoopTime=forLoopEnd-forLoopStart
        shipment.timingInformation=str(totalTime)+";"+str(spinlockTotal)+";"+str(quoteCreationTotal)+";"+str(addressCreationTotal)+";"+str(sieveTotal)+";"+str(forLoopTime)+";"+str(asyncioTotal)
        shipment.activeThreads=threading.active_count()
        shipment.save()

        for c in containers:
            c['xDim'], c['yDim'], c['zDim'], c['units'] = self.convert_to_inches(c['xDim'], c['yDim'], c['zDim'], c['units'])
            # Volume is a read only field so we need to populate it
            volume = c['xDim']*c['yDim']*c['zDim']
            AnalysedContainer.objects.create(**c, volume = volume, owner=validated_data['owner'], shipment = shipment)
            
        return shipment