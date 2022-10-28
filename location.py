import geopandas
import matplotlib.pyplot as plt
import pandas as pd
import pandas_bokeh
import pycountry

from data import g
from states import abbrev_to_us_state

from shapely.errors import ShapelyDeprecationWarning
import warnings
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)


def tally_countries(ip):
    if ip not in g.bad_ips:
        try:
            country = pycountry.countries.get(alpha_2=g.ip_objs[ip]['data']['asn_country_code']).name
            pc = g.ip_objs[ip]['data']['nets'][0]['postal_code']
            state = abbrev_to_us_state[g.ip_objs[ip]['data']['nets'][0]['state']]

            if country in g.country_dict.keys():
                g.country_dict[country] += 1
            else:
                g.country_dict[country] = 1

            if country == 'United States':
                # Tally Zip Codes
                if pc in g.postal_code.keys():
                    g.postal_code[pc] += 1
                else:
                    g.postal_code[pc] = 1
                # Tally States
                if state in g.states.keys():
                    g.states[state] += 1
                else:
                    g.states[state] = 1
        except KeyError:
            pass


def plot_location(map_type='state'):
    pandas_bokeh.output_notebook()

    if map_type == 'state':
        us = geopandas.read_file("./state_map/cb_2018_us_state_5m.shp")

        # Ignore extremely high frequency states
        # g.states['Washington'] = 0
        # g.states['California'] = 0
        # g.states['North Carolina'] = 0

        # Relative to the highest frequency state
        sf = {}
        highest = max(g.states.values())
        for state in g.states:
            sf[state] = g.states[state]/highest

        # Plot State Frequencies
        df=pd.DataFrame({'PCODE': list(sf.keys()), 'A':list(sf.values()) })
        # Join State Plot to US Plot
        new_df=us.join(df.set_index('PCODE'), on='NAME')

        new_df.plot_bokeh(simplify_shapes=20000,
                          category="A",
                          colormap="Viridis",
                          # marker="inverted_triangle",
                          hovertool_columns=["NAME","A"])

    elif map_type == 'zip':
        us = geopandas.read_file("./zip_map/cb_2018_us_zcta510_500k.shp")
        # Set all other Zip Codes to 0
        import uszipcode
        all_codes = [i.zipcode for i in uszipcode.SearchEngine().by_pattern('', returns=1000000)]
        for i, code in enumerate(all_codes):
            if code not in g.postal_code:
                g.postal_code[code] = 0

        # Plot Zip Code Frequencies
        df=pd.DataFrame({'PCODE': list(g.postal_code.keys()), 'A':list(g.postal_code.values()) })
        # Join Zip Code Plot to US Plot
        new_df=us.join(df.set_index('PCODE'), on='ZCTA5CE10')

        new_df.plot_bokeh(simplify_shapes=20000,
                          category="A",
                          colormap="Inferno",
                          # marker="inverted_triangle",
                          hovertool_columns=["ZCTA5CE10","A"])
