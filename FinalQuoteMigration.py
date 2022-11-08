import sys

original_stdout = sys.stdout

with open('FinalQuoteLog.txt', 'a') as f:
    sys.stdout = f

    import csv
    import requests

    base_url = "fbu-qa.pricefx.eu"
    partition = "iplex-dev"


    def ProductMigration():
        with open("Quote/FinalProductCustomerDataCSV/FinalProductMapping.csv", 'r') as file1:
            csvreader = csv.reader(file1)
            Migration1 = {}
            for row in csvreader:
                Migration1[row[0]] = row[1]
            # print(Migration1)
            return (Migration1)


    # ProductMigration()

    def CustomerMigration():
        with open("Quote/FinalProductCustomerDataCSV/FinalCustomerMapping.csv", 'r') as file2:
            csvreader = csv.reader(file2)
            Migration2 = {}
            for row in csvreader:
                Migration2[row[0]] = row[1]
            # print(Migration2)
            return (Migration2)


    # CustomerMigration()

    def UpdateQuoteRecord(quoteIdList):
        productTranslationMap = ProductMigration()
        customerTranslationMap = CustomerMigration()

        for quote in quoteIdList:
            if 'typeId' in quote and quote['typeId']:
                hasCustomerId = False
                hasSku = False
                print('Updating payload for quote Id: ' + quote['typeId'])
                newQuote = getSingleQuote(quote['typeId'])

                updatedCustomerId = newQuote['customerId']


                if newQuote['customerId'] in customerTranslationMap:
                    print('Previuos Customer Id: ' + newQuote['customerId'])
                    if 'customerId' in newQuote:
                        hasCustomerId = True
                        updatedCustomerId = customerTranslationMap[newQuote['customerId']]
                        print('Updated Customer Id: ' + updatedCustomerId)
                else:
                    print('No customer Id exist in migration file')


                updatedInputs = []
                inputs = newQuote['inputs'] if 'inputs' in newQuote else []
                for item in inputs:
                    if item['type'] == 'CUSTOMER':
                        item['value'] = updatedCustomerId
                    updatedInputs.append(item)



                items = newQuote['lineItems']
                updatedLineItems = []
                for line in items:
                    if line['sku'] in productTranslationMap:
                        hasSku = True
                        print('Previuos sku: ' + line['sku'])
                        line['sku'] = productTranslationMap[line['sku']]
                        print('Updated sku: ' + line['sku'])
                    else:
                        print('No sku exist in migration file')
                    updatedLineItems.append(line)

                newQuote['lineItems'] = updatedLineItems
                newQuote['inputs'] = updatedInputs




                payload = {
                    "data": {
                        "quote": newQuote,
                    }
                }
                print('Updated payload is:')
                print(payload)

                if hasSku or hasCustomerId:
                    upsertQuote(payload)
                else:
                    print('No migration, so, upsert was not called')


    def upsertQuote(payload):
        url = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.save"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers, auth=('iplex-dev/sm.hasan', 'start123'))
        data = response.json()['response']['data']
        print('"Response after upsert: ')
        print(response.json())


    def getSingleQuote(typed_id):
        url = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetch/" + typed_id
        response = requests.post(url, auth=('iplex-dev/sm.hasan', 'start123'))

        data = response.json()['response']['data'][0]
        print(data)
        return data


    def getAllQuote():
        url = "https://" + base_url + "/pricefx/" + partition + "/quotemanager.fetchlist"

        payload = {
            "endRow": 581,
            "oldValues": None,
            "operationType": "fetch",
            "startRow": 0,
            "textMatchStyle": "exact",
            # "data": {
            #     "_constructor": "AdvancedCriteria",
            #     "operator": "and",
            #     "criteria": [
            #         {
            #             "fieldName": "",
            #             "operator": "",
            #             "value": ""
            #         }
            #     ]
            # }
        }

        headers = {"Content-Type": "application/json"}

        print('Getting All Quotes.....')

        response = requests.post(url, json=payload, headers=headers, auth=('iplex-dev/sm.hasan', 'start123'))

        data = response.json()['response']['data']
        idList = []
        for item in data:
            idList.append({'typeId': item['typedId'], 'uniqueName': item['uniqueName']})
        print('Got All Quotes.')
        # print(idList)
        return idList


    allQuoteId = getAllQuote()
    UpdateQuoteRecord(allQuoteId)



    sys.stdout = original_stdout

