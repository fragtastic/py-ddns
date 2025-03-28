import os
import requests
from ddns.providers.base_provider import DDNSProvider
from ddns.logging import getLoggerAdapter

logger = getLoggerAdapter('Cloudflare')

class CloudflareProvider(DDNSProvider):
    def __init__(self):
        super().__init__()
        self.api_token = os.getenv("CF_API_TOKEN")
        self.zone_name = os.getenv("CF_ZONE_NAME")
        self.record_name = os.getenv("CF_RECORD_NAME")
        # TODO - abstract to par
        self.ttl = self.getTTL()
        if not self.ttl or self.ttl < 1:
            raise ValueError(f'TTL "{self.ttl}" is invalid. It must be >=1')

        if not all([self.api_token, self.zone_name, self.record_name]):
            raise ValueError("Missing required environment variables: CF_API_TOKEN, CF_ZONE_NAME, CF_RECORD_NAME")

        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def get_zone_id(self):
        url = f"https://api.cloudflare.com/client/v4/zones?name={self.zone_name}"
        response = requests.get(url, headers=self.headers)
        result = response.json()
        if result.get("success") and result["result"]:
            return result["result"][0]["id"]
        logger.error(f"Failed to get zone ID: {result}")
        return None

    def get_record_id(self, zone_id: str):
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={self.record_name}"
        response = requests.get(url, headers=self.headers)
        result = response.json()
        if result.get("success") and result["result"]:
            return result["result"][0]["id"]
        logger.error(f"DNS record not found: {result}")
        return None

    def update_dns_record(self, zone_id: str, record_id: str, ip: str):
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        data = {
            "type": "A",
            "name": self.record_name,
            "content": ip,
            "ttl": self.ttl,
            "proxied": False
        }
        response = requests.put(url, headers=self.headers, json=data)
        result = response.json()
        if result.get("success"):
            logger.info(f"Updated {self.record_name} → {ip}")
        else:
            logger.error(f"Failed to update record: {result}")
