/* Charts use local, readable specifications. Only chart data is loaded here. */
"use strict";
const chartDefinitions = [
  {id:"01",file:"01-sector-treemap",data:"annual",filter:r=>r.year===2025,
    columns:[["sector","Sector"],["production","Production (A$m)",1]],source:"Hort Innovation, pp. 409, 414, 419."},
  {id:"02",file:"02-production-trend",data:"annual",
    columns:[["sector","Sector"],["financial_year","Year"],["production_index","Index",1]],source:"Hort Innovation, pp. 409, 414, 419; index calculated."},
  {id:"03",file:"03-growth-heatmap",data:"annual",filter:r=>r.year>2021,
    columns:[["sector","Sector"],["financial_year","Year"],["production_yoy_pct","Annual change (%)",1]],source:"Hort Innovation, pp. 409, 414, 419; changes calculated."},
  {id:"04",file:"04-production-choropleth",data:"states",
    columns:[["state","State"],["population","Residents",0],["flower_per_resident","A$ / resident",2]],source:"Hort Innovation, p. 410; ABS Table 4, March 2026 vintage (June 2025 observations)."},
  {id:"05",file:"05-production-symbols",data:"states",
    columns:[["state","State"],["flower_production","Flowers (A$m)",1],["nursery_production","Nursery (A$m)",1]],source:"Hort Innovation, pp. 410, 415. Both sectors shown in the table."},
  {id:"06",file:"06-regional-marimekko",data:"state_mix",
    columns:[["region","Region"],["sector","Sector"],["value","Production (A$m)",1]],source:"Hort Innovation, pp. 410, 415; state values combined as labelled."},
  {id:"07",file:"07-state-roles",data:"state_roles",
    columns:[["state","State"],["production_share","Production share (%)",1],["export_share","Export share (%)",1]],source:"Hort Innovation, pp. 410–411; published percentage shares."},
  {id:"08",file:"08-flower-flow-map",data:"flower_imports",filter:r=>r.year===2025,
    columns:[["country","Origin"],["value","Imports (A$m)",1]],source:"Hort Innovation, p. 411. ‘Others’ appears here but has no map link."},
  {id:"09",file:"09-import-bump",data:"flower_imports",filter:r=>r.country!=="Others",
    columns:[["country","Origin"],["financial_year","Year"],["value","Imports (A$m)",1]],source:"Hort Innovation, p. 411; ranks calculated within the five named origins."},
  {id:"10",file:"10-import-waterfall",data:"import_change",
    columns:[["country","Origin"],["change","Change (A$m)",1]],source:"Hort Innovation, p. 411; year-on-year differences calculated."},
  {id:"11",file:"11-export-destinations",data:"flower_exports",
    columns:[["country","Destination"],["share","Export share (%)",1],["reported_value","Reported A$m"]],source:"Hort Innovation, p. 411; ‘<1’ is preserved as published."},
  {id:"12",file:"12-trade-butterfly",data:"annual",filter:r=>r.sector==="Cut flowers",
    columns:[["financial_year","Year"],["imports","Imports (A$m)",1],["exports","Exports (A$m)",1]],source:"Hort Innovation, p. 409."},
  {id:"13",file:"13-nursery-value-volume",data:"annual",filter:r=>r.sector==="Nursery",
    columns:[["financial_year","Year"],["units_million","Units (million)",0],["production","Value (A$m)",1]],source:"Hort Innovation, p. 414."}
];
const assetCache = new Map();
const chartViews = new Map();
window.chartViews = chartViews; // Exposed for reproducible interaction checks.
window.chartErrors = [];

