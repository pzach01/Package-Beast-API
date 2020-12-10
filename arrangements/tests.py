
# to run (everything, not just this test file) use
# ./manage.py test




from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.authtoken.models import Token
from arrangements.views import ArrangementList, Arrangement
from rest_framework.test import force_authenticate
from users.models import User
from subscription.models import Subscription,StripeSubscription

from rest_framework.test import APITestCase

class ArrangmentTests(APITestCase):
    def generic_logic(self,inputData):
        u = User.objects.create(email='a@a.com')
        u.set_password('a')
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
        self.client.login(email="a@a.com", password="a")
        url = '/arrangements/'
        response = self.client.post(url,inputData,format='json')


        data=response.data
        return data

    # QUESTION ASKED: does the code work in some basic form?, 
    def test_1(self):
        try:
            inputData={
            "multiBinPack": False,
            "timeoutDuration": 30,
            "containers": [
                {
                "sku": "unit",
                "description": "string",
                "xDim": 2,
                "yDim": 2,
                "zDim": 1,
                "units": "in"
                }
            ],
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 1,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 2,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 3,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                }
            ]
            }




            data=self.generic_logic(inputData)
            # checks on the data, will print -----------Failed Arrangments Test 1 if these fail

            assert(data['arrangementPossible']==True)
            assert(data['multiBinPack']==False)


            selectedContainer=data['containers'][0]['id']
            for item in data['items']:
                assert(item['container']==selectedContainer)


            validXYZTuples=[(.5,.5,.5), (.5,1.5,.5),(1.5,.5,.5),(1.5,1.5,.5)]
            observedXYZTuples=[]
            for item in data['items']:
                observedXYZTuples.append((item['xCenter'],item['yCenter'],item['zCenter']))
            observedXYZTuples=sorted(observedXYZTuples)
            assert(observedXYZTuples==observedXYZTuples)
            print("Arrangments test 1 Passed")
        except:
            print("---------------Arrangments test 1 Failed")
    # QUESTION ASKED: what is the expected behavior when not all the container fit?
    # arrangment possible should return false
    ## ASK PETER: do containers and items still need to be returned in the event of a failure; simple fix in serializer if not
    def test_2(self):
        try:
            inputData={
            "multiBinPack": False,
            "timeoutDuration": 30,
            "containers": [
                {
                "sku": "unit",
                "description": "string",
                "xDim": 2,
                "yDim": 2,
                "zDim": 1,
                "units": "in"
                }
            ],
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 1,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 2,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 3,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 4,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                }
            ]
            }



            data=self.generic_logic(inputData)
            

            # checks on the data, will print -----------Failed Arrangments Test 2 if these fail

            assert(data['arrangementPossible']==True)
            assert(data['multiBinPack']==False)
            assert(len(data['items'])==5)
            count=0
            for item in data['items']:
                # null container field
                if(item['container']==None):
                    pass
                else:
                    count+=1
            assert(len(data['containers'])==1)
            assert(count==4)
            print("Arrangments test 2 Passed")
        except:
            print("------------------Arrangments test 2 Failed")
    # QUESTION ASKED: what is the behavior when we try to optimize boxes into multiple containers (and there is one best container)
    # return all containers that are filled
    def test_3(self):
        try:
            inputData={
            "multiBinPack": False,
            "timeoutDuration": 30,
            "containers": [
                {
                "sku": "unit",
                "description": "string",
                "xDim": 2,
                "yDim": 2,
                "zDim": 1,
                "units": "in"
                },
                {
                "sku": "unit",
                "description": "string",
                "xDim": 1,
                "yDim": 2,
                "zDim": 1,
                "units": "in"
                }
            ],
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 1,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 2,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 3,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                }
            ]
            }



            data=self.generic_logic(inputData)
            

            assert(data['arrangementPossible']==True)
            assert(data['multiBinPack']==False)
            assert(len(data['items'])==4)
            assert(len(data['containers'])==2)
            usedContainerId=None
            for container in data['containers']:
                if container['xDim']==2 and (container['yDim']==2 and container['zDim']==1):
                    usedContainerId=container['id']
            for item in data['items']:
                assert(item['container']==usedContainerId)
            print("Arrangments test 3 Passed")
        except:
            print("------------------Arrangments test 3 Failed")

    # QUESTION ASKED: does the items returned match the order of the rendering (in at least one case)
    def test_4(self):
        try:
            inputData={
            "multiBinPack": False,
            "timeoutDuration": 30,
            "containers": [
                {
                "sku": "unit",
                "description": "string",
                "xDim": 2,
                "yDim": 2,
                "zDim": 2,
                "units": "in"
                }
            ],
            "items": [
                {
                "id": 0,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 1,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 2,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 3,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 4,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 5,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 6,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                },
                {
                "id": 7,
                "sku": "string",
                "description": "string",
                "length": 1,
                "width": 1,
                "height": 1,
                "units": "in"
                }
            ]
            }



            data=self.generic_logic(inputData)
            assert(data['arrangementPossible']==True)
            assert(data['multiBinPack']==False)


            selectedContainer=data['containers'][0]['id']
            for item in data['items']:
                assert(item['container']==selectedContainer)

            
            item1Tuple=(data['items'][0]['xCenter'],data['items'][0]['yCenter'],data['items'][0]['zCenter'])
            assert(item1Tuple==(.5,.5,.5))
            
            item2Tuple=(data['items'][1]['xCenter'],data['items'][1]['yCenter'],data['items'][1]['zCenter'])
            assert(item2Tuple==(.5,.5,1.5))

            item3Tuple=(data['items'][2]['xCenter'],data['items'][2]['yCenter'],data['items'][2]['zCenter'])
            assert(item3Tuple==(.5,1.5,.5))
            
            item4Tuple=(data['items'][3]['xCenter'],data['items'][3]['yCenter'],data['items'][3]['zCenter'])
            assert(item4Tuple==(.5,1.5,1.5))

            item5Tuple=(data['items'][4]['xCenter'],data['items'][4]['yCenter'],data['items'][4]['zCenter'])
            assert(item5Tuple==(1.5,.5,.5))

            item6Tuple=(data['items'][5]['xCenter'],data['items'][5]['yCenter'],data['items'][5]['zCenter'])
            assert(item6Tuple==(1.5,.5,1.5))

            item7Tuple=(data['items'][6]['xCenter'],data['items'][6]['yCenter'],data['items'][6]['zCenter'])
            assert(item7Tuple==(1.5,1.5,.5))

            item8Tuple=(data['items'][7]['xCenter'],data['items'][7]['yCenter'],data['items'][7]['zCenter'])
            assert(item8Tuple==(1.5,1.5,1.5))            


            print("Arrangments test 4 Passed")
        except:
            print("------------------Arrangments test 4 Failed")
    # QUESTION ASKED: expected behavior in the following use case
    # items: ['1x1x1','1x1x1']
    # containers:['2x2x1','2x1x1']
    def test_5(self):
        inputData={
        "multiBinPack": False,
        "timeoutDuration": 30,
        "containers": [
            {
            "sku": "unit",
            "description": "string",
            "xDim": 2,
            "yDim": 2,
            "zDim": 1,
            "units": "in"
            },
            {
            "sku": "unit",
            "description": "string",
            "xDim": 2,
            "yDim": 1,
            "zDim": 1,
            "units": "in"
            },

        ],
        "items": [
            {
            "id": 0,
            "sku": "string",
            "description": "string",
            "length": 1,
            "width": 1,
            "height": 1,
            "units": "in"
            },
            {
            "id": 1,
            "sku": "string",
            "description": "string",
            "length": 1,
            "width": 1,
            "height": 1,
            "units": "in"
            }
        ]
        }



        data=self.generic_logic(inputData)
        assert(data['arrangementPossible']==True)
        assert(data['multiBinPack']==False)
        selectedContainer=None
        for container in data['containers']:
            if (container['xDim']==2) and (container['yDim']==1 and container['zDim']==1):
                selectedContainer=container['id']

        for item in data['items']:
            assert(item['container']==selectedContainer)

        print("Arrangments test 5 Passed")
        
    # QUESTION ASKED: expected behavior (packing in smallest container) in following use case
    # items: ['4.5x9.75x7.93' for ele in range(0,20)]
    # containers:['18x24x18','29.25x12.75x23']
    
    def test_6(self):
        inputData={
        "multiBinPack": False,
        "timeoutDuration": 30,
        "containers": [

            {
            "sku": "unit",
            "description": "string",
            "xDim": 12.75,
            "yDim": 29.25,
            "zDim": 23,
            "units": "in"
            },
            {
            "sku": "unit",
            "description": "string",
            "xDim": 18,
            "yDim": 24,
            "zDim": 18,
            "units": "in"
            }

        ],
        "items": [
            {
            "id": 0,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 1,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 2,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 3,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 4,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 5,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 6,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 7,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 8,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 9,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 10,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 11,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 12,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 13,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 14,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 15,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 16,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 17,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 18,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            },
            {
            "id": 19,
            "sku": "string",
            "description": "string",
            "length": 4.5,
            "width": 9.75,
            "height": 7.93,
            "units": "in"
            }


        ]
        }
        import time
        start=time.time()
        data=self.generic_logic(inputData)
        end=time.time()
        
        assert(data['arrangementPossible']==True)
        assert(data['multiBinPack']==False)
        selectedContainer=None
        for container in data['containers']:
            if (container['xDim']==18) and (container['yDim']==24 and container['zDim']==18):
                selectedContainer=container['id']
        assert(len(data['items'])==20)
        for item in data['items']:
            if not (item['container']==selectedContainer):
                # 30 seconds/2 containers
                assert(end-start>15)

        print("Arrangments test 6 Passed")


    # PZ test case that tests if masterItemId matches the correct value
    def test_7(self):
        inputData={
        "multiBinPack": False,
        "timeoutDuration": 30,
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
        "items": [
            {
            "id": 6763,
            "sku": "string",
            "description": "string",
            "length": 1,
            "width": 1,
            "height": 1,
            "units": "in"
            },
            {
            "id": 6763,
            "sku": "string",
            "description": "string",
            "length": 1,
            "width": 1,
            "height": 1,
            "units": "in"
            },
            {
            "id": 6763,
            "sku": "string",
            "description": "string",
            "length": 1,
            "width": 1,
            "height": 1,
            "units": "in"
            }
        ]
        }

        import time
        start=time.time()
        data=self.generic_logic(inputData)
        end=time.time()
        
        assert(data['arrangementPossible']==True)
        assert(data['multiBinPack']==False)

        for item in data['items']:
             assert (item['masterItemId']==6763)
                # 30 seconds/2 containers

        print("Arrangments test 7 Passed")


    # DZ test case from December 10, 2020
    #     containers=[
    # '26x15.25x7.313',
    #'19.5x14.5x12.188'
    #,'16x12x12',
    #'22x16x15',
    #'18x18x24',
    #'10x10x12',
    #'21x16x10',
    #'29.25x12.75x23',
    #'2x2x1',
    #'2x2x1'
    #]
    # items=[21 gorilla gloves]
    # aka '9.75x4.438x7.875'
    def test_8(self):
        inputData={
        "multiBinPack": False,
        "timeoutDuration": 30,
        "containers": [
            {
            "sku": "string",
            "description": "string",
            "xDim": 26,
            "yDim": 15.25,
            "zDim": 7.313,
            "units": "in"
            },
            {
            "sku": "string",
            "description": "string",
            "xDim": 19.5,
            "yDim": 14.5,
            "zDim": 12.188,
            "units": "in"
            },
            {
            "sku": "string",
            "description": "string",
            "xDim": 16,
            "yDim": 12,
            "zDim": 12,
            "units": "in"
            },
            {
            "sku": "string",
            "description": "string",
            "xDim": 22,
            "yDim": 16,
            "zDim": 15,
            "units": "in"
            },
            {
            "sku": "string",
            "description": "string",
            "xDim": 18,
            "yDim": 18,
            "zDim": 24,
            "units": "in"
            },
            {
            "sku": "string",
            "description": "string",
            "xDim": 10,
            "yDim": 10,
            "zDim": 12,
            "units": "in"
            },
            {
            "sku": "string",
            "description": "string",
            "xDim": 21,
            "yDim": 16,
            "zDim": 10,
            "units": "in"
            },
            {
            "sku": "string",
            "description": "string",
            "xDim": 29.25,
            "yDim": 12.75,
            "zDim": 23,
            "units": "in"
            },
            {
            "sku": "string",
            "description": "string",
            "xDim": 2,
            "yDim": 2,
            "zDim": 1,
            "units": "in"
            },
            {
            "sku": "string",
            "description": "string",
            "xDim": 2,
            "yDim": 2,
            "zDim": 1,
            "units": "in"
            }
        ],
        "items": [
            {
            "id": 100,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 101,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 102,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 103,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 104,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 105,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 106,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 107,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 108,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 109,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 110,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 111,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 112,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 113,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 114,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 115,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 116,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 117,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 118,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 119,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            },
            {
            "id": 120,
            "sku": "string",
            "description": "gorillaGloves",
            "length": 9.75,
            "width": 4.438,
            "height": 7.875,
            "units": "in"
            }
        ]
        }

        import time
        start=time.time()
        data=self.generic_logic(inputData)
        end=time.time()
        assert(data['arrangementPossible']==True)
        assert(data['multiBinPack']==False)
        selectedContainer=None
        foundContainerId=data['items'][0]['container']
        # all items point to same container
        assert(len(data['items'])==21)
        for item in data['items']:
            assert(foundContainerId==item['container'])


        selectedContainer=None
        for container in data['containers']:
            if container['id']==foundContainerId:
                selectedContainer=container   
        foundContainerString=(str(selectedContainer['xDim'])+'x'+str(selectedContainer['yDim'])+'x'+str(selectedContainer['zDim']))
        assert(foundContainerString=='29.25x12.75x23.0')
        print('Arrangments test 8 Passed')