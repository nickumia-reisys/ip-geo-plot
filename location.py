import pycountry
from data import g


def tally_countries(ip):
    country = pycountry.countries.get(alpha_2=g.ip_objs[ip]['data']['asn_country_code']).name
    pc = g.ip_objs[ip]['data']['nets'][0]['postal_code']

    if country in g.country_dict.keys():
        g.country_dict[country] += 1
    else:
        g.country_dict[country] = 1

    if country == 'United States':
        if pc in g.postal_code.keys():
            g.postal_code[pc] += 1
        else:
            g.postal_code[pc] = 1


def plot_postal_codes():
    pass
