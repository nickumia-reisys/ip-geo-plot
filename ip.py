from ipwhois import IPWhois
from ipwhois.exceptions import HTTPLookupError, IPDefinedError
from data import g


def lookup_ips(ip):
    if ip not in g.ip_objs.keys() and ip not in g.bad_ips:
        try:
            g.ip_objs[ip] = {}
            g.ip_objs[ip]['obj'] = IPWhois(ip)
            g.ip_objs[ip]['data'] = g.ip_objs[ip]['obj'].lookup_whois()
        except (HTTPLookupError, IPDefinedError):
            g.bad_ips.append(ip)
