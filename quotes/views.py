from django.shortcuts import render

# Create your views here.
from quotes.models import Quote
from quotes.serializers import QuoteSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from shipments.models import Shipment
from containers.models import Container
from items.models import Item
from django.shortcuts import render
import os

from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from users.models import User
from drf_yasg import openapi

from quotes.models import Quote
from drf_yasg.utils import swagger_auto_schema


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class QuoteList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Quote.objects.filter(owner=user)

    serializer_class = QuoteSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuoteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

@swagger_auto_schema(method='put', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'quoteId': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['put'])
@permission_classes([permissions.IsAuthenticated,IsOwner])
def refresh_shippo_quote(request):
    import shippo
    user=User.objects.get(email=request.user)
    if user.userHasShippoAccount() and (os.getenv('ENVIRONMENT_TYPE')=='PRODUCTION'):
        shippo.config.api_key=user.shippoAccessToken
    else:
        shippo.config.api_key = os.getenv('SHIPPO_API_KEY')
    quoteId=request.data['quoteId']
    shippoQuote = Quote.objects.get(id=quoteId)
    # shippoQuoteObjectId = shippoQuote.get('objectId', None)
    print(shippoQuote.arrangement)

    arrangement = shippoQuote.arrangement
    container = Container.objects.filter(arrangement=arrangement)[0]
    items = Item.objects.filter(arrangement=arrangement)
    shipment = Shipment.objects.get(id = shippoQuote.shipment.id)
    oldRates = Quote.objects.filter(shipment=shipment)
    print('shipment', shipment.shipFromAddress)

    # arrangement = Arrangement.objects.get(id=arrangementId)
    print(arrangement.containers)
    xDim = container.xDim
    yDim = container.yDim
    zDim = container.zDim
    print('dims', xDim, yDim, zDim)
    weight = 0
    for item in items:
        weight =+ item.weight

    parcel = {
        "length": xDim,
        "width": yDim,
        "height": zDim,
        "distance_unit": "in",
        "weight": weight,
        "mass_unit": "lb"
    }
    print(parcel)

    # it is probably better to just serialize the address data and pass it to shippo.shipment.create
    # country was not present so it was hard to test. fix this later
    # shipFrom = AddressSerializer(shipment.shipFromAddress)
    # shipTo = AddressSerializer(shipment.shipToAddress)
    # print(shipTo.data)

    addressFrom = shippo.Address.create(
        name = shipment.shipFromAddress.name,
        street1 = shipment.shipFromAddress.addressLine1,
        city = shipment.shipFromAddress.city,
        state = shipment.shipFromAddress.stateProvinceCode,
        zip = shipment.shipFromAddress.postalCode,
        phone = shipment.shipToAddress.phoneNumber,
        country = "US",
        validate = True
    )

    addressTo = shippo.Address.create(
        name = shipment.shipToAddress.name,
        street1 = shipment.shipToAddress.addressLine1,
        city = shipment.shipToAddress.city,
        state = shipment.shipToAddress.stateProvinceCode,
        zip = shipment.shipToAddress.postalCode,
        country = "US",
        phone = shipment.shipToAddress.phoneNumber,
        validate = True
    )

    newShippoShipment = shippo.Shipment.create(address_from=addressFrom, address_to=addressTo, parcels=[parcel], asynchronous=False)
    newRates = newShippoShipment['rates']

    for newRate in newRates:
        for oldRate in oldRates:
            if newRate['servicelevel']['token'] == oldRate.serviceLevel.token:
                #If this quote is the same as the old quote remove the refund so we can re-quote
                if quoteId == oldRate.id and not oldRate.shippoTransaction.shippoRefund:
                    oldRate.shippoTransaction.shippoRefund = ''
                oldRate.cost=newRate['amount']
                oldRate.serviceDescription=newRate['servicelevel']['name']
                oldRate.daysToShip=newRate['estimated_days']
                oldRate.scheduledDeliveryTime=['duration_terms']
                oldRate.shippoRateId=['object_id']
                oldRate.save()

                if oldRate.id == quoteId:
                    returned_quote_in_view = oldRate

    serializer=QuoteSerializer(returned_quote_in_view)
    return Response(serializer.data)
   
    