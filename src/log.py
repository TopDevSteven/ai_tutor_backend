import logging
import os

import json_log_formatter


def init_logging():
    # Configure the global logger
    log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
    handler = logging.StreamHandler()
    logging.basicConfig(level=log_level, handlers=[handler])

    if os.getenv("DATADOG_LOGGING") == "true":
        formatter = json_log_formatter.VerboseJSONFormatter()
        handler.setFormatter(formatter)
        logging.info("Using JSON log formatter")

    logging.info(f"Log level set to {logging.getLevelName(log_level)}")
