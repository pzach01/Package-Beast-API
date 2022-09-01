import aiohttp
import asyncio
import time
import json


async def create_shippo_address(session, url, address):
    address['validate']=True
    async with session.post(url, json=address) as resp:
        shippo_address = await resp.json()
        return shippo_address

async def create_shippo_shipment(session, url, shipment):
    async with session.post(url, json=shipment) as resp:
        print(resp)
        shippo_shipment = await resp.json()
        return shippo_shipment


async def create_shippo_shipments(shipments, shippo_api_key):
    headers={'Authorization': f'ShippoToken {shippo_api_key}'}

    async with aiohttp.ClientSession(headers=headers) as session:

        tasks = []

        url = f'https://api.goshippo.com/shipments/'

        for shipment in shipments:
            tasks.append(asyncio.ensure_future(create_shippo_shipment(session, url, shipment)))
        shippo_shipments = await asyncio.gather(*tasks)

        shipmentsToReturn = []
        for shippo_shipment in shippo_shipments:
            shipmentsToReturn.append(shippo_shipment)
        return shipmentsToReturn


async def create_shippo_addresses(address_from, address_to, shippo_api_key):
    headers={'Authorization': f'ShippoToken {shippo_api_key}'}

    async with aiohttp.ClientSession(headers=headers) as session:

        tasks = []

        url = f'https://api.goshippo.com/addresses/'
        tasks.append(asyncio.ensure_future(create_shippo_address(session, url, address_from)))
        tasks.append(asyncio.ensure_future(create_shippo_address(session, url, address_to)))

        shippo_addresses = await asyncio.gather(*tasks)

        addressesToReturn = []
        for shippo_address in shippo_addresses:
            addressesToReturn.append(shippo_address)
        return addressesToReturn[0], addressesToReturn[1]


def lambda_handler(event, context):
    body = event['body']
    body = json.loads(body)
    shippo_api_key = body['SHIPPO_API_KEY']

    address_from = body['address_from']
    address_to = body['address_to']

    shipment = body
    del shipment['SHIPPO_API_KEY']

    # Take list of parcels and make a list of shipments, each with one parcel.
    shipments = []
    parcels = shipment['parcels']
    for parcel in  parcels:
        shipment['parcels'] = [parcel]
        shipments.append(shipment)

    start_time = time.time()
    addressFrom, addressTo = asyncio.run(create_shippo_addresses(address_from, address_to, shippo_api_key))

    if not addressFrom['validation_results']['is_valid']:
        return {
            'statusCode': 200,
            'body': json.dumps({'messages':['invalid from address']})
        }
    if not addressTo['validation_results']['is_valid']:
        return {
            'statusCode': 200,
            'body': json.dumps({'messages':['invalid to address']})
        }

    if addressFrom['street1'].lower() == addressTo['street1'].lower() and addressFrom['zip'] == addressTo['zip']:
        return {
            'statusCode': 200,
            'body': json.dumps({'messages':['same from and to addresses']})
        }

    print("address time", time.time()-start_time)
    start_time = time.time()

    shipmentsToReturn = asyncio.run(create_shippo_shipments(shipments, shippo_api_key))

    print("shipment time", time.time()-start_time)

    return {
        'statusCode': 200,
        'body': json.dumps(shipmentsToReturn)
    }


b={
    "SHIPPO_API_KEY":"shippo_test_41c916402deba95527751c894fd23fc03d7d8198",
    "address_from":{
        "name":"peter",
        "street1": "1349 Hertz Drive SE",
        "street2": "",
        "city": "Cedar Rapids",
        "state": "IA",
        "zip": 54302,
        "country":"US",
        "phone":"+1 319 329 8349",
        "email": "mrhippo@goshippo.com"
    },
    "address_to":{
        "name":"peter",
        "street1": "1349 Hertz Drive SE",
        "street2": "",
        "city": "Cedar Rapids",
        "state": "IA",
        "zip": 54302,
        "country":"US",
        "phone":"+1 319 329 8349",
        "email": "mrhippo@goshippo.com"
    },
    "parcels": [{
        "length": "10",
        "width": "15",
        "height": "10",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "8",
        "width": "6",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "8",
        "width": "7",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "9",
        "width": "8",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    },{
        "length": "10",
        "width": "15",
        "height": "10",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "8",
        "width": "6",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "8",
        "width": "7",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "9",
        "width": "8",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "10",
        "width": "15",
        "height": "10",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "8",
        "width": "6",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "8",
        "width": "7",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "9",
        "width": "8",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    },{
        "length": "10",
        "width": "15",
        "height": "10",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "8",
        "width": "6",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "8",
        "width": "7",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }, {
        "length": "9",
        "width": "8",
        "height": "8",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb"
    }],
    "async": True
}


json_b = json.dumps(b)
e = {"body":json_b}

a = lambda_handler(e, 1)
print(a)

