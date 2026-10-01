"""Reduce Natural Earth to the properties and coordinate precision used on the page.

Usage: python tools/prepare_geography.py --source-dir ../research
Expected input files: ne-states.json and ne-world.json (URLs in data/README.md).
No statistical observations are inferred from the boundary geometry.
"""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('--source-dir',type=Path,required=True)
args=p.parse_args()
states={r['state']:r for r in json.loads((ROOT/'data/states.json').read_text())}
def rounded(a):
    if isinstance(a,list):return [rounded(v) for v in a]
    return round(a,3) if isinstance(a,float) else a
def geometry(g):return {'type':g['type'],'coordinates':rounded(g['coordinates'])}
source=json.loads((args.source_dir/'ne-states.json').read_text())
features=[]
for f in source['features']:
    name=f['properties']['name']
    if f['properties'].get('admin')=='Australia' and name in states:
        features.append({'type':'Feature','properties':states[name],'geometry':geometry(f['geometry'])})
(ROOT/'data/australia.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},separators=(',',':')))
world=json.loads((args.source_dir/'ne-world.json').read_text())
features=[{'type':'Feature','properties':{'country':f['properties']['ADMIN']},'geometry':geometry(f['geometry'])}
          for f in world['features'] if f['properties']['ADMIN']!='Antarctica']
(ROOT/'data/world.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},separators=(',',':')))
coords={f['properties']['ADMIN']:[f['properties']['LABEL_X'],f['properties']['LABEL_Y']] for f in world['features']}
values={'Malaysia':22.6,'Kenya':20.5,'Vietnam':18.7,'Ecuador':15.8,'China':12.5}
flows=[];labels=[]
for country,value in values.items():
    flows.append({'type':'Feature','properties':{'country':country,'value':value},
                  'geometry':{'type':'LineString','coordinates':[coords[country],coords['Australia']]}})
for country in list(values)+['Australia']:
    lon,lat=coords[country]
    # Label offsets improve separation on a small world map; endpoints stay at source anchors.
    off={'Malaysia':(12,-5),'Vietnam':(15,1),'China':(-3,6)}.get(country,(0,0))
    labels.append({'country':country,'longitude':lon,'latitude':lat,
                   'label_longitude':lon+off[0],'label_latitude':lat+off[1]})
(ROOT/'data/flower_flows.geojson').write_text(json.dumps({'type':'FeatureCollection','features':flows},indent=2))
(ROOT/'data/flow_labels.json').write_text(json.dumps(labels,indent=2))
print('Prepared maps from Natural Earth. Symbols and links indicate administrative totals.')
