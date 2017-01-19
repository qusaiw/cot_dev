#!/usr/bin/env python
# Written by Qusai Abu-Obaida

import re

DEV_CATCH = re.compile(r'([a-z]\d\d_)?([a-z0-9]+)(_.+)?(_\dp?\d*)')
COT_CATCH = re.compile(r'([A-Z]+[0-9]+_)([A-Z0-9]+)(_[A-Z0-9]+)?(_\dP?\d*)')
SPECIAL_COT_CATCH = re.compile(r'([A-Z]+[0-9]+_)([A-Z]+)()(\d)*')
my_list = []
final = {}


def extract(group):
    """This function extracts the 4 groups from the regex search, the regex terms are all made to return the same
        groups in the same order, when provided a regex object, return prefix, family, infix and drive for any cell
    """
    pre = group.group(1).strip('_') if group.group(1) else None
    family = group.group(2).strip('_') if group.group(2) else None
    infix = group.group(3).strip('_') if group.group(3) else None
    drive = group.group(4).strip('_') if group.group(4) else None
    return pre, family, infix, drive


def main():
    with open('list.txt') as f:
        for line in f:
            # Extracts the dev and cot names from a list, assumes the names are separated by ":"
            my_list.append([line[:-1].split(':')[0], line[:-1].split(':')[1]])
    for item in my_list:
        dev_name = item[0]
        cot_name = item[1]
        if dev_name.lower() != dev_name:
            print "%s has lowercase letter. skipping cell"
            continue
        if cot_name.upper() != cot_name:
            print "%s has lowercase letters, skipping cell" % cot_name
            continue
        my_search = DEV_CATCH.search(dev_name)
        if not my_search:
            print "%s: unmatched name" % cot_name
            continue
        # dev_specs is a tuple -> (prefix, family, infix, drive)
        dev_specs = extract(my_search)
        my_search = COT_CATCH.search(cot_name)
        if not my_search:
            my_search = SPECIAL_COT_CATCH.search(cot_name)
        if not my_search:
            print "%s unmatched name" % dev_name
            continue
        # cot_specs is a tuple -> (prefix, family, infix, drive)
        cot_specs = extract(my_search)
        # "final" is a dictionary with [dev_name, cot_name] as keys and [dev_specs, cot_specs] as values
        final[str(item)] = [dev_specs, cot_specs]

if __name__ == '__main__':
    main()
print final
