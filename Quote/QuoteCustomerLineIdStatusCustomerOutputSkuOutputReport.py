import csv
import requests

base_url = "fbu-qa.pricefx.eu"
partition = "iplex-qa"


def getproduct(typed_id):
    # url1 = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetchproducts"

    url2 = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetch/" + typed_id
    response2 = requests.get(url2, auth=('iplex-qa/sm.hasan', 'pricefx123'))
    data = response2.json()['response']['data'][0]

    rowItems = []
    type_id = "P-" + typed_id.replace('.Q', '')
    customerId = data['customerId'] if 'customerId' in data else ''
    quotestatus = data['quoteStatus'] if 'quoteStatus' in data else ''

    lineItems = data["lineItems"] if 'lineItems' in data else []
    for obj in lineItems:
        lineId = obj["lineId"]
        sku = obj["sku"]
        customerInOutput = ''
        prodIdInOutput = ''
        outputs = obj['outputs']
        for output in outputs:
            if output['resultName'] == 'Customer':
                customerInOutput = output['result']
            if output['resultName'] == 'ProductCode':
                prodIdInOutput = output['result']

        ourObject = {
            "typed_id": type_id,
            "customerId": customerId,
            "quoteStatus": quotestatus,
            "lineId": lineId,
            "sku": sku,
            "customerInOutput": customerInOutput,
            "prodIdInOutput": prodIdInOutput
        }
        rowItems.append(ourObject)

    # print(rowItems)
    return rowItems


# getproduct('114.Q')

url = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetchlist"

payload = {
    "endRow": 600,
    "oldValues": None,
    "operationType": "fetch",
    "startRow": 0,
    "textMatchStyle": "exact",
    "data": {
        "_constructor": "AdvancedCriteria",
        "operator": "and",
        "criteria": [
            {
                "fieldName": "",
                "operator": "",
                "value": ""
            }
        ]
    }
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers, auth=('iplex-qa/sm.hasan', 'pricefx123'))
myjson = response.json()["response"]["data"]

ourdata = []
csvheader = ['QuoteId', 'CustomerId (Header Input)', 'Quote Status', 'lineId', 'sku (from LineItem)',
             'CustomerId (from output)', 'Product Code (from output)']

for x in myjson:
    unqname = x["uniqueName"] if "uniqueName" in x else ""
    listing = getproduct(unqname.split("-")[1] + ".Q")
    for item in listing:
        ourdata.append([item['typed_id'], item['customerId'], item['quoteStatus'], item['lineId'], item['sku'],
                        item['customerInOutput'], item['prodIdInOutput']])

with open('QuoteReportStatus.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(csvheader)
    writer.writerows(ourdata)

print(ourdata)
