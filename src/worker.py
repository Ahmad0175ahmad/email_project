import time
from azure.identity import DefaultAzureCredential # cite: 4.2
from azure.storage.queue import QueueClient # cite: 341

class EmailWorker:
    def __init__(self, queue_url, clustering_engine, intent_engine, logger):
        self.queue_client = QueueClient.from_queue_url(queue_url, credential=DefaultAzureCredential())
        self.clustering = clustering_engine
        self.intent_engine = intent_engine
        self.logger = logger

    def run(self):
        while True:
            # Poll with 5-minute lock (Cite: 390)
            messages = self.queue_client.receive_messages(visibility_timeout=300)
            
            for msg in messages:
                # Track Correlation ID (Cite: 383, 384)
                correlation_id = msg.id
                self.logger.info(f"Processing message", extra={"custom_dimensions": {"correlation_id": correlation_id}})
                
                try:
                    self.process_email(msg, correlation_id)
                    self.queue_client.delete_message(msg)
                except Exception as e:
                    self.logger.error(f"Failed to process: {str(e)}")
            
            time.sleep(10) # Wait 10s if queue is empty