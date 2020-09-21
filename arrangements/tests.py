
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
    

    # checks on the data, will print -----------Failed Arrangments Test 2 if these fail

    assert(data['arrangementPossible']==False)
    assert(data['multiBinPack']==False)
    assert(len(data['items'])==5)
    for item in data['items']:
        # null container field
        assert(item['container']==None)
    assert(len(data['containers'])==1)
    return client




# QUESTION ASKED: what is the behavior when we try to optimize boxes into multiple containers (and there is one best container)
# return all containers that are filled
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
    assert(len(data['items'])==4)
    assert(len(data['containers'])==2)
    usedContainerId=None
    for container in data['containers']:
        if container['xDim']==2 and (container['yDim']==2 and container['zDim']==1):
            usedContainerId=container['id']
    for item in data['items']:
        assert(item['container']==usedContainerId)
    return client

# QUESTION ASKED: does the items returned match the order of the rendering (in at least one case)
def test_4(client):
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
    
    return client

# QUESTION ASKED: expected behavior in the following use case
# items: ['1x1x1','1x1x1']
# containers:['2x2x1','2x1x1']
def test_5(client):
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
    selectedContainer=None
    for container in data['containers']:
        if (container['xDim']==2) and (container['yDim']==1 and container['zDim']==1):
            selectedContainer=container['id']

    for item in data['items']:
        assert(item['container']==selectedContainer)
        #assert(item['container']==selectedContainer)
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


try:
    client=test_4(client)
    print('Passed Arrangments Test 4')
except:
    print('------------Failed Arrangments Test 4')


try:
    client=test_5(client)
    print('Passed Arrangments Test 5')
except:
    print('------------Failed Arrangments Test 5')
