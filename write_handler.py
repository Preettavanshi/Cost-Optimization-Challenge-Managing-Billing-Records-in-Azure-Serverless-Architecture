# Simple Cosmos DB insert

from azure.cosmos import CosmosClient

def write_billing_record(record):
    cosmos_url = "<COSMOS_DB_ENDPOINT>"
    cosmos_key = "<COSMOS_DB_KEY>"
    database_name = "BillingDB"
    container_name = "BillingRecords"
    client = CosmosClient(cosmos_url, credential=cosmos_key)
    container = client.get_database_client(database_name).get_container_client(container_name)
    container.upsert_item(record)
