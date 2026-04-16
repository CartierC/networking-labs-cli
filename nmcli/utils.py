import logging
import socket

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def validate_host(host: str) -> bool:
    try:
        socket.gethostbyname(host)
        return True
    except socket.gaierror:
        logger.error(f"Cannot resolve host: {host}")
        return False
