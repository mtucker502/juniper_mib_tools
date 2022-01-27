from requests import Session
from loguru import logger
import json
from time import perf_counter


def get_mib_diff(
    old_release: str = None,
    new_release: str = None,
    session: Session = None,
    product: str = "Junos+OS",
    compare_url: str = "https://apps.juniper.net/mib-explorer/compareReleases.html",
):
    start = perf_counter()
    # releases1/2 must match what's available on mib-explorer
    release1 = new_release
    release2 = old_release

    # Enumerate paged responses
    page = 0
    body = f"product={product}&release1={release1}&release2={release2}&withDesc=true"
    oids = []
    while True:
        logger.info(body + f"&pgNo={page}")
        r = session.post(compare_url, data=body + f"&pgNo={page}")
        if r.status_code == 200:
            diff = json.loads(r.text)  # TODO: why didn't we use r.json()?
            if len(diff["list"]) > 0:
                oids += diff["list"]
                page += 1
            else:
                logger.info("Last page!")
                break

        else:
            logger.info("Last page!")
            break

    logger.info(f"Found {len(oids)} OIDs different between {release1} and {release2}.")
    logger.info(f"Fetch completed in {perf_counter() - start} seconds.")

    return oids


# write data out for use with parse_xml.py

# with open("data.json", "w") as fh:
# fh.write(json.dumps(oids))

# new_traps = [oid for oid in oids if "TRAP" in oid['fileName']]
# with open("new_traps.txt", "w") as fh:
#     fh.write(json.dumps(new_traps))
