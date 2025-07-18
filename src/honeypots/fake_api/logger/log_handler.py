import json
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def log_decoy_trigger(event, decoy_type="env_variable", description=None):
    log_entry = {
        "event_type": "deception_trigger",
        "timestamp": datetime.utcnow().isoformat(),
        "decoy_type": decoy_type,
        "description": description or "Decoy interaction detected",
        "request_metadata": {
            "headers": event.get("headers", {}),
            "source_ip": event.get("requestContext", {}).get("identity", {}).get("sourceIp", "unknown"),
            "user_agent": event.get("headers", {}).get("User-Agent", "unknown")
        }
    }

    logger.info("[DAAS_LOG] %s", json.dumps(log_entry))
