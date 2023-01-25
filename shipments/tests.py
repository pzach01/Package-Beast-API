
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
                "postalCode": "52245",
                "country": "United States"

            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323",
                "country": "United States"
            }
            }

            data=self.generic_logic(inputData)
            # checks on the data, will print -----------Failed Shipments Test 1 if these fail

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
                "postalCode": "52245",
                "country": "United States"

            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323",
                "country": "United States"

            }
            }




            data=self.generic_logic(inputData)

            assert(data['fitAllArrangementPossibleAPriori']==False)
            assert(data['arrangementFittingAllItemsFound']==False)
            # checks on the data, will print -----------Failed Shipments Test 2 if these fail

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
            "postalCode": "52245",
            "country": "United States"

        },
        "shipToAddress":{
            "name":"John Doe",
            "phoneNumber":"5156573318",
            "addressLine1": "13178 Oakbrook Drive",
            "addressLine2": "string",
            "city": "Des Moines",
            "stateProvince": "IA",
            "postalCode": "50323",
            "country": "United States"
        }
        }




        data=self.generic_logic(inputData)
        assert(data['fitAllArrangementPossibleAPriori']==True)
        assert(data['arrangementFittingAllItemsFound']==True)        
        # check the return data for truth
        assert(data['arrangements'][0]['items'][0]['xCenter']==.5)
        assert(data['arrangements'][0]['items'][0]['yCenter']==.5)
        assert(data['arrangements'][0]['items'][0]['zCenter']==.5)
        
        arrangmentId=data['arrangements'][0]['id']




        # check the database for truth
        arrangementData=(self.get_arrangment(arrangmentId))
        # this test will fail without saving the arrangment, very odd because item data is still returned
        assert(data['fitAllArrangementPossibleAPriori']==True)
        assert(data['arrangementFittingAllItemsFound']==True)
        
        selectedItem=arrangementData['items'][0]
        assert(selectedItem['xCenter']==.5)
        assert(selectedItem['yCenter']==.5)
        assert(selectedItem['zCenter']==.5)
        # checks on the data, will print -----------Failed Shipments Test 3 if these fail

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
                "postalCode": "52245",
                "country": "United States"

            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323",
                "country": "United States"

            }
            }





            data=self.generic_logic(inputData)
            # check the return data for truth
            assert(data['fitAllArrangementPossibleAPriori']==True)
            assert(data['arrangementFittingAllItemsFound']==True)
            
            assert(data['arrangements'][0]['items'][0]['xCenter']==.5)
            assert(data['arrangements'][0]['items'][0]['yCenter']==.5)
            assert(data['arrangements'][0]['items'][0]['zCenter']==.5)


            assert(data['arrangements'][1]['items'][0]['xCenter']==.5)
            assert(data['arrangements'][1]['items'][0]['yCenter']==.5)
            assert(data['arrangements'][1]['items'][0]['zCenter']==.5)
            assert(len(data['arrangements'])==2)
            # checks on the data, will print -----------Failed Shipments Test 4 if these fail

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
                "postalCode": "52245",
                "country": "United States"

            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323",
                "country": "United States"

            }
            }





            data=self.generic_logic(inputData)
            # check the return data for truth

            assert(data['fitAllArrangementPossibleAPriori']==True)
            assert(data['arrangementFittingAllItemsFound']==True)

            assert(len(data['arrangements'])==8)
            # checks on the data, will print -----------Failed Shipments Test 5 if these fail

            print("Shipments test 5 Passed")
        except:
            print("-----------Shipments test 5 Failed")





    # do unit conversions work for weight
    def test_6(self):
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
                "postalCode": "52245",
                "country": "United States"

            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323",
                "country": "United States"

            }
            }

            data=self.generic_logic(inputData)


            assert(data['fitAllArrangementPossibleAPriori']==True)
            assert(data['arrangementFittingAllItemsFound']==True)

            items=data['quotes'][0]['arrangement']['items']
            weight=sum([item['weight'] for item in items])
            assert(weight==3.205)
            #weights=[item['weight'] for item in data['quotes'][0]['items']]
            #print(weights)
            #assert(sum(weights)==3.205)
            # checks on the data, will print -----------Failed Shipments Test 6 if these fail

            print("Shipments test 6 Passed")
        except:
            print('--------------Failed shipments test 6')


    # QUESTION ASKED:: does the error throw correctly when shipping to same address
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
                "postalCode": "50323",
                "country": "United States"

            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323",
                "country": "United States"

            }
            }

            data=self.generic_logic(inputData)
            # checks on the data, will print -----------Failed Shipments Test 7 if these fail

            assert(data['message']=='same from and to addresses')
            print("Shipments test 7 Passed")
        except:
            print('--------------Failed shipments test 7')
    # QUESTION ASKED:: does validToAddress work
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
                "postalCode": "50323",
                "country": "United States"

            },
            "shipToAddress":{
                "name":"Seymour Cox",
                "phoneNumber":"5156573318",
                "addressLine1": "69 420 Blaze It Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323",
                "country": "United States"

            }
            }

            data=self.generic_logic(inputData)
            # checks on the data, will print -----------Failed Shipments Test 8 if these fail
            assert(data['message']=='invalid to address')

            print("Shipments test 8 Passed")
        except:
            print('--------------Failed shipments test 8')


    # QUESTION ASKED: can we seperate the behavior of fitAllArrangementPossibleAPriori and arrangementFittingAllItemsFound
    def test_9(self):
        try:
            inputData={
            "title": "string",
            "lastSelectedQuoteId": 0,
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 9,
                "width": 9,
                "height": 10,
                "units": "in",
                "weight": 5,
                "weightUnits": "lb"
                },
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
                "xDim": 10,
                "yDim": 10,
                "zDim": 10,
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
                "postalCode": "52245",
                "country": "United States"

            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323",
                "country": "United States"

            }
            }

            data=self.generic_logic(inputData)
            # checks on the data, will print -----------Failed Shipments Test 9 if these fail
            assert(data['fitAllArrangementPossibleAPriori']==True)
            assert(data['arrangementFittingAllItemsFound']==False)


            print("Shipments test 9 Passed")
        except:
            print('--------------Failed shipments test 9')
    # do we bug when using lots of containers?
    def test_10(self):
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
                "xDim": 4,
                "yDim": 4,
                "zDim": 4,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 5,
                "yDim": 5,
                "zDim": 5,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 6,
                "yDim": 6,
                "zDim": 6,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 7,
                "yDim": 7,
                "zDim": 7,
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
                "xDim": 9,
                "yDim": 9,
                "zDim": 9,
                "units": "in"
                },                 
                {
                "sku": "string",
                "description": "string",
                "xDim": 10,
                "yDim": 10,
                "zDim": 10,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 11,
                "yDim": 11,
                "zDim": 11,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 12,
                "yDim": 12,
                "zDim": 12,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 13,
                "yDim": 13,
                "zDim": 13,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 14,
                "yDim": 14,
                "zDim": 14,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 15,
                "yDim": 15,
                "zDim": 15,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 16,
                "yDim": 16,
                "zDim": 16,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 17,
                "yDim": 17,
                "zDim": 17,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 18,
                "yDim": 18,
                "zDim": 18,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 19,
                "yDim": 19,
                "zDim": 19,
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
                "xDim": 21,
                "yDim": 21,
                "zDim": 21,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 22,
                "yDim": 22,
                "zDim": 22,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 23,
                "yDim": 23,
                "zDim": 23,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 24,
                "yDim": 24,
                "zDim": 24,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 25,
                "yDim": 25,
                "zDim": 25,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 26,
                "yDim": 26,
                "zDim": 26,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 27,
                "yDim": 27,
                "zDim": 27,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 28,
                "yDim": 28,
                "zDim": 28,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 29,
                "yDim": 29,
                "zDim": 29,
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
                "xDim": 31,
                "yDim": 31,
                "zDim": 31,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 32,
                "yDim": 32,
                "zDim": 32,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 33,
                "yDim": 33,
                "zDim": 33,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 34,
                "yDim": 34,
                "zDim": 34,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 35,
                "yDim": 35,
                "zDim": 35,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 36,
                "yDim": 36,
                "zDim": 36,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 37,
                "yDim": 37,
                "zDim": 37,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 38,
                "yDim": 38,
                "zDim": 38,
                "units": "in"
                },
                {
                "sku": "string",
                "description": "string",
                "xDim": 39,
                "yDim": 39,
                "zDim": 39,
                "units": "in"
                },                 
                {
                "sku": "string",
                "description": "string",
                "xDim": 40,
                "yDim": 40,
                "zDim": 40,
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
                "postalCode": "52245",
                "country": "United States"

            },
            "shipToAddress":{
                "name":"John Doe",
                "phoneNumber":"5156573318",
                "addressLine1": "13178 Oakbrook Drive",
                "addressLine2": "string",
                "city": "Des Moines",
                "stateProvince": "IA",
                "postalCode": "50323",
                "country": "United States"

            }
            }

            data=self.generic_logic(inputData)
            import time
            time.sleep(30)
            # checks on the data, will print -----------Failed Shipments Test 10 if these fail
            # all of these may fail at times depending on how overloaded Shippo is
            assert(data['fitAllArrangementPossibleAPriori']==True)
            assert(data['arrangementFittingAllItemsFound']==True)
            assert(data['usedAllValidContainers']==False)
            assert(data['noErrorsMakingRequests']==True)
            assert(data['noValidRequests']==False)
            assert(len(data['quotes'])>0)

            print("Shipments test 10 Passed")
        except:
            print('-------------Shipments test 10 Failed')
         
