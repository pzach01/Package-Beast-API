
# Create your tests here.
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.authtoken.models import Token
from arrangements.views import ArrangementList, Arrangement
from rest_framework.test import force_authenticate
from users.models import User
from subscription.models import Subscription,StripeSubscription

from rest_framework.test import APITestCase

class ShipmentsTests(APITestCase):
    def generic_logic(self,inputData,createUser=True):
        if createUser:
            u = User.objects.create(email='b@b.com')
            u.set_password('b')
            u.save()
            sub=Subscription.objects.create(owner=u)
            sub.shipmentsAllowed=500
            sub.itemsAllowed=500
            sub.containersAllowed=500

            sub.save()


            stripeSub=StripeSubscription.objects.create(subscription=sub)
            import time
            stripeSub.currentPeriodEnd=time.time()+(60*60*24*2)
            stripeSub.save()

        # url = reverse('account-list')
        self.client.login(email="b@b.com", password="b")
        url = '/shipments/'
        response = self.client.post(url,inputData,format='json')


        data=response.data
        return data
    def get_arrangment(self,id):
        self.client.login(email="b@b.com", password="b")
        url = '/arrangements/'+str(id)+'/'
        response = self.client.get(url,format='json')
        data=response.data
        return data
    # QUESTION ASKED: can you hit the shipments endpoint?
    def test_1(self):
        try:
            inputData={
            "title": "string",
            "lastSelectedQuoteId": 0,
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                }
            ],
            "containers": [
                {
                "sku": "string",
                "description": "string",
                "xDim": 1,
                "yDim": 1,
                "zDim": 1,
                "units": "in"
                }
            ],
            "multiBinPack": False,
            "timeoutDuration": 15,
            "shipFromAddress": {
                "name":"Lucas Z",
                "phoneNumber":"5156573318",
                "addressLine1": "314 North Clinton Street",
                "addressLine2": "string",
                "city": "Iowa City",
                "stateProvince": "IA",
                "postalCode": "52245"
            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323"
            }
            }

            data=self.generic_logic(inputData)
            # checks on the data, will print -----------Failed Arrangments Test 1 if these fail

            print("Shipments test 1 Passed")
        except:
            print('--------------Failed shipments test 1')


# QUESTION ASKED: what happens if you cant fit any containers?
    def test_2(self):
        try:
            inputData={
            "title": "string",
            "lastSelectedQuoteId": 0,
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 2,
                "width": 2,
                "height": 2,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                }
            ],
            "containers": [
                {
                "sku": "string",
                "description": "string",
                "xDim": 1,
                "yDim": 1,
                "zDim": 1,
                "units": "in"
                }
            ],
            "multiBinPack": False,
            "timeoutDuration": 15,
            "shipFromAddress": {
                "name":"Lucas Z",
                "phoneNumber":"5156573318",
                "addressLine1": "314 North Clinton Street",
                "addressLine2": "string",
                "city": "Iowa City",
                "stateProvince": "IA",
                "postalCode": "52245"
            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323"
            }
            }




            data=self.generic_logic(inputData)
            assert(data['arrangementPossible']==False)
            # checks on the data, will print -----------Failed Arrangments Test 1 if these fail

            print("Shipments test 2 Passed")
        except:
            print("-----------Shipments test 2 Failed")

# QUESTION ASKED: can we access the arrangments corresponding to a shipment?
    def test_3(self):
        inputData={
        "title": "string",
        "lastSelectedQuoteId": 0,
        "items": [
            {
            "id": 0,
            "sku": "string",
            "description": "string",
            "length": 1,
            "width": 1,
            "height": 1,
            "units": "in",
            "weight": 5,
            "weightUnits": "lb"
            }
        ],
        "containers": [
            {
            "sku": "string",
            "description": "string",
            "xDim": 1,
            "yDim": 1,
            "zDim": 1,
            "units": "in"
            }
        ],
        "multiBinPack": False,
        "timeoutDuration": 15,
        "shipFromAddress": {
            "name":"Lucas Z",
            "phoneNumber":"5156573318",
            "addressLine1": "314 North Clinton Street",
            "addressLine2": "string",
            "city": "Iowa City",
            "stateProvince": "IA",
            "postalCode": "52245"
        },
        "shipToAddress":{
            "name":"John Doe",
            "phoneNumber":"5156573318",
            "addressLine1": "13178 Oakbrook Drive",
            "addressLine2": "string",
            "city": "Des Moines",
            "stateProvince": "IA",
            "postalCode": "50323"
        }
        }




        data=self.generic_logic(inputData)
        assert(data['arrangementPossible']==True)
        
        # check the return data for truth
        assert(data['arrangements'][0]['items'][0]['xCenter']==.5)
        assert(data['arrangements'][0]['items'][0]['yCenter']==.5)
        assert(data['arrangements'][0]['items'][0]['zCenter']==.5)
        
        arrangmentId=data['arrangements'][0]['id']




        # check the database for truth
        arrangementData=(self.get_arrangment(arrangmentId))
        # this test will fail without saving the arrangment, very odd because item data is still returned
        assert(arrangementData['arrangementPossible']==True)

        selectedItem=arrangementData['items'][0]
        assert(selectedItem['xCenter']==.5)
        assert(selectedItem['yCenter']==.5)
        assert(selectedItem['zCenter']==.5)
        # checks on the data, will print -----------Failed Arrangments Test 1 if these fail

        print("Shipments test 3 Passed")

