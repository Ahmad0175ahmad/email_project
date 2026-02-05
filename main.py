import os
import signal
import time
import logging
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()  # This specifically tells Python to read your .env file
# Import your custom modules from Phase 1
from src.worker import EmailWorker
from src.model_logic import EmailClustering
from src.intent_classifier import IntentClassifierL3
from version import VERSION

# 1. SETUP LOGGING & OBSERVABILITY (Cite: 382, 384)
# This sends all your logs directly to Application Insights
configure_azure_monitor()
logger = logging.getLogger("email_project")

def handle_shutdown(signum, frame):
    """Graceful Shutdown: Catches SIGTERM from Azure (Cite: 393, 394)"""
    logger.info(f"Received signal {signum}. Completing current task before exit...")
    # Set a flag or stop the worker loop safely
    os._exit(0)

signal.signal(signal.SIGTERM, handle_shutdown)

def main():
    logger.info(f"Starting Email Categorization Model {VERSION}")

    # 2. INITIALIZE GLOBAL RESOURCES ONCE (Cite: 396, 407)
    # These stay in memory for high performance
    credential = DefaultAzureCredential()
    
    # Azure OpenAI Client (Key is pulled from Key Vault/App Settings)
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-15-preview"
    )

    # Load AI Logic
    clustering = EmailClustering(client)
    classifier = IntentClassifierL3(client)

    # 3. START THE WORKER (Cite: 371, 388)
    # This loop runs forever polling the queue
    worker = EmailWorker(
        queue_url=os.getenv("QUEUE_URL"),
        clustering_engine=clustering,
        intent_engine=classifier,
        logger=logger
    )

    worker.run()

if __name__ == "__main__":
    main()