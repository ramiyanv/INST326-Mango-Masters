import re
import sys

def parse_address(line):
    """
    Takes one line of text that looks like:
    "That’s Amore Grill: 15201 Shady Grove Rd, Rockville MD 20850"
    Returns a dictionary with the parts of the address, or None if it doesn't match.
    """
    line = line.strip()
    if not line:
        return None

    pattern = r'^(?P<restaurant>[^:]+):\s*(?P<house_number>\d+)\s+(?P<street>[^,]+),\s*(?P<city>[A-Za-z\s]+)\s+(?P<state>[A-Z]{2})\s+(?P<zip>\d{5})$'

    m = re.search(pattern, line)
    if m is None:
        return None

    result = {
        "restaurant": m.group("restaurant").strip(),
        "house_number": m.group("house_number"),
        "street": m.group("street").strip(),
        "city": m.group("city").strip(),
        "state": m.group("state"),
        "zip": m.group("zip")
    }
    return result


def parse_addresses(path):
   
    results = []
    f = None
    try:
        f = open(path, "r", encoding="utf-8")
        for line in f:
            line = line.strip()
            if line == "":
                continue
            item = parse_address(line)
            results.append(item)
    finally:
        if f is not None:
            f.close()
    return results