# QUESTION ASKED: does shipments play nice with multiple arrangments?
    def test_4(self):
        try:
            inputData={
            "title": "string",
            "lastSelectedQuoteId": 0,
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                }
            ],
            "containers": [
                {
                "sku": "string",
                "description": "string",
                "xDim": 1,
                "yDim": 1,
                "zDim": 1,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 2,
                "yDim": 2,
                "zDim": 2,
                "units": "in"
                }
            ],
            "multiBinPack": False,
            "timeoutDuration": 15,
            "shipFromAddress": {
                "name":"Lucas Z",
                "phoneNumber":"5156573318",
                "addressLine1": "314 North Clinton Street",
                "addressLine2": "string",
                "city": "Iowa City",
                "stateProvince": "IA",
                "postalCode": "52245"
            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323"
            }
            }





            data=self.generic_logic(inputData)
            # check the return data for truth

            assert(data['arrangementPossible']==True)
            
            assert(data['arrangements'][0]['items'][0]['xCenter']==.5)
            assert(data['arrangements'][0]['items'][0]['yCenter']==.5)
            assert(data['arrangements'][0]['items'][0]['zCenter']==.5)


            assert(data['arrangements'][1]['items'][0]['xCenter']==.5)
            assert(data['arrangements'][1]['items'][0]['yCenter']==.5)
            assert(data['arrangements'][1]['items'][0]['zCenter']==.5)
            assert(len(data['arrangements'])==2)
            # checks on the data, will print -----------Failed Arrangments Test 1 if these fail

            print("Shipments test 4 Passed")
        except:
            print("-----------Shipments test 4 Failed")

# QUESTION ASKED: how do we do with 10 containers and 10 small items?
# This test fails. Bug caused by too many containers?
    def test_5(self):
        try:
            inputData={
            "title": "string",
            "lastSelectedQuoteId": 0,
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                },
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                },
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                },
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                },
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                },
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                },
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                },
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                },
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                },
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                }
            ],
            "containers": [
                {
                "sku": "string",
                "description": "string",
                "xDim": 1,
                "yDim": 1,
                "zDim": 1,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 2,
                "yDim": 2,
                "zDim": 2,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 3,
                "yDim": 3,
                "zDim": 3,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 8,
                "yDim": 8,
                "zDim": 8,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 20,
                "yDim": 20,
                "zDim": 20,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 30,
                "yDim": 30,
                "zDim": 30,
                "units": "in"
                },
                                {
                "sku": "string",
                "description": "string",
                "xDim": 20,
                "yDim": 20,
                "zDim": 20,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 30,
                "yDim": 30,
                "zDim": 30,
                "units": "in"
                },
                                {
                "sku": "string",
                "description": "string",
                "xDim": 20,
                "yDim": 20,
                "zDim": 20,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 30,
                "yDim": 30,
                "zDim": 30,
                "units": "in"
                }
            ],
            "multiBinPack": False,
            "timeoutDuration": 15,
            "shipFromAddress": {
                "name":"Lucas Z",
                "phoneNumber":"5156573318",
                "addressLine1": "314 North Clinton Street",
                "addressLine2": "string",
                "city": "Iowa City",
                "stateProvince": "IA",
                "postalCode": "52245"
            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323"
            }
            }





            data=self.generic_logic(inputData)
            # check the return data for truth

            assert(data['arrangementPossible']==True)
            
            assert(len(data['arrangements'])==8)
            # checks on the data, will print -----------Failed Arrangments Test 1 if these fail

            print("Shipments test 5 Passed")
        except:
            print("-----------Shipments test 5 Failed")





    # do unit conversions work for weight
    def test_7(self):
        try:
            inputData={
            "title": "string",
            "lastSelectedQuoteId": 0,
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 1,
                "weightUnits": "lb"
                },
                {
                "id": 1,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 1,
                "weightUnits": "kg"
                }                
            ],
            "containers": [
                {
                "sku": "string",
                "description": "string",
                "xDim": 2,
                "yDim": 1,
                "zDim": 1,
                "units": "in"
                }
            ],
            "multiBinPack": False,
            "timeoutDuration": 15,
            "shipFromAddress": {
                "name":"Lucas Z",
                "phoneNumber":"5156573318",
                "addressLine1": "314 North Clinton Street",
                "addressLine2": "string",
                "city": "Iowa City",
                "stateProvince": "IA",
                "postalCode": "52245"
            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323"
            }
            }

            data=self.generic_logic(inputData)
            items=data['quotes'][0]['arrangement']['items']
            weight=sum([item['weight'] for item in items])
            assert(weight==3.205)
            #weights=[item['weight'] for item in data['quotes'][0]['items']]
            #print(weights)
            #assert(sum(weights)==3.205)
            # checks on the data, will print -----------Failed Arrangments Test 1 if these fail

            print("Shipments test 7 Passed")
        except:
            print('--------------Failed shipments test 7')


    # QUESTION ASKED:: does the error thrown by invalidAddress/error creating shippo Shipment
    def test_8(self):
        try:
            inputData={
            "title": "string",
            "lastSelectedQuoteId": 0,
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                }
            ],
            "containers": [
                {
                "sku": "string",
                "description": "string",
                "xDim": 1,
                "yDim": 1,
                "zDim": 1,
                "units": "in"
                }
            ],
            "multiBinPack": False,
            "timeoutDuration": 15,
            "shipFromAddress": {
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323"
            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323"
            }
            }

            data=self.generic_logic(inputData)
            # checks on the data, will print -----------Failed Arrangments Test 1 if these fail
            assert(data['validAddress']==False)
            print("Shipments test 8 Passed")
        except:
            print('--------------Failed shipments test 8')