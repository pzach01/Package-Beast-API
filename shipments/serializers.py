from quotes.serializers import QuoteSerializer
from rest_framework import serializers
from shipments.models import Shipment
from django.http import Http404
from subscription.models import Subscription
from quotes.models import Quote, ServiceLevel
from containers.serializers import ContainerSerializer
from arrangements.serializers import ArrangementSerializer
from items.serializers import ItemSerializerWithId
from containers.models import Container
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
import multiprocessing
from multiprocessing import Pool

def request_spinlock(requestsArrangementPair):
    import time
    import random
    endTime=time.time()+15

    request=None
    requestId=requestsArrangementPair[0]
    arrangement=requestsArrangementPair[1]
    while(True):
        request=shippo.Shipment.retrieve(requestId)
        if request['status']=='SUCCESS':
            break
        if time.time()>endTime:
            return ('', arrangement)
        time.sleep(2+random.random())
        # try to prevent all the threads from hitting at same time (since they are spawned like this)


    rates=request['rates']

    quotesAsTuplesShippo=[]
    for rate in rates:
        rateId=rate['object_id']
        #(carrier,cost,serviceDescription, guranteedDaysToDelivery,scheduledDeliveryTime)
        serviceLevel=rate['servicelevel']
        serviceToken=serviceLevel['token']
        serviceTerms=serviceLevel['terms']
        t=(rate['provider'],rate['amount'],rate['servicelevel']['name'],rate['estimated_days'],rate['duration_terms'],rateId,serviceToken,serviceTerms)
        quotesAsTuplesShippo.append(t)
    return (quotesAsTuplesShippo,arrangement)




def make_rates_request_async(inputTuple):
    arrangement,weight,xDim,yDim,zDim,addressFromTuple,addressToTuple=inputTuple[0],inputTuple[1],inputTuple[2],inputTuple[3],inputTuple[4],inputTuple[5],inputTuple[6]
    import shippo
    from shippo.error import APIError
    try:
        addressFrom = shippo.Address.create(
            name = addressFromTuple[0],
            street1 = addressFromTuple[1],
            city = addressFromTuple[2],
            state = addressFromTuple[3],
            zip = addressFromTuple[4],
            country = "US",
            phone = addressFromTuple[5],
            validate = True
        )
    except APIError as e:
        return 'error making request'

    try:
        addressTo = shippo.Address.create(
            name = addressToTuple[0],
            street1 = addressToTuple[1],
            city = addressToTuple[2],
            state = addressToTuple[3],
            zip = addressToTuple[4],
            country = "US",
            phone = addressFromTuple[5],
            validate = True
        )
    except APIError as e:
        return 'error making request'       
    if not addressFrom['validation_results']['is_valid']:
        return "invalid from address"
    if not addressTo['validation_results']['is_valid']:
        return "invalid to address"



    if '.' in weight:
        weight=weight[0: (weight.index('.')+5)]
    if '.' in xDim:
        xDim=xDim[0: (xDim.index('.')+5)]
    if '.' in yDim:
        yDim=yDim[0: (yDim.index('.')+5)]
    if '.' in zDim:
        zDim=zDim[0: (zDim.index('.')+5)]



    parcel = {
        "length": xDim,
        "width": yDim,
        "height": zDim,
        "distance_unit": "in",
        "weight": weight,
        "mass_unit": "lb"
    }
    try:
        request = shippo.Shipment.create(
            address_from = addressFrom,
            address_to = addressTo,
            parcels = [parcel],
            asynchronous = True
        )
    except APIError as e:
        return 'error making request'      
    except:
        return "error creating shippo Shipment"
    return (request['object_id'], arrangement)

class SimpleShipmentsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Shipment
        fields = ['id', 'owner', 'created', 'title', 'validFromAddress', 'validToAddress']
    

class ShipmentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    containers = ContainerSerializer(many=True, write_only=True)
    items = ItemSerializerWithId(many=True, write_only=True)
    arrangements=ArrangementSerializer(many=True, required=False, read_only=True)
    timeoutDuration = serializers.IntegerField(write_only=True, min_value=1, max_value=55)
    shipToAddress = AddressSerializer()
    shipFromAddress = AddressSerializer()
    quotes = QuoteSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Shipment
        depth=1
        fields = ['id', 'owner', 'created', 'title', 'lastSelectedQuoteId', 'items', 'containers','arrangements', 'multiBinPack', 'fitAllArrangementPossibleAPriori','arrangementFittingAllItemsFound', 'timeoutDuration', 'shipFromAddress', 'shipToAddress', 'quotes', 'timeout','timingInformation','validFromAddress','validToAddress','usedAllValidContainers','noValidRequests','noErrorsMakingRequests','activeThreads']
        read_only_fields = ['owner', 'created', 'fitAllArrangementPossibleAPriori','arrangementFittingAllItemsFound', 'timeoutDuration','arrangements', 'timeout','validFromAddress','validToAddress','usedAllValidContainers','noValidRequests','noErrorsMakingRequests','activeThreads']
        

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

        for item in items:
            item['height'], item['length'], item['width'], item['units'] = self.convert_to_inches(item['height'], item['length'], item['width'], item['units'])
            item['weight'], item['weightUnits']=self.convert_to_pounds(item['weight'],item['weightUnits'])
            item['xDim'],item['yDim'],item['zDim'] = item['height'],item['length'],item['width']
            x,y,z= item['xDim'], item['yDim'], item['zDim']
            as_string=self.format_as_dimensions(x,y,z)

            itemStrings.append(as_string)
            itemIds.append(item['id'])
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
        shipToAttentionName=shipToAddress.name
        shipToPhoneNumber=shipToAddress.phoneNumber
        shipToAddressLineOne=shipToAddress.addressLine1
        shipToCity=shipToAddress.city
        shipToStateProvinceCode=shipToAddress.stateProvinceCode
        shipToPostalCode=shipToAddress.postalCode


        shipFromAttentionName=shipFromAddress.name
        shipFromPhoneNumber=shipFromAddress.phoneNumber
        shipFromAddressLineOne=shipFromAddress.addressLine1
        shipFromCity=shipFromAddress.city
        shipFromStateProvinceCode=shipFromAddress.stateProvinceCode
        shipFromPostalCode=shipFromAddress.postalCode

        user=User.objects.get(email=validated_data['owner'])
        if user.userHasShippoAccount() and (os.getenv('ENVIRONMENT_TYPE')=='PRODUCTION'):
            shippo.config.api_key=user.shippoAccessToken
        else:
            shippo.config.api_key = os.getenv('SHIPPO_API_KEY')


        addressEndTime=time.time()
        # similiar to running original arrangments serializer multiple times, but only creates
        # one container per arrangment
        forLoopStart=time.time()
        asyncioTotal=0
        inputTuples=[]


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

        for ele in range(0, len(apiObjects)):
            arrangement = Arrangement.objects.create(**validated_data,shipment=shipment)
            arrangement.timeout = timedout
            # later we should tie this to an actual value (per arrangement)
            arrangement.arrangementPossible = True
            arrangement.shipment=shipment
            arrangement.save()

            containerList = []

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
            containerList.append(Container.objects.create(arrangement=arrangement, xDim=xDim, yDim=yDim, zDim=zDim, volume=volume,
                                                        owner=validated_data['owner'], sku=sku, description=description, units=units))
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
                    Item.objects.create(xDim=xDim, yDim=yDim, zDim=zDim, volume=volume, container=containerList[0], arrangement=arrangement,
                                        owner=validated_data['owner'], xCenter=xCenter, yCenter=yCenter, zCenter=zCenter, weight=weight,weightUnits=weightUnits, sku=sku, description=description, units=units, masterItemId=masterItemId, width=width, length=length, height=height)

                    totalWeight+=weight
            else:
                raise Exception('not sure why you are in this code, doesnt necessarily bug besides this line')
                for item in items:
                    volume = item['width']*item['length']*item['height']
                    Item.objects.create(xDim=item['width'], yDim=item['length'], zDim=item['height'],weight=item['weight'],weightUnits=item['weightUnits'], volume=volume,container=None, arrangement=arrangement, owner=validated_data['owner'], xCenter=0, yCenter=0, zCenter=0, sku=item['sku'], description=item['description'], masterItemId=item['id'], units=item['units'], width=item['width'], length=item['length'], height=item['height'])

                    # this line maybe shouldnt be here
                    totalWeight+=item['weightUnits']


            weight=totalWeight
            assert(not xDim==0)
            assert(not yDim==0)
            assert(not zDim==0)

            xDim=str(xDim)
            yDim=str(yDim)
            zDim=str(zDim)

            addressFromTuple=(shipFromAttentionName,shipFromAddressLineOne,shipFromCity,shipFromStateProvinceCode,shipFromPostalCode, shipFromPhoneNumber)
            addressToTuple=(shipToAttentionName, shipToAddressLineOne, shipToCity, shipToStateProvinceCode, shipToPostalCode, shipToPhoneNumber)
            inputTuple=(arrangement,str(weight),xDim,yDim,zDim,addressFromTuple, addressToTuple)
            inputTuples.append(inputTuple)

        forLoopEnd=time.time()


        poolsToMake=min(4,len(inputTuples))

        requestsAndArrangementsPairs=[]
        with Pool(poolsToMake) as p:
            requestsAndArrangementsPairs=p.map(make_rates_request_async, inputTuples)
        for asyncResult in requestsAndArrangementsPairs:
            if asyncResult=='error making request':
                shipment.noErrorsMakingRequests=False
                shipment.save()
            if asyncResult=='error creating shippo Shipment':
                shipment.validFromAddress=False
                shipment.validToAddress=False
                shipment.save()
                return shipment
            if asyncResult=='invalid from address':
                shipment.validFromAddress=False
                shipment.save()
                return shipment
            if asyncResult=='invalid to address':
                shipment.validToAddress=False
                shipment.save()
                return shipment
        # note that for this code to work correctly loops.run_until_complete (and async_handler) must return the methods in the order they were input
        # (it does this in testing)

        # give shippo 3 secs of lead time to make arrangment

        # arbritrary limit
        # spin lock that exits when status=SUCCESS for all requests or timeout
        inputList=[]
        anyValid=False
        for pair in requestsAndArrangementsPairs:
            if pair=='error making request':
                pass
            else:
                anyValid=True
                rateId=pair[0]
                arrangement=pair[1]
                inputList.append((rateId,arrangement))
        if not anyValid:
            shipment.noValidRequests=True
            shipment.save()
            return shipment


        spinlockStart=time.time()
        outputList=[]
        with Pool(poolsToMake) as p:
            outputList=p.map(request_spinlock, inputList)
        spinlockEnd=time.time()

                    
        quoteCreationStart=time.time()
        for rateAndArrangment in outputList:
            quotesAsTuplesShippo,arrangement=rateAndArrangment[0],rateAndArrangment[1]            
            if quotesAsTuplesShippo=='':
                continue
            for quote in quotesAsTuplesShippo:
                #(carrier,cost,serviceDescription, guranteedDaysToDelivery,scheduledDeliveryTime)
                q=Quote.objects.create(owner=validated_data['owner'],shipment=shipment, arrangement=arrangement,carrier=quote[0],cost=float(quote[1]),serviceDescription=quote[2],daysToShip=quote[3],scheduledDeliveryTime=quote[4],shippoRateId=quote[5])
                serviceName=quote[2]
                serviceToken=quote[6]
                serviceTerms=quote[7]
                ServiceLevel.objects.create(name=serviceName,token=serviceToken,terms=serviceTerms,quote=q)
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
        return shipment

