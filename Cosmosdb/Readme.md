## Imp points to note:

- Resource group with same name in same region is not possible
- You can create multiple databases in one account
- Account sticks with one kind of api
- Container is nothing but a table 
- Databases contains many containers(tables)

### Sample basic python cosmosdb example :
- https://docs.microsoft.com/en-us/azure/cosmos-db/create-sql-api-python
- https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-python-samples

### Python code for basic actions on cosmosdb
https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/cosmos/azure-cosmos/samples/document_management.py#L81-L88


## Triggering Azure SDK from Lamnda-AWS
- We can use aws-layers to upload the azude-sdk-cosmos library and utilize in the lambda-code
-  below command installs libraries required for wirking with cosmos-db-sdk-python in the current folder
    pip3 install --pre azure-cosmos -t  .
- folder structure need to be maitained to use in the lambda-layer as : "python/lib/python3.8/site-packages/<your-libraries>"
    
Note:
The folder is upload to this git-repo for your reference

