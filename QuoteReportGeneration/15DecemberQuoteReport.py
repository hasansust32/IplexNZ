
import csv
import requests

base_url = "fbu-qa.pricefx.eu"
partition = "iplex-qa2"


def getproduct(typed_id):
    # url1 = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetchproducts"

    url2 = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetch/" + typed_id
    response2 = requests.get(url2, auth=('iplex-qa2/hasan', 'Pricefx123'))
    data = response2.json()['response']['data'][0]

    rowItems = []
    type_id = "P-" + typed_id.replace('.Q','')
    customerId = data['customerId'] if 'customerId' in data else ''
    quotestatus = data['quoteStatus'] if 'quoteStatus' in data else ''

    lineItems = data["lineItems"] if 'lineItems' in data else []

    for obj in lineItems:
      lineIdInLineItem = obj["lineId"]
      skuInLineItem = obj["sku"]
      
      customerInLineItem=''
      prodIdInLineItem=''
      ProductTypeInLineItem=''
      UnitOfMeasureInLineItem=''
      TotalLengthInLineItem=''
      PipeLengthInLineItem=''
      CalculatedQuantityInLineItem=''
      WeightInLineItem=''
      TotalLineWeightInLineItem=''
      ListPriceInLineItem=''
      DiscountInLineItem=''
      PriceLineItem=''
      FinalCustomerPriceInLineItem=''
      MarginInLineItem=''


      outputs = obj['outputs']
      for output in outputs:
        if output['resultName'] == 'Customer':
          customerInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'ProductCode':
          prodIdInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'ProductType':
          ProductTypeInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'UnitOfMeasure':
          UnitOfMeasureInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'TotalLength':
          TotalLengthInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'PipeLength':
          PipeLengthInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'CalculatedQuantity':
          CalculatedQuantityInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'Weight':
          WeightInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'TotalLineWeight':
          TotalLineWeightInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'ListPrice':
          ListPriceInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'Discount':
          DiscountInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'Price':
          PriceLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'FinalCustomerPrice':
          FinalCustomerPriceInLineItem = output['result'] if 'result' in output else ''
        if output['resultName'] == 'Margin':
          MarginInLineItem = output['result'] if 'result' in output else ''
      
      


      HeaderQuoteNumber =''
      HeaderCustomerNumber=''
      HeaderOpportunityID=''
      HeaderCustomerReference=''
      HeaderContact=''
      HeaderStockLocation=''
      HeaderTotalQuoteValue=''
      HeaderOverallQuoteMargin=''

      HeaderOutput = data["outputs"] if 'outputs' in data else []
      for obj in HeaderOutput:
        if obj['resultName'] == 'externalRef':
          HeaderQuoteNumber = obj['result'] if 'result' in obj else ''
        if obj['resultName'] == 'customer':
          HeaderCustomerNumber = obj['result'] if 'result' in obj else ''
        if obj['resultName'] == 'opportunityID':
          HeaderOpportunityID = obj['result'] if 'result' in obj else ''
        if obj['resultName'] == 'customerReference':
          HeaderCustomerReference = obj['result'] if 'result' in obj  else ''
        if obj['resultName'] == 'contact':
          HeaderContact = obj['result'] if 'result' in obj else ''
        if obj['resultName'] == 'stockLocation':
          HeaderStockLocation = obj['result'] if 'result' in obj else ''
        if obj['resultName'] == 'totalQuoteValue':
          HeaderTotalQuoteValue = obj['result'] if 'result' in obj else ''
        if obj['resultName']== 'overallQuoteMargin':
          HeaderOverallQuoteMargin = obj['result'] if 'result' in obj else ''
        
        

      ourObject = {
          "typed_id": type_id, 
          "customerId": customerId, 
          "quoteStatus" : quotestatus,
          "HeaderQuoteNumber" : HeaderQuoteNumber,
          "HeaderCustomerNumber": HeaderCustomerNumber,
          "HeaderOpportunityID": HeaderOpportunityID,
          "HeaderCustomerReference": HeaderCustomerReference,
          "HeaderContact": HeaderContact,
          "HeaderStockLocation": HeaderStockLocation,
          "HeaderTotalQuoteValue": HeaderTotalQuoteValue,
          "HeaderOverallQuoteMargin": HeaderOverallQuoteMargin,
          "lineIdInLineItem": lineIdInLineItem, 
          "skuInLineItem": skuInLineItem,
          "customerInLineItem" : customerInLineItem,
          "prodIdInLineItem": prodIdInLineItem,
          "ProductTypeInLineItem" : ProductTypeInLineItem,
          "UnitOfMeasureInLineItem": UnitOfMeasureInLineItem,
          "TotalLengthInLineItem": TotalLengthInLineItem,
          "PipeLengthInLineItem": PipeLengthInLineItem,
          "CalculatedQuantityInLineItem": CalculatedQuantityInLineItem,
          "WeightInLineItem" : WeightInLineItem,
          "TotalLineWeightInLineItem": TotalLineWeightInLineItem,
          "ListPriceInLineItem": ListPriceInLineItem,
          "DiscountInLineItem": DiscountInLineItem,
          "PriceLineItem" : PriceLineItem,
          "FinalCustomerPriceInLineItem" : FinalCustomerPriceInLineItem,
          "MarginInLineItem" : MarginInLineItem

          
        }
      rowItems.append(ourObject)


      
    # print(rowItems)
    return rowItems


