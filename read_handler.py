# Read API logic to retrieve records, fallback to Blob if not found in Cosmos

import json
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient, exceptions

def read_billing_record(record_id):
    cosmos_url = "<COSMOS_DB_ENDPOINT>"
    cosmos_key = "<COSMOS_DB_KEY>"
    database_name = "BillingDB"
    container_name = "BillingRecords"
    client = CosmosClient(cosmos_url, credential=cosmos_key)
    container = client.get_database_client(database_name).get_container_client(container_name)

    try:
        record = container.read_item(item=record_id, partition_key=record_id)
        return record
    except exceptions.CosmosResourceNotFoundError:
        blob_service_client = BlobServiceClient.from_connection_string("<BLOB_STORAGE_CONN_STRING>")
        container_client = blob_service_client.get_container_client("billing-archive")
        for y in range(2020, datetime.datetime.now().year + 1):
            for m in range(1, 13):
                try:
                    blob_path = f"{y}/{m:02}/{record_id}.json"
                    blob_client = container_client.get_blob_client(blob_path)
                    return json.loads(blob_client.download_blob().readall())
                except:
                    continue
        raise Exception("Record not found")
