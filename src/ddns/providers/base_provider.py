import abc
import os

class DDNSProvider(abc.ABC):
    def __init__(self):
        self.zone_name = None
        self.record_name = None

    @abc.abstractmethod
    def get_zone_id(self):
        pass

    @abc.abstractmethod
    def get_record_id(self, zone_id: str):
        pass

    @abc.abstractmethod
    def update_dns_record(self, zone_id: str, record_id: str, ip: str):
        pass

    def getTTL(self) -> int:
        ttl = int(os.getenv('TTL', '120'))
        if not ttl or ttl < 1:
            raise ValueError(f'TTL "{ttl}" is invalid. It must be >=1')
        return ttl
