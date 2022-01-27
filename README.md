# Juniper MIB Tools

A collection of tools (one for now) for analysing Juniper MIBs

## Installing

```bash
git clone https://github.com/mtucker502/juniper_mib_tools.git
cd juniper_mib_tools
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## MIB Diffs

### Background

Doing a diff between two Junos versions is not easy. This is especially true when doing a diff between releases with large differences in release dates. Juniper provides a very useful tool [MIB Explorer](https://apps.juniper.net/mib-explorer/) but it requires you to 1) Scroll-to-load to retrieve the entire OID list and 2) To click on each OID to get more detail about the OID.

### How to use

- `example.py` has been included to show how to use this tool in your own scripts or automations
- A CLI tool has been provided which creates a CSV of the mib diff for further analysis

CLI Usage:

```bash
python snmp_mib_diff.py 21.3R1 21.4R1
```