# getproduct('114.Q')

url = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetchlist"

payload = {
    "endRow": 410,
    "oldValues": None,
    "operationType": "fetch",
    "startRow": 400,
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

response = requests.post(url, json=payload, headers=headers, auth=('iplex-qa2/hasan', 'Pricefx123'))
myjson = response.json()["response"]["data"]

ourdata = []
csvheader = ['TypedId', 'CustomerId', 'Quote Status', 'Header Quote Number', 'Header Customer  Number' ,
             'Header Opportunity Id', 'Header Customer Reference', 'Header Contact', 'Header Stock Location', 
             'Header Total Quote Value', 'Header Overall Quote Margin', 'lineId in LineItem', 'SKU in LineItem',
             'Customer in LineItem', 'ProductId in LineItem', 'Product Type in LineItem', 'Unit of measure in LineItem', 
             'Total Length in LineItem', 'Pipe Length in LineItem', 'Calculated Quentity in LineItem', 'Weight in LineItem', 
             'Total Line Weight in LineItem', 'ListPrice in LineItem', 'Discount in LineItem', 'Price in LineItem', 
             'Final Customer Price in LineItem', 'Margin in LineItem'  ]

for x in myjson:
  unqname = x["uniqueName"] if "uniqueName" in x else ""
  listing = getproduct(unqname.split("-")[1] + ".Q")
  for item in listing:
    ourdata.append([item['typed_id'], item['customerId'], item['quoteStatus'], item['HeaderQuoteNumber'],
                    item['HeaderCustomerNumber'], item['HeaderOpportunityID'],  item['HeaderCustomerReference'], 
                    item['HeaderContact'], item['HeaderStockLocation'], item['HeaderTotalQuoteValue'],
                    item['HeaderOverallQuoteMargin'], item['lineIdInLineItem'], item['skuInLineItem'], 
                    item['customerInLineItem'], item['prodIdInLineItem'], item['ProductTypeInLineItem'], 
                    item['UnitOfMeasureInLineItem'], item['TotalLengthInLineItem'], item['PipeLengthInLineItem'], 
                    item['CalculatedQuantityInLineItem'], item['WeightInLineItem'], item['TotalLineWeightInLineItem'],
                    item['ListPriceInLineItem'], item['DiscountInLineItem'], item['PriceLineItem'], 
                    item['FinalCustomerPriceInLineItem'], item['MarginInLineItem']
                    
                    ])
     

with open('UpdatedQuoteReport-4.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(csvheader)
    writer.writerows(ourdata)


