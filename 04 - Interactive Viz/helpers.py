import pandas as pd

def get_dropped_perc(origin, after):
    return (1 - (after.shape[0] / origin.shape[0])) * 100


# Get the cantons data
canton_cols = ['Code', 'Canton']
cantons = pd.read_csv(r'Cantons of Switzerland.csv', usecols = canton_cols)
code_to_canton = cantons.set_index('Code').to_dict()
canton_to_code = cantons.set_index('Canton').to_dict()

def get_canton_code(canton):
    return canton_to_code[canton]

def get_canton(code):
    return code_to_canton[code]
