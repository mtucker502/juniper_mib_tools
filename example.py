from juniper_mib_tools.session import get_session
from juniper_mib_tools.diff import get_mib_diff
from juniper_mib_tools.oid import get_oids_detail, parse_xml
from juniper_mib_tools.tools import csv_writer


old_release = "21.3R1"
new_release = "21.4R1"

session = get_session()
oid_diff = get_mib_diff(
    old_release=old_release, new_release=new_release, session=session
)
oid_detail = get_oids_detail(oid_diff, release=new_release, session=session)
oid_final = parse_xml(oid_detail)

csv_writer(oid_final, f"mib_diff_junos_{old_release}_to_{new_release}.csv")
