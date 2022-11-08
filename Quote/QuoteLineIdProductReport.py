import csv
import requests

base_url = "fbu-qa.pricefx.eu"
partition = "iplex-dev"


def getproduct(typed_id):
    # url1 = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetchproducts"

    url2 = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetch/" + typed_id
    response2 = requests.get(url2, auth=('iplex-dev/sm.hasan', 'start123'))
    data = response2.json()['response']['data'][0]

    rowitems = []
    lineItems = data["lineItems"]
    for obj in lineItems:
        ourObject = {'typed_id': "P-" + typed_id.replace('.Q','')}
        ourObject['lineId'] = obj["lineId"]
        ourObject['sku'] = obj["sku"]
        rowitems.append(ourObject)
    print(rowitems)
    return rowitems


# getproduct('114.Q')

url = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetchlist"

payload = {
    "endRow": 570,
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

response = requests.post(url, json=payload, headers=headers, auth=('iplex-dev/sm.hasan', 'start123'))
myjson = response.json()["response"]["data"]

ourdata = []
csvheader = ['UNIQUE-NAME', 'LINE-ID', 'PRODUCT-ID']

for x in myjson:
    unqname = x["uniqueName"] if "uniqueName" in x else ""
    listing = getproduct(unqname.split("-")[1] + ".Q")
    for item in listing:
        ourdata.append([item['typed_id'], item['lineId'], item['sku']])

with open('02.After_quote_LineId_ProductId_report.csv ', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(csvheader)
    writer.writerows(ourdata)

# print(myjson)
