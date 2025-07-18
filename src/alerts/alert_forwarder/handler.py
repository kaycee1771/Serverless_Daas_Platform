import gzip
import base64
import json
import logging

from classifier import classify_intent

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Decode and decompress the CloudWatch Logs data
        cw_data = base64.b64decode(event['awslogs']['data'])
        decompressed = gzip.decompress(cw_data).decode('utf-8')
        log_data = json.loads(decompressed)

        for log_event in log_data.get("logEvents", []):
            message = log_event.get("message", "")

            # Filter for deception triggers
            if "[DAAS_LOG]" in message:
                try:
                    log_json = json.loads(message.replace("[DAAS_LOG] ", ""))

                    # Predict attacker intent using ML
                    intent = classify_intent(log_json)

                    # Structure the alert
                    alert = {
                        "alert_type": "deception_trigger",
                        "intent": intent,
                        "decoy_type": log_json.get("decoy_type", "unknown"),
                        "timestamp": log_json.get("timestamp"),
                        "source_ip": log_json.get("request_metadata", {}).get("source_ip"),
                        "user_agent": log_json.get("request_metadata", {}).get("user_agent"),
                        "description": log_json.get("description", "unknown")
                    }

                    logger.info("[ALERT] %s", json.dumps(alert))

                except Exception as e:
                    logger.warning("Failed to process DAAS_LOG entry: %s", e)

    except Exception as outer_error:
        logger.error("Failed to process log event: %s", outer_error)
