import boto3, json
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Key, Attr, Not

TABLE_NAME_STR = 'FoodProducts'
INDEX_NAME_STR = 'special_GSI'
DDB = boto3.resource('dynamodb', region_name='us-east-1')
    
def lambda_handler(event, context):
   
    offer_path_str = event.get('path')
    if offer_path_str is not None:
        return scan_index(event, context)
    else:
        pass
    print("running scan on table")
    
    DDB = boto3.resource('dynamodb', region_name='us-east-1')

    TABLE = DDB.Table(TABLE_NAME_STR)
    
    response = TABLE.scan()
    
    data = response['Items']
    

    
    while 'LastEvaluatedKey' in response:
        response = TABLE.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        print("We needed to paginate and extend the response")
        data.extend(response['Items'])
        
    #python return non standard JSON
    #so we need a helper to convet Decimal('595') and special returned by dynamo 
    #to an integer like 595
    for item in data:
       item['price_in_cents_int'] = item.pop('price_in_cents')
       if item.get('special') is not None:
         item['special_int'] = item.pop('special')
       item['tag_str_arr'] = item.pop('tags')
       item['description_str'] = item.pop('description')
       item['product_name_str'] = item.pop('product_name')
       item['product_id_str'] = item.pop('product_id')
       
       if item['price_in_cents_int']:
            item['price_in_cents_int'] = int(item['price_in_cents_int'])
       if item.get('special_int') is not None:
            item['special_int'] = int(item['special_int'])

    return_me={"product_item_arr": data}
    
    return return_me
    
def scan_index(event, context):

    print("running scan on index")
    ## event and context not used
    TABLE = DDB.Table(TABLE_NAME_STR)

    
    response = TABLE.scan(
        IndexName=INDEX_NAME_STR,
        FilterExpression=Not(Attr("tags").contains("out of stock"))
    )

    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = TABLE.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            IndexName=INDEX_NAME_STR,
            FilterExpression=Not(Attr("tags").contains("out of stock"))
        )
        print("We needed to paginate and extend the response")
        data.extend(response['Items'])
        
    #python return non standard JSON
    #so we need a helper to convet Decimal('595') and special returned by dynamo 
    #to an integer like 595
    for item in data:
       item['price_in_cents_int'] = item.pop('price_in_cents')
       item['special_int'] = item.pop('special')
       item['tag_str_arr'] = item.pop('tags')
       item['description_str'] = item.pop('description')
       item['product_name_str'] = item.pop('product_name')
       item['product_id_str'] = item.pop('product_id')
       
       if item['price_in_cents_int']:
            item['price_in_cents_int'] = int(item['price_in_cents_int'])
       if item.get('special_int') is not None:
            item['special_int'] = int(item['special_int'])

    return_me = {
        "product_item_arr": data
    }
    return return_me

    
#remove this line below once you have tested locally and wish to deploy
#print(lambda_handler({}, None))


"""
Copyright @2021 [Amazon Web Services] [AWS]
    
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
