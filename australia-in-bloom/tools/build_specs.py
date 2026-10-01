"""Build readable Vega / Vega-Lite specifications from the compact source tables."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data'
S=ROOT/'specs'
S.mkdir(exist_ok=True)
INK='#193c32'; GREEN='#147d64'; PINK='#b63468'; GOLD='#ae7c24'; BLUE='#367fa5'
SECTORS=['Nursery','Cut flowers','Turf']
COLORS=[GREEN,PINK,GOLD]
COUNTRIES=['Malaysia','Kenya','Vietnam','Ecuador','China']
COUNTRY_COLORS=['#236853','#397d9f','#b63468','#a97823','#735ca2']
VL='https://vega.github.io/schema/vega-lite/v5.json'
VEGA='https://vega.github.io/schema/vega/v5.json'
config={
 'font':'Arial','view':{'stroke':None},
 'axis':{'labelFontSize':13,'titleFontSize':13,'titleFontWeight':'normal','titlePadding':13,
         'labelColor':'#4d6158','titleColor':'#4d6158','gridColor':'#e4ebe6','domain':False,
         'tickColor':'#ced9d1','labelPadding':6,'labelLimit':180},
 'legend':{'title':None,'labelFontSize':13,'orient':'top','symbolSize':100,'padding':8,
           'labelColor':INK,'labelLimit':180},
 'text':{'fontSize':13,'color':INK},'title':{'fontSize':15,'anchor':'start','color':INK}
}
def load(name):return json.loads((D/f'{name}.json').read_text())
def write(name,spec):
    (S/f'{name}.json').write_text(json.dumps(spec,indent=2)+'\n')
def base(h=260):return {'$schema':VL,'width':'container','height':h,'background':None,
                        'autosize':{'type':'fit','contains':'padding'},'config':config}
def tip(f,t='quantitative',title=None,fmt=None):
    o={'field':f,'type':t}
    if title:o['title']=title
    if fmt:o['format']=fmt
    return o
def sector_color():return {'field':'sector','type':'nominal','scale':{'domain':SECTORS,'range':COLORS},'legend':{'orient':'top'}}

# 01. Genuine Vega treemap transform. Tree hierarchy is root > sector.
treemap={
 '$schema':VEGA,'description':'Production value of nursery, cut flowers and turf in 2024/25.',
 'width':600,'height':270,'padding':0,'autosize':{'type':'fit','contains':'padding'},
 'data':[
  {'name':'annual','url':'data/annual.json'},
  {'name':'leaves','source':'annual','transform':[{'type':'filter','expr':'datum.year == 2025'},
    {'type':'formula','as':'id','expr':'datum.sector'},{'type':'formula','as':'parent','expr':'"All"'}]},
  {'name':'tree_root','values':[{'id':'All','parent':None,'production':0}]},
  {'name':'tree','source':['tree_root','leaves'],'transform':[{'type':'stratify','key':'id','parentKey':'parent'},
    {'type':'treemap','field':'production','method':{'signal':'width < 500 ? "slice" : "binary"'},'sort':{'field':'value','order':'descending'},
     'size':[{'signal':'width'},{'signal':'height'}],'paddingInner':4}]},
  {'name':'cells','source':'tree','transform':[{'type':'filter','expr':'datum.depth == 1'}]}
 ],
 'scales':[{'name':'color','type':'ordinal','domain':SECTORS,'range':COLORS}],
 'marks':[
  {'type':'rect','from':{'data':'cells'},'encode':{'update':{
    'x':{'field':'x0'},'x2':{'field':'x1'},'y':{'field':'y0'},'y2':{'field':'y1'},
    'fill':{'scale':'color','field':'sector'},
    'tooltip':{'signal':'{"Sector":datum.sector,"Production (A$m)":datum.production,"Share":format(datum.production/3382.5,".1%")}'}}}},
  {'type':'text','from':{'data':'cells'},'encode':{'update':{
    'x':{'signal':'datum.x0+12'},'y':{'signal':'datum.y0 + (datum.y1-datum.y0 < 65 ? (datum.y1-datum.y0)/2+4 : 25)'},'fill':{'value':'white'},
    'text':{'signal':'datum.y1-datum.y0 < 65 ? datum.sector+"  $"+format(datum.production,",.1f")+"m  ("+format(datum.production/3382.5,".1%")+")" : (datum.sector == "Cut flowers" ? "Flowers" : datum.sector)'},'font':{'value':'Arial'},'fontSize':{'signal':'datum.y1-datum.y0 < 65 ? 13 : 15'},'fontWeight':{'value':'bold'},
    'limit':{'signal':'datum.x1-datum.x0-18'}}}},
  {'type':'text','from':{'data':'cells'},'encode':{'update':{
    'x':{'signal':'datum.x0+12'},'y':{'signal':'datum.y0+49'},'fill':{'value':'white'},
    'text':{'signal':'"$"+format(datum.production,",.1f")+"m"'},
    'font':{'value':'Arial'},'fontSize':{'value':14},'limit':{'signal':'datum.x1-datum.x0-18'},'opacity':{'signal':'datum.y1-datum.y0 < 65 ? 0 : 1'}}}},
  {'type':'text','from':{'data':'cells'},'encode':{'update':{
    'x':{'signal':'datum.x0+12'},'y':{'signal':'datum.y1-16'},'fill':{'value':'white'},
    'text':{'signal':'format(datum.production/3382.5,".1%")'},
    'font':{'value':'Arial'},'fontSize':{'value':22},'fontWeight':{'value':'bold'},
    'opacity':{'signal':'datum.y1-datum.y0 > 85 ? 1 : 0'}}}}
 ]}
write('01-sector-treemap',treemap)

# 02. Index permits comparison of growth despite vastly different sector sizes.
s=base(285);s.update({
 'data':{'url':'data/annual.json'},
 'params':[{'name':'sectorFocus','value':'All','bind':{'input':'select','options':['All']+SECTORS,'name':'Highlight sector: '}}],
 'encoding':{
  'x':{'field':'financial_year','type':'ordinal','title':None,'axis':{'labelAngle':0}},
  'y':{'field':'production_index','type':'quantitative','title':'Production value · 2020/21 = 100','scale':{'domain':[92,120],'zero':False}},
  'color':sector_color(),'opacity':{'condition':{'test':'sectorFocus == "All" || datum.sector == sectorFocus','value':1},'value':0.15},
  'tooltip':[tip('sector','nominal','Sector'),tip('financial_year','nominal','Year'),tip('production','quantitative','Production (A$m)',',.1f'),tip('production_index','quantitative','Index','.1f')]},
 'layer':[
  {'mark':{'type':'line','strokeWidth':3,'point':{'filled':True,'size':60}}},
  {'data':{'values':[{'baseline':100}]},'mark':{'type':'rule','strokeDash':[4,4],'color':'#71887a'},
   'encoding':{'x':{'value':0},'x2':{'value':{'expr':'width'}},'y':{'field':'baseline','type':'quantitative'},'color':{'value':'#71887a'},'opacity':{'value':0.6},'tooltip':[]}}
 ]})
write('02-production-trend',s)

# 03. Year-on-year changes, computed from the same rounded monetary source values.
s=base(165);s.update({'data':{'url':'data/annual.json'},
 'transform':[{'filter':'datum.year > 2021'}],
 'encoding':{'x':{'field':'financial_year','type':'ordinal','title':None,'axis':{'labelAngle':0,'orient':'top'}},
  'y':{'field':'sector','type':'nominal','title':None,'sort':SECTORS},
  'tooltip':[tip('sector','nominal','Sector'),tip('financial_year','nominal','Year'),tip('production_yoy_pct','quantitative','Annual change (%)','+.1f')]},
 'layer':[{'mark':{'type':'rect','stroke':'white','strokeWidth':3},'encoding':{'color':{
  'field':'production_yoy_pct','type':'quantitative','scale':{'domain':[-14,0,14],'range':['#be8642','#f3f5ef','#147d64']},'legend':None}}},
 {'transform':[{'calculate':'format(datum.production_yoy_pct,"+.1f")+"%"','as':'label'}],
  'mark':{'type':'text','fontSize':14,'fontWeight':'bold'},'encoding':{'text':{'field':'label'},
  'color':{'condition':{'test':'abs(datum.production_yoy_pct)>8','value':'white'},'value':INK}}}]})
write('03-growth-heatmap',s)

projection={'type':'conicEqualArea','parallels':[-18,-36],'rotate':[-134,0,0],'center':[0,-27]}
geo={'url':'data/australia.geojson','format':{'type':'json','property':'features'}}
maptips=[tip('properties.state','nominal','State'),tip('properties.flower_production','quantitative','Flower production (A$m)',',.1f'),
         tip('properties.population','quantitative','Residents, 30 June 2025',','),
         tip('properties.flower_per_resident','quantitative','Production per resident (A$)','.2f')]

# 04. Normalised choropleth, deliberately not raw totals as fill.
s=base(385);s.update({'projection':projection,'layer':[
 {'data':geo,'mark':{'type':'geoshape','fill':'#e1e7e1','stroke':'white','strokeWidth':1.2},
  'encoding':{'tooltip':[tip('properties.state','nominal','State'),tip('properties.flower_status','nominal','Reporting')]}},
 {'data':geo,'transform':[{'filter':'isValid(datum.properties.flower_per_resident)'}],
  'mark':{'type':'geoshape','stroke':'white','strokeWidth':1.2},'encoding':{
   'color':{'field':'properties.flower_per_resident','type':'quantitative','scale':{'domain':[0,25],'range':['#edf4ed','#11644f']},
     'legend':{'orient':'bottom','title':'A$ per resident','gradientLength':210,'format':'$.0f'}},'tooltip':maptips}},
 {'data':{'url':'data/states.json'},'transform':[{'filter':'datum.abbr != "ACT"'}],
  'mark':{'type':'text','fontWeight':'bold','fontSize':13},
  'encoding':{'longitude':{'field':'longitude','type':'quantitative'},'latitude':{'field':'latitude','type':'quantitative'},
   'text':{'field':'abbr'},'color':{'condition':{'test':'datum.flower_per_resident>14','value':'white'},'value':INK},
   'tooltip':[tip('state','nominal','State'),tip('flower_per_resident','quantitative','Production per resident (A$)','.2f')]}}
]})
write('04-production-choropleth',s)

# 05. Symbol area encodes totals. Metric switch keeps the same underlying map.
s=base(385);s.update({'projection':projection,
 'params':[{'name':'mapSector','value':'Cut flowers','bind':{'input':'select','options':['Cut flowers','Nursery'],'name':'Compare sector: '}}],
 'layer':[
 {'data':geo,'mark':{'type':'geoshape','fill':'#edf1ec','stroke':'white','strokeWidth':1.2}},
 {'data':{'url':'data/states.json'},'transform':[
   {'calculate':'mapSector == "Cut flowers" ? datum.flower_production : datum.nursery_production','as':'value'},
   {'filter':'isValid(datum.value)'}],
  'mark':{'type':'circle','stroke':'white','strokeWidth':1.2,'opacity':0.8,
          'color':{'expr':f'mapSector == "Cut flowers" ? "{PINK}" : "{GREEN}"'}},
  'encoding':{'longitude':{'field':'longitude','type':'quantitative'},'latitude':{'field':'latitude','type':'quantitative'},
   'size':{'field':'value','type':'quantitative','scale':{'range':[0,3000],'zero':True},'legend':{'orient':'bottom','title':'Production (A$m)','format':',.0f'}},
   'tooltip':[tip('state','nominal','State'),tip('value','quantitative','Production (A$m)',',.1f')]}},
 {'data':{'url':'data/states.json'},'transform':[{'filter':'datum.abbr != "ACT"'}],
  'mark':{'type':'text','fontSize':12,'fontWeight':'bold','dy':{'expr':'datum.abbr == "TAS" ? 18 : datum.abbr == "VIC" ? 0 : -32'},'dx':{'expr':'datum.abbr == "VIC" ? -40 : 0'},'color':INK},
  'encoding':{'longitude':{'field':'longitude','type':'quantitative'},'latitude':{'field':'latitude','type':'quantitative'},'text':{'field':'abbr'}}}
]})
write('05-production-symbols',s)

# 06. Marimekko area is proportional to a state-sector production value.
rows=[]; states={r['abbr']:r for r in load('states')}
groups=[('NSW',['NSW']),('QLD',['QLD']),('VIC',['VIC']),('WA',['WA']),('SA + TAS',['SA','TAS'])]
values=[(label,sum(states[k]['flower_production'] for k in keys),sum(states[k]['nursery_production'] for k in keys)) for label,keys in groups]
total=sum(f+n for _,f,n in values);left=0
for label,f,n in values:
    width=(f+n)/total
    for sector,lo,hi,v in [('Nursery',0,n/(f+n),n),('Cut flowers',n/(f+n),1,f)]:
        rows.append({'region':label,'sector':sector,'x0':left,'x1':left+width,'cx':left+width/2,'y0':lo,'y1':hi,
                     'value':v,'sector_share':v/(f+n),'combined_value':f+n,'cy':(lo+hi)/2})
    left+=width
(D/'state_mix.json').write_text(json.dumps(rows,indent=2)+'\n')
s=base(310);s.update({'data':{'url':'data/state_mix.json'},'layer':[
 {'mark':{'type':'rect','stroke':'white','strokeWidth':2},'encoding':{
  'x':{'field':'x0','type':'quantitative','scale':{'domain':[0,1]},'axis':None},'x2':{'field':'x1'},
  'y':{'field':'y1','type':'quantitative','scale':{'domain':[0,1.23]},'axis':{'values':[0,0.25,0.5,0.75,1],'format':'.0%','title':'Within-region production mix'}},'y2':{'field':'y0'},
  'color':{'field':'sector','type':'nominal','scale':{'domain':['Nursery','Cut flowers'],'range':[GREEN,PINK]}},
  'tooltip':[tip('region','nominal','Region'),tip('sector','nominal','Sector'),tip('value','quantitative','Production (A$m)',',.1f'),tip('sector_share','quantitative','Share within region','.1%'),tip('combined_value','quantitative','Combined value (A$m)',',.1f')]}},
 {'transform':[{'filter':'datum.sector == "Nursery"'},{'calculate':'datum.region == "SA + TAS" ? 1.17 : 1.06','as':'label_y'}], 'mark':{'type':'text','fontSize':12,'fontWeight':'bold'},
  'encoding':{'x':{'field':'cx','type':'quantitative'},'y':{'field':'label_y','type':'quantitative'},'text':{'field':'region'}}},
 {'transform':[{'filter':'datum.sector == "Cut flowers" && datum.sector_share > 0.12'}],
  'mark':{'type':'text','fontSize':13,'fontWeight':'bold','color':'white',
          'opacity':{'expr':'(datum.x1-datum.x0)*width >= 35 ? 1 : 0'}},
  'encoding':{'x':{'field':'cx','type':'quantitative'},'y':{'field':'cy','type':'quantitative'},'text':{'field':'sector_share','format':'.0%'}}}
]})
write('06-regional-marimekko',s)

# 07. Export-origin shares and production shares have different denominators.
s=base(235);s.update({'data':{'url':'data/state_roles.json'},
 'encoding':{'y':{'field':'state','type':'nominal','sort':['Queensland','Western Australia','Victoria','New South Wales'],'title':None},
              'tooltip':[tip('state','nominal','State'),tip('production_share','quantitative','Share of AU production (%)','.1f'),tip('export_share','quantitative','Share of AU exports (%)','.1f')]},
 'layer':[
 {'mark':{'type':'rule','color':'#b5c5bb','strokeWidth':3},'encoding':{'x':{'field':'production_share','type':'quantitative','title':'Share of the Australian total (%)','scale':{'domain':[0,65]}},'x2':{'field':'export_share'}}},
 {'transform':[{'fold':['production_share','export_share'],'as':['role','share']},
   {'calculate':'datum.role == "production_share" ? "Production" : "Exports"','as':'role_label'}],
  'mark':{'type':'point','filled':True,'size':110},'encoding':{
   'x':{'field':'share','type':'quantitative'},'color':{'field':'role_label','type':'nominal','scale':{'domain':['Production','Exports'],'range':[PINK,BLUE]}},
   'shape':{'field':'role_label','type':'nominal','scale':{'domain':['Production','Exports'],'range':['circle','diamond']},'legend':{'orient':'top','title':None}}}}
]})
write('07-state-roles',s)

# 08. Geodesic country-pair flows; no actual ports or transport routes are claimed.
s=base(445);s.update({'projection':{'type':'equalEarth','rotate':[-135,0,0]},
 'params':[{'name':'origin','value':'All','bind':{'input':'select','options':['All']+COUNTRIES,'name':'Highlight origin: '}}],
 'layer':[
 {'data':{'url':'data/world.geojson','format':{'type':'json','property':'features'}},
  'mark':{'type':'geoshape','fill':'#e5ebe3','stroke':'#fff','strokeWidth':0.45}},
 {'data':{'url':'data/flower_flows.geojson','format':{'type':'json','property':'features'}},
  'mark':{'type':'geoshape','filled':False,'strokeCap':'round'},'encoding':{
   'strokeWidth':{'field':'properties.value','type':'quantitative','scale':{'domain':[0,25],'range':[0,10]},'legend':{'orient':'bottom','title':'Import value (A$m)','values':[10,20],'symbolType':'stroke','symbolStrokeColor':'#71887a','symbolSize':300}},
   'color':{'field':'properties.country','type':'nominal','scale':{'domain':COUNTRIES,'range':COUNTRY_COLORS},'legend':None},
   'opacity':{'condition':{'test':'origin == "All" || datum.properties.country == origin','value':0.75},'value':0.07},
   'tooltip':[tip('properties.country','nominal','Origin'),tip('properties.value','quantitative','Imports to Australia (A$m)','.1f')]}},
 {'data':{'url':'data/flow_labels.json'},'mark':{'type':'circle','size':40,'color':INK},
  'encoding':{'longitude':{'field':'longitude','type':'quantitative'},'latitude':{'field':'latitude','type':'quantitative'}}},
 {'data':{'url':'data/flow_labels.json'},'mark':{'type':'text','dy':-12,'fontWeight':'bold','fontSize':12,'color':INK},
  'encoding':{'longitude':{'field':'label_longitude','type':'quantitative'},'latitude':{'field':'label_latitude','type':'quantitative'},'text':{'field':'country'}}}
]})
write('08-flower-flow-map',s)

# 09. The top-five origins are ranked among themselves, excluding 'Others'.
s=base(300);s.update({'data':{'url':'data/flower_imports.json'},
 'transform':[{'filter':'datum.country != "Others"'},
  {'window':[{'op':'rank','as':'rank'}],'sort':[{'field':'value','order':'descending'}],'groupby':['year']}],
 'params':[{'name':'countryFocus','value':'All','bind':{'input':'select','options':['All']+COUNTRIES,'name':'Follow a country: '}}],
 'encoding':{'x':{'field':'year','type':'quantitative','scale':{'domain':[2022.95,2025.65],'zero':False},'title':None,
  'axis':{'values':[2023,2024,2025],'format':'d','labelExpr':'datum.value == 2023 ? "2022/23" : datum.value == 2024 ? "2023/24" : "2024/25"'}},
  'y':{'field':'rank','type':'quantitative','scale':{'domain':[5.4,0.6],'zero':False},'axis':{'values':[1,2,3,4,5]},'title':'Rank among five named origins'},
  'color':{'field':'country','type':'nominal','scale':{'domain':COUNTRIES,'range':COUNTRY_COLORS},'legend':{'columns':3}},
  'opacity':{'condition':{'test':'countryFocus == "All" || datum.country == countryFocus','value':1},'value':0.12},
  'tooltip':[tip('country','nominal','Origin'),tip('financial_year','nominal','Year'),tip('rank','quantitative','Rank','d'),tip('value','quantitative','Imports (A$m)','.1f')]},
 'layer':[{'mark':{'type':'line','strokeWidth':3,'point':{'filled':True,'size':70}}},
 {'transform':[{'filter':'datum.year == 2025'}],'mark':{'type':'text','align':'left','dx':10,'fontSize':12},
  'encoding':{'text':{'field':'country'}}}]})
write('09-import-bump',s)

# 10. Changes sum to $11.4m; source-table rounding residual is the same in both years.
countries=load('flower_imports');wf=[];running=0
for i,country in enumerate(['Malaysia','Kenya','Vietnam','Ecuador','China','Others']):
    v={r['year']:r['value'] for r in countries if r['country']==country}
    delta=round(v[2025]-v[2024],1); end=round(running+delta,1)
    wf.append({'country':country,'start':min(running,end),'end':max(running,end),'after':end,
               'change':delta,'order':i,'kind':'Fall' if delta<0 else 'Rise','label':f'{delta:+.1f}'})
    running=end
wf.append({'country':'Net rise','start':0,'end':11.4,'after':11.4,'change':11.4,'order':6,'kind':'Total','label':'+11.4'})
(D/'import_change.json').write_text(json.dumps(wf,indent=2)+'\n')
s=base(300);s.update({'data':{'url':'data/import_change.json'},'encoding':{
 'x':{'field':'country','type':'ordinal','sort':{'field':'order'},'title':None,'axis':{'labelAngle':-25,'labelLimit':110}},
 'y':{'field':'end','type':'quantitative','title':'Contribution to import growth (A$m)','scale':{'domain':[0,15.2]}},
 'tooltip':[tip('country','nominal','Origin'),tip('change','quantitative','Change 2023/24–2024/25 (A$m)','+.1f')]},
 'layer':[{'mark':{'type':'bar','width':{'band':0.7}},'encoding':{'y2':{'field':'start'},
  'color':{'field':'kind','type':'nominal','scale':{'domain':['Rise','Fall','Total'],'range':[GREEN,GOLD,INK]},'legend':None}}},
 {'mark':{'type':'text','dy':-9,'fontSize':13,'fontWeight':'bold'},'encoding':{'text':{'field':'label'}}}]})
write('10-import-waterfall',s)

# 11. Use published shares to avoid turning '<1' values into invented dollars.
s=base(260);s.update({'data':{'url':'data/flower_exports.json'},'encoding':{
 'y':{'field':'country','type':'nominal','sort':['Japan','Netherlands','United States','China','South Korea','Others'],'title':None},
 'x':{'field':'share','type':'quantitative','title':'Share of flower export value (%)','scale':{'domain':[0,29]}},
 'tooltip':[tip('country','nominal','Destination'),tip('share','quantitative','Export share (%)','.1f'),tip('reported_value','nominal','Reported export value (A$m)')]},
 'layer':[{'mark':{'type':'bar','color':BLUE,'height':19}},
 {'transform':[{'calculate':'format(datum.share,".1f")+"%"','as':'label'}],
  'mark':{'type':'text','align':'left','dx':6,'fontSize':13},'encoding':{'text':{'field':'label'}}}]})
write('11-export-destinations',s)

# 12. Mirror bars preserve a single shared dollar scale across import and export.
s=base(265);s.update({'data':{'url':'data/annual.json'},
 'transform':[{'filter':'datum.sector == "Cut flowers"'}, {'fold':['imports','exports'],'as':['direction','value']},
  {'calculate':'datum.direction == "imports" ? -datum.value : datum.value','as':'signed'},
  {'calculate':'datum.direction == "imports" ? "Imports" : "Exports"','as':'direction_label'}],
 'encoding':{'y':{'field':'financial_year','type':'ordinal','title':None},
  'x':{'field':'signed','type':'quantitative','title':'Imports (left) and exports (right), A$m',
       'scale':{'domain':[-120,30]},'axis':{'labelExpr':'abs(datum.value)','values':[-100,-50,0,25]}},
  'color':{'field':'direction_label','type':'nominal','scale':{'domain':['Imports','Exports'],'range':[PINK,BLUE]}},
  'tooltip':[tip('financial_year','nominal','Year'),tip('direction_label','nominal','Trade'),tip('value','quantitative','Value (A$m)','.1f')]},
 'layer':[{'mark':{'type':'bar','height':22}},
 {'mark':{'type':'text','dx':{'expr':'datum.signed < 0 ? -18 : 15'},'fontSize':12,'color':INK},
  'encoding':{'text':{'field':'value','format':'.1f'}}}]})
write('12-trade-butterfly',s)

# 13. A connected scatter plot relates nursery units to value, with chronological arrows via labels.
s=base(285);s.update({'data':{'url':'data/annual.json'},'transform':[{'filter':'datum.sector == "Nursery"'}],
 'encoding':{'x':{'field':'units_million','type':'quantitative','title':'Plants produced (million units)',
                 'scale':{'domain':[2000,2400],'zero':False},'axis':{'format':',.0f','tickCount':4}},
  'y':{'field':'production','type':'quantitative','title':'Production value (A$m)',
       'scale':{'domain':[2600,2880],'zero':False},'axis':{'format':',.0f','tickCount':4}},
  'tooltip':[tip('financial_year','nominal','Year'),tip('units_million','quantitative','Plants (million)',',.0f'),tip('production','quantitative','Production (A$m)',',.1f')]},
 'layer':[{'mark':{'type':'line','color':'#9aaea1','strokeWidth':2},'encoding':{'order':{'field':'year','type':'quantitative'}}},
 {'mark':{'type':'point','filled':True,'size':100},'encoding':{'color':{'condition':{'test':'datum.year == 2025','value':PINK},'value':GREEN}}},
 {'mark':{'type':'text','dx':8,'dy':-12,'align':'left','fontSize':12},'encoding':{'text':{'field':'financial_year'}}}]})
write('13-nursery-value-volume',s)
print('Built 13 Vega / Vega-Lite chart specifications.')
