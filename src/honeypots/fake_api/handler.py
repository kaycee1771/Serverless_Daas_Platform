import os
import json
import logging
from logger.log_handler import log_decoy_trigger

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Incoming request: %s", json.dumps(event))

    # Pull fake decoy values
    fake_api_key = os.getenv("FAKE_API_KEY", "none")
    fake_url = os.getenv("FAKE_INTERNAL_URL", "none")

    # Log the trigger (e.g., someone accessed this trap endpoint)
    log_decoy_trigger(event, decoy_type="http_honeypot", description="Fake API endpoint accessed")

    # Return the fake values (helps attackers interact more)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "This is a fake service endpoint.",
            "fake_api_key": fake_api_key,
            "fake_internal_url": fake_url
        })
    }
