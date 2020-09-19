# to run (everything, not just this test file) use
# ./manage.py test

# Using the standard RequestFactory API to create a form POST request
def test_1():
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

    from rest_framework.test import APIClient, APIRequestFactory
    from rest_framework.authtoken.models import Token
    from arrangements.views import ArrangementList, Arrangement
    from rest_framework.test import force_authenticate

    import json
    from users.models import User

    client = APIClient()
    factory = APIRequestFactory()


    pz_user = User.objects.get(email='peter.douglas.zach@gmail.com')
    pz_view = ArrangementList.as_view()

    pz_request = factory.post('/arrangements/',json.dumps(inputData), content_type='application/json')
    force_authenticate(pz_request, user=pz_user)
    pz_response = pz_view(pz_request)
    data=pz_response.data
    

    # checks on the data, will print -----------Failed Arrangments Test 1 if these fail

    assert(data['arrangementPossible']==True)
    assert(data['multiBinPack']==False)


try:
    test_1()
    print('Passed Arrangments Test 1')
except:
    print('------------Failed Arrangments Test 1')
 


