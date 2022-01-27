from requests import Session
from loguru import logger


def get_session() -> Session:
    """Returns a Session() preconfigured with headers and set-cookies for Juniper online MIB tools."""
    headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}

    # Setup session
    session = Session()
    session.headers.update(headers)

    # We need to access a valid page to get set-cookies. Here we use compare.jsp
    logger.info("Fetching set-cookies")
    session.get("https://apps.juniper.net/mib-explorer/compare.jsp")

    return session
