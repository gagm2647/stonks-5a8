import json
import uuid
import urllib3
from decouple import config

class SquareAPI:

    def __init__(self):

        self.http = urllib3.PoolManager()
        self.head = {
            'Content-Type': 'application/json',
            'Square-Version': '2022-03-16',
            'Authorization': "Bearer " + config("API_TOKEN")
        }
        self.url = 'https://connect.squareupsandbox.com/v2/'

    def squareAPI_GET(self, request):

        r = self.http.request(
            'GET',
            self.url + request,
            headers=self.head
        )

        if r.status > 299:
            raise Exception("API call return status: " + str(r.status) + " Error: " + r.data.decode('utf-8'))

        return json.loads(r.data.decode('utf-8'))

    def squareAPI_POST(self, request, data):

        encoded_data = json.dumps(data).encode('utf-8')

        r = self.http.request(
            'POST',
            self.url + request,
            body=encoded_data,
            headers=self.head
        )

        if r.status > 299:
            raise Exception("API call return status: " + str(r.status) + " Error: " + r.data.decode('utf-8'))

        return json.loads(r.data.decode('utf-8'))

    def getPriceOf(self, itemName):

        catalog_list = self.squareAPI_GET('catalog/list')

        for index in range(len(catalog_list['objects'])):

            if catalog_list['objects'][index]["type"] == "ITEM":
                if catalog_list['objects'][index]['item_data']['name'] == itemName:
                    return int(catalog_list['objects'][index]['item_data']['variations'][0]['item_variation_data'][
                                   'price_money']['amount'])

        raise Exception("Item not found")

    def setPriceOf(self, itemName, amount):

        catalog_list = self.squareAPI_GET('catalog/list')
        found = False

        for index in range(len(catalog_list['objects'])):

            if catalog_list['objects'][index]["type"] == "ITEM":
                if catalog_list['objects'][index]['item_data']['name'] == itemName:
                    found = True
                    catalog_list['objects'][index]['item_data']['variations'][0]['item_variation_data']['price_money'][
                        'amount'] = amount

        if not found:
            raise Exception("Item not found")

        data = {
            "batches": [
                {
                    "objects": catalog_list['objects']
                }
            ],
            "idempotency_key": str(uuid.uuid4()),
        }

        self.squareAPI_POST('catalog/batch-upsert', data)
