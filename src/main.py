import os
import time
from ddns.utils import get_public_ip, load_provider
from ddns.logging import getLoggerAdapter

logger = getLoggerAdapter('Main')


def main():
    logger.info(f"Running git commit: {os.getenv('GIT_COMMIT_SHA', 'UNKNOWN')}")

    interval = int(os.getenv('UPDATE_INTERVAL_MINUTES', '10'))
    if not interval or interval < 1:
        logger.critical(f'Interval "{interval}" is invalid. It must be >=1')
        return
    ddns = load_provider()
    if not ddns:
        return

    # TODO - move all this into ddns instead. Should be straightforward as ddns.update()
    zone_id = ddns.get_zone_id()
    if not zone_id:
        return

    record_id = ddns.get_record_id(zone_id)
    if not record_id:
        return

    last_ip = None
    logger.info(f"Running DDNS check every {interval} minute(s)")

    while True:
        current_ip = get_public_ip()
        logger.debug(f"Got public IP: {current_ip}")
        if current_ip and current_ip != last_ip:
            ddns.update_dns_record(zone_id, record_id, current_ip)
            last_ip = current_ip
            logger.info(f"IP updated: {current_ip}")
        else:
            logger.debug(f"IP unchanged: {current_ip}")
        time.sleep(interval * 60)


if __name__ == "__main__":
    main()
