import abc

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
