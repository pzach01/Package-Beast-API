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
    # lowercase post returns byte code this returns subscriptable object

    from rest_framework.test import APIClient, APIRequestFactory
    from rest_framework.authtoken.models import Token


    client = APIClient()
    from users.models import User
    
    factory = APIRequestFactory()
    request = factory.post('/arrangments/',inputData)

    user = User.objects.get(email='lucas.j.zach@gmail.com')
    client = APIClient()
    client.login(username='lucas.j.zach@gmail.com', password='Letsgetit35!')
    tokens = Token.objects.all()
    token=tokens[len(tokens)-1]
    print(tokens)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


    response=client.post('/arrangments/', request, format='json')
    print(response)
test_1()
