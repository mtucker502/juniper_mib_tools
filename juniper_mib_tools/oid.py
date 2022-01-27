from requests import Session
from tqdm import tqdm
from typing import List
from loguru import logger
from lxml import etree
from io import StringIO
from copy import deepcopy
from time import perf_counter


def get_oid_detail(
    oid: dict,
    release: str = None,
    session: Session = None,
    product: str = "Junos+OS",
    info_url: str = "https://apps.juniper.net/mib-explorer/getObjectDetails.html",
) -> dict:
    """Retrieves detailed information about a specific OID"""

    body = f"product={product}&release={release}"
    logger.debug(body + f"&objectName={oid.get('name')}")
    r = session.post(info_url, data=body + f"&objectName={oid.get('name')}")
    return r.json()[0]


def get_oids_detail(
    oids: List[dict],
    release: str = None,
    session: Session = None,
    product: str = "Junos+OS",
    info_url: str = "https://apps.juniper.net/mib-explorer/getObjectDetails.html",
    disable_progress: bool = False,
) -> dict:
    """Helper function for looping through many oids"""
    ...
    start = perf_counter()
    oids_copy = deepcopy(oids)
    # Fix logging for tqdm
    if not disable_progress:
        logger.remove()
        logger.add(lambda msg: tqdm.write(msg, end=""))

    logger.info(f"Fetching details for {len(oids_copy)} oid(s)")
    for oid in tqdm(oids_copy, disable=disable_progress):
        oid.update(
            get_oid_detail(
                oid,
                release=release,
                session=session,
                product=product,
                info_url=info_url,
            )
        )

    logger.info(f"Fetch completed in {perf_counter() - start} seconds.")

    return oids_copy


def parse_xml(oids: dict) -> dict:
    """The Juniper MIB API returns fancy XML nested within JSON. It's ugly. This fixes that"""
    oids_copy = deepcopy(oids)
    parser = etree.HTMLParser()
    logger.debug("Converting nested XML to JSON")
    for idx, oid in enumerate(oids_copy):
        # clean up the HTML and convert to dictionary
        html = oid.pop("fileName")
        if html:
            tree = etree.parse(StringIO(html), parser)
            try:
                rows = tree.findall('.//div[@class="row"]')
                for row in rows:
                    field = row.find('div[@class="field"]').text
                    value = row.find('div[@class="value"]').text
                    oid[field] = value
            except etree.XMLSyntaxError as err:
                logger.error(f"HTML parsing error in oids[{idx}]: {oid['name']}")
                logger.error(err)

        # remove the nested mibObjectUniqueInfo dictionary and add to oid dict
        unique_info = oid.pop("mibObjectUniqueInfo")
        oid.update(**unique_info)

    return oids_copy
