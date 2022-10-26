import pickle
import sys

from ipwhois import IPWhois
from ipwhois.exceptions import HTTPLookupError, IPDefinedError
import pycountry

from ip import lookup_ips
from data import g
from location import tally_countries



def iterate_input(input_file, work_todo, starting_no=0):
    with open(input_file, 'r') as input_t:
        ips = input_t.read()

    ips_individual = ips.split('\n')[0:-1]
    ip_count = len(ips_individual)

    for i, ip in enumerate(ips_individual):
        print('Working on %d out of %d: %s' % (i, ip_count, ip))
        if i >= starting_no:
            work_todo(ip)


if __name__ == "__main__":
    g.load_data()

    if sys.argv[1] == 'lookup':
        iterate_input('ips', lookup_ips)
        g.save_data()
    if sys.argv[1] == 'tally':
        iterate_input('ips_working', tally_countries)
        print(g.country_dict)
        print(g.postal_code)
    if sys.argv[1] == 'print':
        print(len(g.bad_ips), g.bad_ips)
        print(g.ip_objs.keys())