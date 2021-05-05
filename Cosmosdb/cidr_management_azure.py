import json
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import base64
from ipaddress import IPv4Network

#{
#        "accountAlias":"MyAccountName",
#        "region" : "US",
#        "stage" : "dev",
#        "component" : "component",
#        "service" : "service",
#        "owner": "Nokku",
#        "AssignedBy" : "NokkuPrudhvi"
#}


def lambda_handler(event, context):
        
    accountAlias=event["accountAlias"]
    region = event["region"]
    stage=event["stage"]
    component=event["component"]
    service = event["service"]
    owner=event["owner"]
    AssignedBy=event["AssignedBy"]
    
    # Initialize the Cosmos client
    endpoint = "https://<db-account-name>.documents.azure.com:443/"
    key = '<primary-key>'
    
    # <create_cosmos_client>
    client = CosmosClient(endpoint, key)
    # </create_cosmos_client>
    

    database_name = 'firstCosmosDatabase'
    database = client.get_database_client(database_name)
    container_name = 'firstCosmosContainer4'
    container = database.get_container_client(container_name)
    item_list = list(container.read_all_items())

    print('Found {0} items'.format(item_list.__len__()))
    
    unsorted_ip_addr_list=[]
    allinfo_occupied_yes=[]
    allinfo_occupied_no_dict={}
    for doc in item_list:
        print(doc)
        #print('Item Id: {0}'.format(doc.get('id')))
        if doc["occupied"]=="No":
            unsorted_ip_addr_list.append(IPv4Network(doc["cidr"]))
            allinfo_occupied_no_dict[doc["cidr"]] = doc
        elif doc["occupied"]=="Yes":
            allinfo_occupied_yes.append(doc)
    print(unsorted_ip_addr_list)
    sorted_ip_addr_list=unsorted_ip_addr_list
    sorted_ip_addr_list.sort()
    print(sorted_ip_addr_list)
    
    for i in sorted_ip_addr_list:
        overlapFlag=False
        to_be_deleted_item=""
        for j in allinfo_occupied_yes:
            if( i.overlaps(IPv4Network(j['cidr']))  and component!="Not Managed"):
                overlapFlag=True
                to_be_deleted_item=j
                break
        if overlapFlag==True:
            print(f"deleting entry from db-{str(i)} as it is overlapping with item occupied==yes")
            response = container.delete_item(item=to_be_deleted_item["id"], partition_key=to_be_deleted_item["id"])
            print('Deleted item\'s Id is {0}'.format(to_be_deleted_item["id"]))
            
        elif overlapFlag==False:
            free_cidr=str(i)
            print(f"Free cidr is {str(i)}")
            print(allinfo_occupied_no_dict)
            print(allinfo_occupied_no_dict[free_cidr])
            free_cidr_complete_item=allinfo_occupied_no_dict[free_cidr]
            response = container.delete_item(item=free_cidr_complete_item["id"], partition_key=free_cidr_complete_item["id"])
            print(response)
            print('Deleted item\'s Id is {0}'.format(free_cidr_complete_item["id"]))
            data=accountAlias+region+stage+component+service+owner+free_cidr
            # base-64 enconding
            encodedBytes=base64.b64encode(data.encode("utf-8"))
            encodedstr= str(encodedBytes,"utf-8")
            id=str(encodedstr)
            
            item={
                "id":id,
                "accountAlias":accountAlias,
                "region" : region,
                "stage" : stage,
                "occupied" : "Yes",
                "component" : component,
                "service" : service,
                "owner": owner,
                "AssignedBy" : AssignedBy,
                "manual_script" : "Manual",
                "cidr":free_cidr
            }
            container.create_item(body=item)
            break

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
