
# to run (everything, not just this test file) use
# ./manage.py test




from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.authtoken.models import Token
from arrangements.views import ArrangementList, Arrangement
from rest_framework.test import force_authenticate
from users.models import User


# QUESTION ASKED: does the code work in some basic form?, 
def test_1(client):
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



    factory = APIRequestFactory()


    pz_user = User.objects.get(email='peter.douglas.zach@gmail.com')
    pz_view = ArrangementList.as_view()

    pz_request =factory.post('/arrangements/',data=inputData, format='json')

    force_authenticate(pz_request, user=pz_user)
    pz_response = pz_view(pz_request)
    data=pz_response.data
    

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
    return client
# QUESTION ASKED: what is the expected behavior when not all the container fit?
# arrangment possible should return false
## ASK PETER: do containers and items still need to be returned in the event of a failure; simple fix in serializer if not
def test_2(client):
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



    factory = APIRequestFactory()


    pz_user = User.objects.get(email='peter.douglas.zach@gmail.com')
    pz_view = ArrangementList.as_view()

    pz_request =factory.post('/arrangements/',data=inputData, format='json')

    force_authenticate(pz_request, user=pz_user)
    pz_response = pz_view(pz_request)
    data=pz_response.data
    

    # checks on the data, will print -----------Failed Arrangments Test 1 if these fail

    assert(data['arrangementPossible']==False)
    assert(data['multiBinPack']==False)

    return client




# QUESTION ASKED: what is the behavior when we try to optimize boxes into multiple containers (and there is one best container)
# only return containers that are filled
def test_3(client):
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



    factory = APIRequestFactory()


    pz_user = User.objects.get(email='peter.douglas.zach@gmail.com')
    pz_view = ArrangementList.as_view()

    pz_request =factory.post('/arrangements/',data=inputData, format='json')

    force_authenticate(pz_request, user=pz_user)
    pz_response = pz_view(pz_request)
    data=pz_response.data
    

    # checks on the data, will print -----------Failed Arrangments Test 1 if these fail

    assert(data['arrangementPossible']==True)
    assert(data['multiBinPack']==False)
    # only include containers that are filled
    assert(len(data['containers'])==1)
    usedContainerId=data['containers'][0]['id']
    for item in data['items']:
        assert(item['container']==usedContainerId)
    return client



from rest_framework.test import APIClient
client = APIClient()

try:
    client=test_1(client)
    print('Passed Arrangments Test 1')
except:
    print('------------Failed Arrangments Test 1')
    




try:
    client=test_2(client)
    print('Passed Arrangments Test 2')
except:
    print('------------Failed Arrangments Test 2')

try:
    client=test_3(client)
    print('Passed Arrangments Test 3')
except:
    print('------------Failed Arrangments Test 3')
