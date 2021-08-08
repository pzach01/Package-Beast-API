from rest_framework import serializers
from shipments.models import Shipment
from django.http import Http404
from subscription.models import Subscription
from quotes.models import Quote
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

class ShipmentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    containers = ContainerSerializer(many=True, write_only=True)
    items = ItemSerializerWithId(many=True, write_only=True)
    arrangements=ArrangementSerializer(many=True, required=False, read_only=True)
    timeoutDuration = serializers.IntegerField(write_only=True, min_value=1, max_value=55)
    shipToAddress = AddressSerializer()
    shipFromAddress = AddressSerializer()
    includeUpsContainers = serializers.BooleanField(write_only=True)
    includeUspsContainers = serializers.BooleanField(write_only=True)

    class Meta:
        model = Shipment
        depth=1
        fields = ['id', 'owner', 'created', 'title', 'lastSelectedQuoteId', 'items', 'containers','arrangements', 'multiBinPack', 'arrangementPossible', 'timeoutDuration', 'shipFromAddress', 'shipToAddress', 'quotes', 'timeout', 'includeUpsContainers', 'includeUspsContainers']
        read_only_fields = ['owner', 'created', 'arrangementPossible', 'timeoutDuration','arrangements', 'timeout']
    """
    # used before integration with Shippo API
    def make_ups_request(self,shipToAttentionName,shipToPhoneNumber,shipToAddressLineOne,shipToCity,shipToStateProvinceCode,shipToPostalCode,shipFromAttentionName,shipFromPhoneNumber,shipFromAddressLineOne,shipFromCity,shipFromStateProvinceCode,shipFromPostalCode,weight,xDim,yDim,zDim):
        # note that this is not production url
        testUrl='https://wwwcie.ups.com/ups.app/xml/Rate'
        testUrl=testUrl.replace('\n', '')

        # no pickup type
        # RequestOption can be changed to Rate to get a single rate for a single service, Shop specifies all
        # should 'AttentionName' be included ?
        # see package code for specific subtypes of packages like:
        #00 = UNKNOWN
        #01 = UPS Letter
        #02 = Package
        #03 = Tube
        #04 = Pak
        #21 = Express Box
        #24 = 25KG Box
        #25 = 10KG Box
        #30 = Pallet
        #2a = Small Express
        #Box
        #2b = Medium Express
        #Box
        #2c = Large Express
        #Box.
        # can add in some stuff to support cms

        shipperName='Lucas Zach'
        shipperPhoneNumber='5156573318'
        shipperAddressLineOne='13178 Oakbrook Drive'
        shipperCity='Des Moines'
        shipperStateProvinceCode='IA'
        shipperPostalCode='50323'
        shipperCountryCode='US'

        shipToCountryCode='US'

        shipFromCountryCode='US'
        #LBS = Pounds, KGS =Kilograms.
        unitOfMeasurement='LBS'
        xml='''
        <?xml version="1.0"?>

        <AccessRequest xml:lang="en-US">
        <AccessLicenseNumber>5D9635047BCF95F2</AccessLicenseNumber>
        <UserId>LucasZach35</UserId>
        <Password>Letsgetit35!</Password>
        </AccessRequest>

        <?xml version="1.0"?>
        <RatingServiceSelectionRequest xml:lang="en-US">

        <Request>
        <TransactionReference>
        <CustomerContext>This string will be in the response</CustomerContext>
        </TransactionReference>
        <RequestAction>Shop</RequestAction>
        <RequestOption>Shop</RequestOption>
        </Request>
        '''
        xml+='<Shipment>'
        xml+='<Shipper>'

        xml+='<Name>'+shipperName+'</Name>'
        xml+='<AttentionName></AttentionName>'
        xml+='<PhoneNumber>'+shipperPhoneNumber+'</PhoneNumber>'
        xml+='<FaxNumber></FaxNumber>'
        xml+='<ShipperNumber></ShipperNumber>'

        xml+='<Address>'
        xml+='<AddressLine1>'+shipperAddressLineOne+'</AddressLine1>'
        xml+='<City>'+shipperCity+'</City>'
        xml+='<StateProvinceCode>'+shipperStateProvinceCode+'</StateProvinceCode>'
        xml+='<PostalCode>'+shipperPostalCode+'</PostalCode>'
        xml+='<CountryCode>'+shipperCountryCode+'</CountryCode>'
        xml+='</Address>'

        xml+='</Shipper>'

        xml+='<ShipTo>'

        xml+='<CompanyName></CompanyName>'
        xml+='<AttentionName>'+shipToAttentionName+'</AttentionName>'
        xml+='<PhoneNumber>'+shipToPhoneNumber+'</PhoneNumber>'
        xml+='<FaxNumber></FaxNumber>'

        xml+='<Address>'
        xml+='<AddressLine1>'+shipToAddressLineOne+'</AddressLine1>'
        xml+='<City>'+shipToCity+'</City>'
        xml+='<StateProvinceCode>'+shipToStateProvinceCode+'</StateProvinceCode>'
        xml+='<PostalCode>'+shipToPostalCode+'</PostalCode>'
        xml+='<CountryCode>'+shipToCountryCode+'</CountryCode>'
        xml+='</Address>'

        xml+='</ShipTo>'


        xml+='<ShipFrom>'
        xml+='<CompanyName></CompanyName>'
        xml+='<AttentionName>'+shipFromAttentionName+'</AttentionName>'
        xml+='<PhoneNumber>'+shipFromPhoneNumber+'</PhoneNumber>'
        xml+='<FaxNumber></FaxNumber>'
        
        xml+='<Address>'
        xml+='<AddressLine1>'+shipFromAddressLineOne+'</AddressLine1>'
        xml+='<City>'+shipFromCity+'</City>'
        xml+='<StateProvinceCode>'+shipFromStateProvinceCode+'</StateProvinceCode>'
        xml+='<PostalCode>'+shipFromPostalCode+'</PostalCode>'
        xml+='<CountryCode>'+shipFromCountryCode+'</CountryCode>'
        xml+='</Address>'

        xml+='</ShipFrom>'
        
        # review what these mean
        # ignored because of shopping
        xml+='''
        <Service>
        <Code>03</Code>
        <Description>UPS Ground</Description>
        </Service>

        <Package>

        <PackagingType>
        <Code>02</Code>
        <Description>UPS Package</Description>
        </PackagingType>
        '''

        xml+='<PackageWeight>'
        xml+='<UnitOfMeasurement>'
        xml+='<Code>'+unitOfMeasurement+'</Code>'
        xml+='</UnitOfMeasurement>'
        xml+='<Weight>'+weight+'</Weight>'
        xml+='</PackageWeight>'

        xml+='<Dimensions>'
        xml+='<Length>'+xDim+'</Length>'
        xml+='<Width>'+yDim+'</Width>'
        xml+='<Height>'+zDim+'</Height>'
        xml+='</Dimensions>'
        xml+='</Package>'

        xml+='</Shipment>'
        xml+='</RatingServiceSelectionRequest>'
        

        import requests
        # 21.90
        #r = requests.get(get_shipping_cost_info_string('10','2','LG FLAT RATE BOX','','',''))

        # 15.55
        r = requests.post(testUrl,data=xml)

        dataAsText=(r.text)
        import xmltodict
        import json
        dataDict = xmltodict.parse(dataAsText)
        nestOne=dataDict['RatingServiceSelectionResponse']
        assert(nestOne['Response']['ResponseStatusDescription']=="Success")

        ratedShipments=nestOne['RatedShipment']
        tupleList=[]
        for r in ratedShipments:
            carrier='UPS'
            if not r['TotalCharges']['CurrencyCode']=='USD':
                raise Exception("unsupported currency")
            cost=r['TotalCharges']['MonetaryValue']
            guranteedDaysToDelivery=r['GuaranteedDaysToDelivery']
            serviceCode=r['Service']['Code']
            scheduledDeliveryTime=r['ScheduledDeliveryTime']
            serviceDescription='Error'

            # couldnt find how to force response to include serviceDescription 
            if serviceCode=='01':
                serviceDescription='Next Day Air'
            if serviceCode=='02':
                serviceDescription='2nd Day Air'
            if serviceCode=='03':
                serviceDescription='Ground'
            if serviceCode=='12':
                serviceDescription='3 Day Select'
            if serviceCode=='13':
                serviceDescription='Next Day Air Saver'
            if serviceCode=='14':
                serviceDescription='UPS Next Day Air Early'
            if serviceCode=='59':
                serviceDescription='2nd Day Air A.M.'
            #Valid international values:
            #07 = Worldwide Express
            #08 = Worldwide Expedited
            #11= Standard
            #54 = Worldwide Express Plus
            #65 = Saver
            #96 = UPS Worldwide Express
            #Freight
            #71 = UPS Worldwide
            if (serviceCode=='07') or (serviceCode=='08') or (serviceCode=='11') or (serviceCode=='54') or (serviceCode=='65') or (serviceCode=='96') or (serviceCode=='71'):
                serviceDescription='International service, not supported'
            tupleList.append((carrier,cost,serviceDescription, guranteedDaysToDelivery,scheduledDeliveryTime))
        return tupleList
    """

    """
    # used before Shippo integration
    def make_usps_request(self,shipToPostalCode,shipFromPostalCode,weight,xDim,yDim,zDim):
        boxType='VARIABLE'
        # assumes weight is in pounds as decimal
        weightOunces=round(weight*16)
        weightPounds=weightOunces//16
        weightOunces=weightOunces-(16*weightPounds)

        weightPounds=str(weightPounds)
        weightOunces=str(weightOunces)
        # not a USPS special box; reexamine this in the docs
        endpoint='https://secure.shippingapis.com/ShippingAPI.dll?API=RateV4 &XML='
        xml='<RateV4Request USERID="106PACKA2149"><Revision>2</Revision><Package ID="0"><Service>ALL</Service>'
        xml+='<ZipOrigination>'+shipFromPostalCode+'</ZipOrigination>'
        xml+='<ZipDestination>'+shipToPostalCode+'</ZipDestination>'
        xml+='<Pounds>'+weightPounds+'</Pounds>'
        xml+='<Ounces>'+weightOunces+'</Ounces>'
        xml+='<Container>'+boxType+'</Container>'
        xml+='<Width>'+xDim+'</Width>'
        xml+='<Length>'+yDim+'</Length>'
        xml+='<Height>'+zDim+'</Height>'
        xml+='<Girth></Girth><Machinable>TRUE</Machinable></Package></RateV4Request>'
        testUrl= endpoint+xml

        import requests
        r = requests.post(testUrl,data=xml)

        dataAsText=(r.text)
        import xmltodict
        import json
        dataDict = xmltodict.parse(dataAsText)
        nestOne=dataDict['RateV4Response']
        nestTwo=nestOne['Package']
        data=nestTwo['Postage']
        #(carrier,cost,serviceDescription, guranteedDaysToDelivery,scheduledDeliveryTime)

        tupleList=[]
        for d in data:
            t=('USPS',d['Rate'],d['MailService'],'','')
            tupleList.append(t)
        return tupleList
    """


    def make_rates_request(self,username,shipToAttentionName,shipToPhoneNumber,shipToAddressLineOne,shipToCity,shipToStateProvinceCode,shipToPostalCode,shipFromAttentionName,shipFromPhoneNumber,shipFromAddressLineOne,shipFromCity,shipFromStateProvinceCode,shipFromPostalCode,weight,xDim,yDim,zDim):
        if '.' in weight:
            weight=weight[0: (weight.index('.')+5)]
        if '.' in xDim:
            xDim=xDim[0: (xDim.index('.')+5)]
        if '.' in yDim:
            yDim=yDim[0: (yDim.index('.')+5)]
        if '.' in zDim:
            zDim=zDim[0: (zDim.index('.')+5)]


        import shippo
        import os

        user=User.objects.get(email=username)
        if user.userHasShippoAccount() and (os.getenv('ENVIRONMENT_TYPE')=='PRODUCTION'):
            shippo.config.api_key=user.shippoAccessToken
        else:
            shippo.config.api_key = os.getenv('SHIPPO_API_KEY')

        address_from = shippo.Address.create(
            name = shipFromAttentionName,
            street1 = shipFromAddressLineOne,
            city = shipFromCity,
            state = shipFromStateProvinceCode,
            zip = shipFromPostalCode,
            country = "US",
            validate = True
        )

        address_to = shippo.Address.create(
            name = shipToAttentionName,
            street1 = shipToAddressLineOne,
            city = shipToCity,
            state = shipToStateProvinceCode,
            zip = shipToPostalCode,
            country = "US",
            validate = True
        )
        parcel = {
            "length": xDim,
            "width": yDim,
            "height": zDim,
            "distance_unit": "in",
            "weight": weight,
            "mass_unit": "lb"
        }

        response = shippo.Shipment.create(
            address_from = address_from,
            address_to = address_to,
            parcels = [parcel],
            asynchronous = True
        )
        return response
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
        # make no more then 10 api requests
        requestLimit=10
        requestsMade=0

        containers = validated_data.pop('containers')
        items = validated_data.pop('items')
        timeoutDuration=validated_data.pop('timeoutDuration')
        lastSelectedQuoteId=validated_data.pop('lastSelectedQuoteId')
        # this is actually unused (remove at future date from)
        multiBinPack=validated_data['multiBinPack']
        includeUpsContainers = validated_data.pop('includeUpsContainers')
        includeUspsContainers = validated_data.pop('includeUspsContainers')

        # shipFromAddress=Address.objects.create(validated_data.pop('shipFromAddress'))
        # shipToAddress=Address.objects.create(validated_data.pop('shipToAddress'))
        # print(shipToAddress)
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
            return shipment
        # similiar to running original arrangments serializer multiple times, but only creates
        # one container per arrangment
        requestsAndArrangements=[]
        for ele in range(0, len(apiObjects)):
            arrangement = Arrangement.objects.create(**validated_data,shipment=shipment)
            arrangement.timeout = timedout
            arrangement.arrangementPossible = arrangementPossible
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

            if requestsMade<requestLimit:
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
                weight=totalWeight
                assert(not xDim==0)
                assert(not yDim==0)
                assert(not zDim==0)

                xDim=str(xDim)
                yDim=str(yDim)
                zDim=str(zDim)
                request=self.make_rates_request(validated_data['owner'],shipToAttentionName,shipToPhoneNumber,shipToAddressLineOne,shipToCity,shipToStateProvinceCode,shipToPostalCode,shipFromAttentionName,shipFromPhoneNumber,shipFromAddressLineOne,shipFromCity,shipFromStateProvinceCode,shipFromPostalCode,str(weight),xDim,yDim,zDim)
                requestsAndArrangements.append((request,arrangement))
        import time
        import shippo
        endTime=time.time()+15
        # give shippo 3 secs of lead time to make arrangment
        time.sleep(3)
        # spin lock that exits when status=SUCCESS for all requests or timeout
        keepGoing=True


        while(time.time()<endTime and keepGoing):
            keepGoing=False
            for index in range(0, len(requestsAndArrangements)):
                requestAndArrangement=requestsAndArrangements[index]

                request,arrangement=requestAndArrangement[0],requestAndArrangement[1]
                # no need to check this object again
                if request['status']=='SUCCESS':
                    pass
                else:
                    newRequest=shippo.Shipment.retrieve(request['object_id'])
                    if newRequest['status']=='SUCCESS':
                        requestsAndArrangements[index]=(newRequest,arrangement)
                    else:
                        keepGoing=True
                        # give shippo more time
                        time.sleep(.5)


                    

        for rateAndArrangment in requestsAndArrangements:
            request,arrangment=rateAndArrangment[0],rateAndArrangment[1]
            rates=request['rates']

            quotesAsTuplesShippo=[]
            for rate in rates:
                rateId=rate['object_id']
                #(carrier,cost,serviceDescription, guranteedDaysToDelivery,scheduledDeliveryTime)
                t=(rate['provider'],rate['amount'],rate['servicelevel']['name'],rate['estimated_days'],rate['duration_terms'],rateId)
                quotesAsTuplesShippo.append(t)
            
            for quote in quotesAsTuplesShippo:
                #(carrier,cost,serviceDescription, guranteedDaysToDelivery,scheduledDeliveryTime)
                Quote.objects.create(owner=validated_data['owner'],shipment=shipment, arrangement=arrangement,carrier=quote[0],cost=float(quote[1]),serviceDescription=quote[2],daysToShip=quote[3],scheduledDeliveryTime=quote[4],shippoRateId=quote[5])
        return shipment

