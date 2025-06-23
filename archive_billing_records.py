# Azure Durable Function to archive old billing records from Cosmos DB to Blob Storage
import datetime
import azure.functions as func
import logging
import json
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient, exceptions

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f"Archival function started at {utc_timestamp}")

    # Cosmos DB setup
    cosmos_url = "<COSMOS_DB_ENDPOINT>"
    cosmos_key = "<COSMOS_DB_KEY>"
    database_name = "BillingDB"
    container_name = "BillingRecords"
    client = CosmosClient(cosmos_url, credential=cosmos_key)
    container = client.get_database_client(database_name).get_container_client(container_name)

    # Blob setup
    blob_service_client = BlobServiceClient.from_connection_string("<BLOB_STORAGE_CONN_STRING>")
    blob_container = blob_service_client.get_container_client("billing-archive")

    cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=90)

    query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff_date.isoformat()}'"
    records = list(container.query_items(query=query, enable_cross_partition_query=True))

    for record in records:
        record_id = record["id"]
        record_date = datetime.datetime.fromisoformat(record["timestamp"])
        folder_path = f"{record_date.year}/{record_date.month:02}/{record_date.day:02}"
        blob_name = f"{folder_path}/{record_id}.json"

        blob_client = blob_container.get_blob_client(blob_name)
        blob_client.upload_blob(json.dumps(record), overwrite=True)
        container.delete_item(record, partition_key=record["partitionKey"])

    logging.info(f"Archived {len(records)} records to blob storage")
