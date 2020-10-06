import json
import os
import boto3

lex_model = boto3.client('lex-models')

# ddb = boto3.client('dynamodb')

dynamodb = boto3.resource('dynamodb')


def first_name(event, context):
    table = dynamodb.Table('names_test')
    data = scanData(table) #data = list
    first_values = []
    unique_first = removeDuplicates(data)
    obj = {}
    unique_first_names = []
    for i in unique_first:
        # unique_first_names.append(i.replace("first_name", "value"))
        i["value"] = i["first_name"]
        del(i["first_name"])
        unique_first_names.append(i)
    # print(unique_first_names)

    get_values = lex_get_slot_values(unique_first)
    # latest_slot = lex_model.create_slot_type_version(name = 'FirstNames')
    latest_intent = lex_model.create_intent_version(name = 'BookField')
    latest_bot = lex_model.create_bot_version(name = 'names_test')
    # print(latest_slot)
    return latest_bot

def scanData(table):
    scan_kwargs = {
        'ProjectionExpression': "first_name",
    }
    response = table.scan(**scan_kwargs)
    data = response['Items']
    return data
    
def lex_get_slot_values(first_names):
    params = {
        'name': "FirstNames",
        'version': "$LATEST"
    }
    data = lex_model.get_slot_type(**params)
    checksum = data['checksum']
    print(data)
    lex_update_slot_values(first_names,checksum)
    

def lex_update_slot_values(first_names, value):
    print(first_names)
    params = {
        'name': "FirstNames",
        'description': "Available first names",
        'enumerationValues': first_names,
        'createVersion': True
    }
    
    if(value is not None):
        params["checksum"] = value
    
    data = lex_model.put_slot_type(**params)
    print("--------response from lex---------")
    print(data)

def removeDuplicates(data):
    unique_first_names = []
    # adding unique values to the new list  
    for value in data:
        if value not in unique_first_names:
            unique_first_names.append(value)
    
    return unique_first_names
        

    
    
    



