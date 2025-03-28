import requests
import importlib
import os
from ddns.logging import getLoggerAdapter

logger = getLoggerAdapter('utils')

def get_public_ip():
    try:
        # TODO - Make this replacable from ENV
        return requests.get("https://api.ipify.org").text.strip()
    except Exception as e:
        logger.error(f"Could not get public IP: {e}")
        return None

def load_provider():
    provider_name = os.getenv("DDNS_PROVIDER")
    if not provider_name:
        logger.error("DDNS_PROVIDER environment variable is not set.")
        return None

    try:
        module = importlib.import_module(f"ddns.providers.{provider_name.lower()}")
        class_name = "".join([part.capitalize() for part in provider_name.split("_")]) + "Provider"
        provider_class = getattr(module, class_name)
        return provider_class()
    except (ModuleNotFoundError, AttributeError) as e:
        logger.error(f'Failed to load provider "{provider_name}": {e}')
        return None
