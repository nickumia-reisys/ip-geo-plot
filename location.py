import geopandas
import matplotlib.pyplot as plt
import pandas as pd
import pandas_bokeh
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
    pandas_bokeh.output_notebook()
    us = geopandas.read_file("./zip_map/cb_2018_us_zcta510_500k.shp")

    # Plot Zip Code Frequencies
    df=pd.DataFrame({'PCODE': list(g.postal_code.keys()), 'A':list(g.postal_code.values()) })

    # Join Zip Code Plot to US Plot
    new_df=us.join(df.set_index('PCODE'), on='ZCTA5CE10')


    new_df.plot_bokeh(simplify_shapes=20000,
                      category="A",
                      colormap="Spectral",
                      hovertool_columns=["ZCTA5CE10","A"])

