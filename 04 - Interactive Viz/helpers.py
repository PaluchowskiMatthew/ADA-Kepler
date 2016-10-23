import pandas as pd
from urllib.parse import urlencode
from pprint import *
import requests

# Get the cantons data
canton_cols = ['Code', 'Canton']
cantons = pd.read_csv(r'Cantons of Switzerland.csv', usecols = canton_cols)
code_to_canton = cantons.set_index('Code')['Canton'].to_dict()
canton_to_code = cantons.set_index('Canton')['Code'].to_dict()


''' Return the percentage of dropped rows from before to after '''
def get_dropped_perc(before, after):
    return (1 - (after.shape[0] / before.shape[0])) * 100

'''
By using np.save and np.load on the dict, we can avoid doing the requests more than once :)
This does not work now because of some utf8, should be figured out!
'''
np.save('canton_dict.npy',urlencode(set()))
np.save('has_looked_up.npy',{})

has_looked_up = np.load('has_looked_up.npy').item()
canton_dict = np.load('canton_dict.npy').item()

def check_looked_up(name):
    try:
        has_looked_up[name]
    except:
        return False
    return True
def set_has_looked_up(name):
    has_looked_up.add(name)
    
def get_canton(name):
    try:
        return canton_dict[name]
    except:
        return ''

    
''' Do a lookup on geonames.org for name. Returns the first query result. '''
def geo_lookup(name):
    # Insert username
    username = 'user1'
    
    url = r'http://api.geonames.org/searchJSON?'
    encoded_args = urlencode({'name': name, 'country':'ch', 'maxRows':'1', 'username': username} )
    
    try:
        r = requests.get(url + encoded_args)

        result = r.json()

        if result['totalResultsCount'] > 0:
            geoname = result['geonames'][0]
            admincode = geoname['adminCode1']
            return admincode
    except:
        print('For qurery parmas:')
        pprint(encoded_args)
        pprint(r.json())
        

''' Check whether the code is a valid swizz canton code. '''
def is_canton_code(code):
    
    try:
        get_canton(code.strip().upper())
    except:
        return False
    return True
        
''' For a cantom name, get the beloning code '''
def get_canton_code(canton):
    return canton_to_code[canton]

''' For a cantom code, get the beloning name '''
def get_canton(code):
    return code_to_canton[code]