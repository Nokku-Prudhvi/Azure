import json
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import base64


def prepare_item(cidr):
    accountAlias="unknown"
    region = "unknown"
    stage="unknown"
    occupied="No"
    component="unknown"
    service = "unknown"
    owner="unknown"
    AssignedBy="unknown"
    manual_script="script"
    
    data=accountAlias+region+stage+component+service+owner+cidr
    # base-64 enconding
    encodedBytes=base64.b64encode(data.encode("utf-8"))
    encodedstr= str(encodedBytes,"utf-8")
    id=str(encodedstr)
    
    item={
        "id":id,
        "accountAlias":accountAlias,
        "region" : region,
        "stage" : stage,
        "occupied" : occupied,
        "component" : component,
        "service" : service,
        "owner": owner,
        "AssignedBy" : AssignedBy,
        "manual_script" : manual_script
    }
    return item
    
    
def lambda_handler(event, context):
    # Initialize the Cosmos client
    endpoint = "https://<db-name>.documents.azure.com:443/"
    key = '<primary-key>'
    
    # <create_cosmos_client>
    client = CosmosClient(endpoint, key)
    # </create_cosmos_client>
    
    # Create a database
    # <create_database_if_not_exists>
    database_name = 'firstCosmosDatabase'
    database = client.create_database_if_not_exists(id=database_name)
    # </create_database_if_not_exists>
    
    # Create a container
    # Using a good partition key improves the performance of database operations.
    # <create_container_if_not_exists>
    container_name = 'firstCosmosContainer4'
    container = database.create_container_if_not_exists(
        id=container_name, 
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    # </create_container_if_not_exists>

    # Add items to the container
    items_to_create_list=[]
    m=0
    count=0
    while(m<7):
        n=0
        while(n<256):
            #print(f'10.{m}.{n}.0/20')
            n+=16
            count+=1
            items_to_create_list.append(prepare_item(f'10.{m}.{n}.0/20'))
        m+=1
        
    print(count)
     # <create_item>
    for each_item in items_to_create_list:
        print(each_item)
        container.create_item(body=each_item)
    # </create_item>

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
