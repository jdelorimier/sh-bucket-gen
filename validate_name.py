import re

name = 'c4ads-sh-china-trade-data'

def assert_no_spaces(name):
    test = re.findall(r' ',name)
    return len(test) == 0

def assert_all_lower_case(name):
    test = re.findall(r'[A-Z]',name)
    return len(test) == 0

def assert_prefix(name):
    test = re.findall(r'^c4ads-sh-', name)
    return len(test) == 1

