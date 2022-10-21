import aiohttp
import asyncio
import json
import time


async def get_shippo_shipment(session, url):
    async with session.get(url) as resp:
        shippo_shipment = await resp.json()
        return shippo_shipment
        

async def get_all_shippo_shipments(shipmentIds, shippo_api_key, production):
    shipmentsToReturn = []
    if production:
        headers={'Authorization': f'Bearer {shippo_api_key}'}
    else:
        headers={'Authorization': f'ShippoToken {shippo_api_key}'}

    async with aiohttp.ClientSession(headers=headers) as session:

        tasks = []
        for shipmentId in shipmentIds:

            url = f'https://api.goshippo.com/shipments/{shipmentId}'
            print(url)
            tasks.append(asyncio.ensure_future(get_shippo_shipment(session, url)))

        shippo_shipments = await asyncio.gather(*tasks)
        
        for shippo_shipment in shippo_shipments:
            # print(shippo_shipment)
            shipmentsToReturn.append(shippo_shipment)

    return shipmentsToReturn

def lambda_handler(event, context):
    body = event['body']
    body = json.loads(body)
    shippo_api_key = body['SHIPPO_API_KEY']
    shipmentIds = body['shipmentIds']
    production = body['production']
    
    # Try getting shippo shipments until all shipments are returned with status SUCCESS
    timeBetweenRequests = [0, 1, 2, 2.5, 3, 4, 4.5]
    for t_req in timeBetweenRequests:
        shipmentsToReturn = asyncio.run(get_all_shippo_shipments(shipmentIds, shippo_api_key, production))
        
        allShipmentsSuccessStatus = True
        for shipment in shipmentsToReturn:
            if shipment['status']!='SUCCESS':
                allShipmentsSuccessStatus = False
                break
        
        if allShipmentsSuccessStatus:
            print("all shipments returned success status")
            print("time between requests", t_req)
            break
        else:
            print("not all shipments returned success status")
            time.sleep(t_req)
    return {
        'statusCode': 200,
        'body': json.dumps(shipmentsToReturn)
    }


# I had to get shipmentId from quoteId -> get quote/quoteId, 
# Uncomment the following lines to test

'''
b={
    "SHIPPO_API_KEY":"shippo_test_41c916402deba95527751c894fd23fc03d7d8198",
    "shipmentIds": ["8b848ca670674f84ba8ec638b02e5f09", "8b848ca670674f84ba8ec638b02e5f09"]
}

    

json_b = json.dumps(b)
e = {"body":json_b}
a = lambda_handler(e, 1)
print(a)
'''