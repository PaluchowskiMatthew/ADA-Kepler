import numpy as np
import pandas as pd
from urllib.parse import urlencode
from pprint import *
import requests
from collections import defaultdict


USERNAME = 'user1'
URL = r'http://api.geonames.org/searchJSON?'

# Get the cantons data
canton_cols = ['Code', 'Canton']
cantons = pd.read_csv(r'Cantons of Switzerland.csv', usecols = canton_cols)
code_to_canton = cantons.set_index('Code')['Canton'].to_dict()
canton_to_code = cantons.set_index('Canton')['Code'].to_dict()


''' Return the percentage of dropped rows from before to after '''
def get_dropped_perc(before, after):
    return (1 - (after.shape[0] / before.shape[0])) * 100


def geo_query(name):
    """Do a lookup on geonames.org for name. Returns the first query result."""
    try:
        # Encode the arguments to avoid problems with special characters, spaces etc. 
        encoded_args = urlencode({'name': name, 'country':'ch', 'maxRows':'1', 'username': USERNAME} )
        
        # Request the geonames API
        r = requests.get(URL + encoded_args)
        
        # Parse the result as json
        result = r.json()
        
        if result['totalResultsCount'] > 0:
            # If there was a positive result, get the info from the result
            geonames = result['geonames']
            geo = geonames[0]
            
            canton = geo['adminCode1']
            lat = geo['lat']
            lng = geo['lng']
            
            if canton == '00':
                return False
            
            return {'canton': canton, 'lat': lat, 'long': lng}
        else:
            # Else, we return false
            return False
        
    except BaseException as e:
        # Sometimes we get some strange results back, which leads our parsing to crash.
        # This is allso returned as False
        print('Exception:', name, e)
        return False
        
def geo_lookup(name):
    """Cached version of geo_query """
    if geo_cache[name] != '':
        result = geo_cache[name]
    else:
        result = geo_query(name)
        geo_cache[name] = result
    return result

def get_geo_dict(group):
    """
    Returns a dictionary of name -> {canton info} mapping, achieved by querying geonames.org
    Input is a pandas.groupby object. """
    
    # Initialize result sets
    geo_res = {}
    geo_err = set()
    
    
    for ind, group in group:
        # The group name is the first element of the splitted index
        name = ind.split(' - ')[0]
        
        # Do a lookup with our cached API-function, using the whole name
        res = geo_query(name)
        
        
        if res:
            # If there is a result, save it
            geo_res[ind] = res
        else:
            # If the result is negative, try to do a query with only the last word,
            # which is often the name of the city
            name = name.split(' ')[-1].strip(')')
            res = geo_query(name)
            
            if res:
                # If positive, save the result
                geo_res[ind] = res
            else:
                # Else, save it as an error to be handeled later
                geo_err.add(ind)
    
    return geo_res, geo_err


def is_canton_code(code):
    ''' Check whether the code is a valid swizz canton code. '''
    try:
        get_canton(code.strip().upper())
    except:
        return False
    return True
        

def get_canton_code(canton):
    ''' For a cantom name, get the beloning code '''
    return canton_to_code[canton]


def get_canton(code):
    ''' For a cantom code, get the beloning name '''
    return code_to_canton[code]