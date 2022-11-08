import csv

base_url = "fbu-qa.pricefx.eu"
partition = "iplex-dev"


def getproduct(typed_id):
    # url1 = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetchproducts"

    url2 = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetch/" + typed_id
    response2 = requests.get(url2, auth=('iplex-dev/sm.hasan', 'start123'))
    data = response2.json()['response']['data'][0]

    skus = []

    lineItem = data["lineItems"]
    for product in lineItem:
        if "sku" in product and product["sku"]:
            skus.append(product["sku"])

    print(typed_id)
    productsku = " | ".join(skus) if skus else ""

    return productsku


import requests

base_url = "fbu-qa.pricefx.eu"
partition = "iplex-dev"

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
csvheader = ['UNIQUE-NAME', 'CUSTOMER-ID']


for x in myjson:
    cusId = x["customerId"] if "customerId" in x else ""
    unqname = x["uniqueName"] if "uniqueName" in x else ""
    productId = ""

    # if unqname:
    if len(unqname) != 0:
        productId = getproduct(unqname.split("-")[1] + ".Q")
    else:
        ""


    # productId = getProduct(unqname.split('P-')[1])

    listing = [unqname, cusId ]
    ourdata.append(listing)

with open('01.After_quote_Customer_report.csv ', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(csvheader)
    writer.writerows(ourdata)

# print(myjson)