async function readAsset(path) {
  if (window.INLINE_ASSETS && Object.hasOwn(window.INLINE_ASSETS,path)) return window.INLINE_ASSETS[path];
  if (!assetCache.has(path)) assetCache.set(path,fetch(path).then(response=>{
    if(!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
    return response.json();
  }));
  return assetCache.get(path);
}

async function inlineData(value) {
  if(Array.isArray(value)) return Promise.all(value.map(inlineData));
  if(!value || typeof value!=="object") return value;
  if(typeof value.url==="string" && value.url.startsWith("data/")) {
    let rows=await readAsset(value.url);
    if(value.format?.property) rows=rows[value.format.property];
    const copy={...value,values:rows};
    delete copy.url;
    delete copy.format;
    return copy;
  }
  const entries=await Promise.all(Object.entries(value).map(async([key,item])=>[key,await inlineData(item)]));
  return Object.fromEntries(entries);
}

function element(tag,text,className) {
  const el=document.createElement(tag);
  if(text!==undefined)el.textContent=text;
  if(className)el.className=className;
  return el;
}

async function addChartTools(def) {
  const tools=document.querySelector(`.chart-tools[data-chart="${def.id}"]`);
  const link=element("a","View chart JSON");
  const path=`specs/${def.file}.json`;
  if(window.INLINE_ASSETS) {
    link.href=URL.createObjectURL(new Blob([JSON.stringify(await readAsset(path),null,2)],{type:"application/json"}));
    link.download=`${def.file}.json`;
  } else {link.href=path;link.target="_blank";link.rel="noopener";}
  tools.append(link);
  const details=element("details");
  details.append(element("summary","Read the values"));
  const table=element("table");
  table.setAttribute("aria-label",document.querySelector(`#figure-${def.id} h3`).textContent+" — data table");
  const head=element("thead");const header=element("tr");
  for(const [,label] of def.columns){const th=element("th",label);th.scope="col";header.append(th);}
  head.append(header);table.append(head);
  const body=element("tbody");
  let rows=await readAsset(`data/${def.data}.json`);
  if(def.filter)rows=rows.filter(def.filter);
  for(const row of rows){
    const tr=element("tr");
    for(const [key,,precision] of def.columns){
      const value=row[key];
      const display=value===null||value===undefined?"Not reported":typeof value==="number"?
        value.toLocaleString("en-AU",{minimumFractionDigits:precision??0,maximumFractionDigits:precision??1}):value;
      tr.append(element("td",display));
    }
    body.append(tr);
  }
  table.append(body);details.append(table,element("p",def.source,"table-note"));tools.append(details);
}

async function renderChart(def) {
  const container=document.getElementById(`chart-${def.id}`);
  container.append(element("p","Loading chart…","chart-placeholder"));
  try {
    const original=await readAsset(`specs/${def.file}.json`);
    const spec=await inlineData(original);
    const isVega=spec.$schema.includes("/vega/v");
    if(isVega)spec.width=Math.max(260,container.clientWidth);
    if(def.id==="08")spec.height=Math.max(240,Math.min(445,container.clientWidth*0.43));
    const result=await vegaEmbed(container,spec,{mode:isVega?"vega":"vega-lite",renderer:"svg",actions:false,tooltip:true});
    chartViews.set(def.id,result.view);
    container.querySelector(".chart-placeholder")?.remove();
    let lastWidth=container.clientWidth;
    new ResizeObserver(()=>{
      const nextWidth=container.clientWidth;
      if(Math.abs(nextWidth-lastWidth)>2){
        lastWidth=nextWidth;
        if(def.id==="08")result.view.height(Math.max(240,Math.min(445,nextWidth*0.43)));
        result.view.width(nextWidth).resize().runAsync();
      }
    }).observe(container);
    await addChartTools(def);
  } catch(error) {
    console.error(`Chart ${def.id}`,error);
    window.chartErrors.push({id:def.id,error:String(error)});
    container.replaceChildren(element("p","This chart could not load. Open the project through a web server or use the standalone HTML preview.","chart-error"));
    await addChartTools(def).catch(()=>{});
  }
}

window.chartsReady=Promise.all(chartDefinitions.map(renderChart));
