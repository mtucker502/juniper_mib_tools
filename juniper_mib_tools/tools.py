import csv
from loguru import logger
from pathlib import Path


def csv_writer(oids, csv_file: Path = "diff.csv"):
    """Takes the list of OIDS, creates keys, then writes the data as a CSV"""

    # Generate keys
    keys = set().union(*(d.keys() for d in oids))
    logger.debug(f"Found keys: {keys}")

    # Write CSV
    logger.debug(f"Writing CSV to {csv_file}")
    with open(csv_file, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(oids)
    logger.debug(f"Wrote CSV data to {csv_file}")
