import json
from azure.storage.blob import BlobClient # cite: 4.1

def atomic_write_to_blob(account_url, container, filename, data, correlation_id):
    # Log the correlation ID for observability
    print(f"[{correlation_id}] Writing output to {filename}")
    
    blob_client = BlobClient(
        account_url=account_url, 
        container_name=container, 
        blob_name=filename, 
        credential=DefaultAzureCredential()
    )
    
    # Generate full JSON in memory and upload in one action
    json_content = json.dumps(data)
    blob_client.upload_blob(json_content, overwrite=True)