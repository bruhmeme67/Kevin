"""Recreate compact chart data from the transcribed source tables.

Usage: python tools/prepare_data.py
Numeric source values are deliberately preserved at their published precision.
See data/README.md for sources, units and missing-value rules.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)

def save(name, rows):
    (DATA / (name + '.json')).write_text(json.dumps(rows, indent=2) + '\n')
    if rows and isinstance(rows, list) and isinstance(rows[0], dict):
        keys = list(dict.fromkeys(k for row in rows for k in row))
        with (DATA / (name + '.csv')).open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)

# Hort Innovation 2024/25, printed pages 409, 414, 419.
source = {
    'Cut flowers': {
        'production': [277.3, 314.7, 308.4, 289.9, 324.7],
        'exports': [7.9, 9.5, 9.3, 9.0, 8.0],
        'imports': [95.4, 104.6, 103.0, 96.7, 108.1],
        'wholesale_supply': [380.5, 438.7, 430.0, 404.2, 452.7],
    },
    'Nursery': {
        'production': [2789.5, 2833.0, 2775.3, 2648.0, 2757.0],
        'exports': [6.0, 8.7, 14.1, 8.6, 8.4],
        'imports': [46.1, 47.8, 43.4, 40.3, 42.5],
        'wholesale_supply': [2928.6, 2972.7, 2902.7, 2773.5, 2888.8],
        'units_million': [2324, 2334, 2264, 2064, 2133],
    },
    'Turf': {
        'production': [269.5, 281.9, 296.1, 301.4, 300.8],
        'wholesale_supply': [269.5, 281.9, 296.1, 301.4, 300.8],
        'area_ha': [3749, 3312, 3479, 3542, 3535],
    },
}
annual = []
for sector, metrics in source.items():
    for i, year in enumerate(range(2021, 2026)):
        row = {'sector': sector, 'year': year, 'financial_year': f'{year-1}/{str(year)[2:]}'}
        row.update({k: v[i] for k, v in metrics.items()})
        row['production_index'] = row['production'] / metrics['production'][0] * 100
        row['production_yoy_pct'] = None if i == 0 else (metrics['production'][i] / metrics['production'][i-1] - 1) * 100
        if 'imports' in row:
            row['net_imports'] = row['imports'] - row['exports']
        if 'units_million' in row:
            row['units_index'] = row['units_million'] / metrics['units_million'][0] * 100
            row['value_per_unit'] = row['production'] / row['units_million']
        annual.append(row)
save('annual', annual)

# Latest ABS March 2026 release, 310104.xlsx, Persons, June 2025 row.
# The spreadsheet uses the first day of the quarter-ending month as its date key.
pop = {
    'New South Wales': 8587369, 'Victoria': 7064041, 'Queensland': 5670203,
    'South Australia': 1901652, 'Western Australia': 3044966,
    'Tasmania': 577827, 'Northern Territory': 265978,
    'Australian Capital Territory': 484681,
}
# Hort Innovation printed pp. 410, 415. Missing flower figures are NOT zero.
flowers = {'Victoria': 114.4, 'Western Australia': 71.1, 'Queensland': 61.8,
           'New South Wales': 40.2, 'South Australia': 30.9, 'Tasmania': 6.2}
flower_share = {'Victoria': 35.2, 'Western Australia': 21.9, 'Queensland': 19.0,
                'New South Wales': 12.4, 'South Australia': 9.5, 'Tasmania': 1.9}
nursery = {'New South Wales': 827.0, 'Queensland': 827.0, 'Victoria': 772.0,
           'Western Australia': 220.6, 'South Australia': 55.2,
           'Northern Territory': 35.9, 'Tasmania': 19.2}
nursery_share = {'New South Wales':30, 'Queensland':30, 'Victoria':28,
                 'Western Australia':8, 'South Australia':2,
                 'Northern Territory':1.3, 'Tasmania':0.7}
abbreviations = dict(zip(pop, ['NSW','VIC','QLD','SA','WA','TAS','NT','ACT']))
# Approximate administrative symbol anchors, not farm or port coordinates.
anchors = {'New South Wales': [146.7,-32.6], 'Victoria': [144.7,-37.0],
           'Queensland': [144.3,-22.5], 'South Australia': [135.6,-29.9],
           'Western Australia': [121.5,-25.3], 'Tasmania': [146.6,-42.1],
           'Northern Territory': [133.3,-19.5], 'Australian Capital Territory': [149.1,-35.4]}
states=[]
for state, population in pop.items():
    fv=flowers.get(state)
    states.append({'state':state, 'abbr':abbreviations[state], 'population':population,
       'population_date':'2025-06-30', 'year':2025,
       'flower_production':fv, 'nursery_production':nursery.get(state),
       'flower_share':flower_share.get(state), 'nursery_share':nursery_share.get(state),
       'flower_per_resident':None if fv is None else fv*1e6/population,
       'longitude':anchors[state][0], 'latitude':anchors[state][1],
       'flower_status':'Not separately reported' if fv is None else 'Reported'})
save('states',states)

# p. 411: rounded money values and published percentage shares are separate fields.
country_imports={'Malaysia':[22.9,22.6,22.6], 'Kenya':[18.1,17.8,20.5],
    'Vietnam':[6.0,9.8,18.7], 'Ecuador':[15.2,15.5,15.8],
    'China':[17.9,10.7,12.5], 'Others':[22.9,20.2,17.9]}
imports=[]
for country, values in country_imports.items():
    for year,value in zip(range(2023,2026),values):
        imports.append({'country':country,'year':year,'financial_year':f'{year-1}/{str(year)[2:]}','value':value})
save('flower_imports',imports)
save('flower_exports',[
    {'country':'Japan','value':1.9,'reported_value':'1.9','share':24.6},
    {'country':'Netherlands','value':1.9,'reported_value':'1.9','share':23.8},
    {'country':'United States','value':1.7,'reported_value':'1.7','share':22.0},
    {'country':'China','value':1.1,'reported_value':'1.1','share':14.3},
    {'country':'South Korea','value':None,'reported_value':'<1','share':7.9},
    {'country':'Others','value':None,'reported_value':'<1','share':7.3},
])
save('state_roles',[
    {'state':'Queensland','production_share':19.0,'export_share':58.9},
    {'state':'Western Australia','production_share':21.9,'export_share':22.2},
    {'state':'Victoria','production_share':35.2,'export_share':18.0},
    {'state':'New South Wales','production_share':12.4,'export_share':0.9},
])
save('flower_state_imports',[
    {'state':state,'year':year,'value':value}
    for state,values in {'Victoria':[31.8,37.5,46.7], 'New South Wales':[37.5,28.8,28.8],
      'Western Australia':[22.4,16.5,14.9],'Queensland':[6.7,9.0,11.5],
      'South Australia':[4.6,4.9,6.3]}.items()
    for year,value in zip(range(2023,2026),values)
])
print('Prepared source tables. No values below $1m have been replaced with point estimates.')
