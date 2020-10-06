import json
import os
import boto3

lex_model = boto3.client('lex-models')

# ddb = boto3.client('dynamodb')

dynamodb = boto3.resource('dynamodb')


def last_name(event, context):
    # TODO implement
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
    table = dynamodb.Table('names_test')
    data = scanData(table) #data = list
    unique_last = removeDuplicates(data)
    unique_last_names = []
    for i in unique_last:
        # unique_first_names.append(i.replace("first_name", "value"))
        i["value"] = i["last_name"]
        del(i["last_name"])
        unique_last_names.append(i)
    print(unique_last_names)

    get_values = lex_get_slot_values(unique_last)
    # latest_slot = lex_model.create_slot_type_version(name = 'LastName')
    latest_bot = lex_model.create_bot_version(name = 'names_test')
    return unique_last

def scanData(table):
    scan_kwargs = {
        'ProjectionExpression': "last_name",
    }
    response = table.scan(**scan_kwargs)
    data = response['Items']
    return data
    
def lex_get_slot_values(last_names):
    params = {
        'name': "LastName",
        'version': "$LATEST"
    }
    data = lex_model.get_slot_type(**params)
    checksum = data['checksum']
    print(data)
    lex_update_slot_values(last_names,checksum)
    

def lex_update_slot_values(last_names, value):
    print(last_names)
    params = {
        'name': "LastName",
        'description': "Available last names",
        'enumerationValues': last_names,
        'createVersion': True
    }
    
    if(value is not None):
        params["checksum"] = value
    
    data = lex_model.put_slot_type(**params)
    print("--------response from lex---------")
    print(data)

def removeDuplicates(data):
    unique_last_names = []
    # adding unique values to the new list  
    for value in data:
        if value not in unique_last_names:
            unique_last_names.append(value)
    
    return unique_last_names
        

    
    
    



