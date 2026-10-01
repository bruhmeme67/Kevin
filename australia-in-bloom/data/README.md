# Data dictionary and provenance

Prepared for **Australia in Bloom**, 30 September 2026. Sources checked 29 September 2026.

## Scope and sources

The story covers cut flowers, nursery plants and turf, the handbook's “other horticulture” grouping. It does **not** describe the value of all Australian horticulture. All dollar figures are nominal **Australian dollars**, usually millions. A financial year labelled 2024/25 ends on 30 June 2025. Monetary changes do not isolate inflation, product mix, quality or physical output.

### S1. Industry production and trade

**Hort Innovation / Freshlogic by Kynetec (2026), Australian Horticulture Statistics Handbook 2024/25, All Other Horticulture, version 1.0.** This is the latest handbook edition located at the research date.

- [Publisher-hosted PDF mirror](https://prod2.thegoodmoodfood.com.au/globalassets/hort-innovation/australian-horticulture-statistics-handbook/australian-horticulture-statistics-handbook-2024-25-other.pdf)
- [Original indexed publisher PDF URL](https://www.horticulture.com.au/globalassets/hort-innovation/australian-horticulture-statistics-handbook/australian-horticulture-statistics-handbook-2024-25-other.pdf) — the publisher's redesigned site returned 404 at the research date; the publisher-hosted mirror above supplied the document.
- Printed p. 406 (PDF page 3): total other-horticulture five-year series.
- Printed p. 409 (PDF page 6): flower production, exports, imports and wholesale supply, 2020/21–2024/25.
- Printed p. 410 (PDF page 7): flower state production values and published percentage shares.
- Printed p. 411 (PDF page 8): flower import origins, export destinations and state trade shares.
- Printed pp. 413–414 (PDF pages 10–11): nursery methodology and five-year value/unit series. Nursery production value is based on project NY21000, independently of the handbook's THRUchain methodology.
- Printed p. 415 (PDF page 12): nursery state production values.
- Printed p. 419 (PDF page 16): turf five-year production value and area series.

Tables were transcribed into small structured files. All five years use the **same 2024/25 edition**. Published monetary precision and published percentages are retained. International trade data is attributed to **Global Trade Atlas (GTA)** by the handbook; this project accesses it through Hort Innovation, not as an independently downloaded GTA dataset. Source figures are estimates compiled from supply-chain and industry information. No source chart, map, photograph or layout has been reproduced.

### S2. Population, an independent statistical source

**Australian Bureau of Statistics (2026), National, state and territory population, March 2026**, Table 4, Estimated Resident Population, persons, states and territories.

- [Release page](https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/mar-2026)
- [Table 4: 310104.xlsx](https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/mar-2026/310104.xlsx)

Extracted the **June 2025** row from the **latest March 2026 release vintage**. These reference-period observations match the production year. The original workbook date key is `2025-06-01` because it denotes the quarter-ending month; the observations refer to **30 June 2025**. Persons columns were selected, rather than male or female columns. ABS produces population estimates using Census and administrative data. This source is joined to S1 by state name, supplying a denominator for chart 04.

| State | Persons at 30 June 2025 |
|---|---:|
| New South Wales | 8,587,369 |
| Victoria | 7,064,041 |
| Queensland | 5,670,203 |
| South Australia | 1,901,652 |
| Western Australia | 3,044,966 |
| Tasmania | 577,827 |
| Northern Territory | 265,978 |
| Australian Capital Territory | 484,681 |

These are revised figures from the specified vintage, not the preliminary values on the older June 2025 release's headline table. The Australian total includes other territories and is not needed in the state calculations.

### S3. Boundaries and geographic anchors

**Natural Earth**, public-domain map data, obtained from its maintained repository:

- [1:50m admin-1 states and provinces](https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_1_states_provinces.geojson)
- [1:110m countries](https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson)
- [Terms of use](https://www.naturalearthdata.com/about/terms-of-use/)

Australia's eight main states and territories are retained; Jervis Bay and other small offshore territories are omitted. Antarctica is omitted from the world map. Unused properties are dropped and coordinates rounded to 0.001 degrees, sufficient for the display scale. No statistical values are rounded beyond their source precision. Map geometry is not used to infer production.

Country flow endpoints use the source's `LABEL_X` and `LABEL_Y` representative coordinates. Australian proportional symbols use approximate administrative label points, documented in `tools/prepare_data.py`; these are graphic anchors, not measured farms. Some text labels are offset for legibility. Links represent country-to-country trade connections, not ports, aircraft paths or observed routes.

## Files and units

| File | One row / feature represents | Key fields |
|---|---|---|
| `annual.json` / `.csv` | Sector × financial year, 15 rows | `production`, `exports`, `imports`, `wholesale_supply`: A$m; `units_million`: million nursery units; `area_ha`: hectares; `production_index`: 2020/21=100; `production_yoy_pct`: %; `net_imports`: A$m |
| `states.json` / `.csv` | One of eight states/territories | `flower_production`, `nursery_production`: A$m; `population`: persons; `flower_per_resident`: A$/person; published sector shares: % |
| `flower_imports.json` / `.csv` | Origin group × year, 18 rows | `value`: A$m; five named origins plus Others, 2022/23–2024/25 |
| `flower_exports.json` / `.csv` | Export destination group, six rows | `share`: published %; `value`: rounded A$m where numeric; `reported_value`: exact published text, including `<1` |
| `state_roles.json` / `.csv` | Four states with labelled export shares | National production share and national export share, both %; denominators differ |
| `flower_state_imports.json` / `.csv` | State × year, 15 rows | `value`: A$m; supporting source table, not an additional chart |
| `state_mix.json` | Region × sector, 10 rows | Derived Marimekko coordinates in 0–1 units, monetary values and within-region shares |
| `import_change.json` | Origin contribution, plus total | A$m changes and cumulative coordinates for the waterfall |
| `australia.geojson` | State boundary with joined attributes | Geographic geometry + `states.json` fields |
| `world.geojson` | Country boundary | Geometry and country name only |
| `flower_flows.geojson` | Named import origin to Australia | `value`: A$m, 2024/25; LineString endpoints |
| `flow_labels.json` | Source or destination label | Representative coordinates and adjusted text-label coordinates |

CSV source tables are provided for inspection and editing. The website loads only JSON/GeoJSON. JSON `null` becomes an empty CSV cell; it never means zero.

## Calculations

- Production per resident = state flower production in A$m × 1,000,000 / state resident population.
- Production index = annual production value / 2020/21 production value × 100.
- Year-on-year change (%) = (current value / previous value − 1) × 100. The first year has no prior year in this extract, so its annual change is missing.
- Net flower imports = imports − exports. 2024/25: 108.1 − 8.0 = **A$100.1m**.
- Flower import growth = 108.1 − 96.7 = **A$11.4m**. Vietnam's contribution = 18.7 − 9.8 = **A$8.9m**, or **78.1%** of the net rise.
- Five named origins = 22.6 + 20.5 + 18.7 + 15.8 + 12.5 = **A$90.1m**; 90.1/108.1 = **83.3%** of national import value.
- Nursery share of group production = 2757.0/3382.5 = **81.5%**.
- Nursery unit change, 2020/21–2024/25 = (2133/2324 − 1) × 100 = **−8.2%**. Value change = (2757.0/2789.5 − 1) × 100 = **−1.2%**.
- Marimekko widths = region's flower + nursery value / sum for the six included states. Heights = sector value / regional two-sector total. SA and Tasmania are grouped. NT and ACT are excluded because separate flower values are unavailable. Turf is excluded.
- Import ranks are computed among the five named countries for each year, excluding the aggregated Others group.

## Rounding, comparability and exclusions

1. Flowers are reported in money because physical units differ across varieties. The project does not invent stem counts or variety shares.
2. Flower state values sum to A$324.6m, while the published national total is A$324.7m. Preserve both; do not allocate the A$0.1m difference to an unreported territory.
3. Nursery state values sum to A$2756.9m versus a A$2757.0m national total. This is also retained.
4. Named-plus-Other flower imports sum to A$108.0m in 2024/25 and A$96.6m in 2023/24, while national totals are A$108.1m and A$96.7m. The source-rounding residual is A$0.1m in both years, so component changes reconcile to A$11.4m.
5. Published export percentages sum to 99.9%. They are not rescaled. Values reported as `<1` are stored as a range label with a null numeric point estimate. No precise dollar amount is inferred from rounded shares.
6. Gross trade values and production/wholesale values are measured at different supply-chain stages. No chart adds them into a purported physical supply flow or treats their ratio as consumer import reliance.
7. A$452.7m flower wholesale supply is retained in the source table and discussed as context; it is **not** a measured retail-demand series.
8. No claim is made about causal drivers such as climate, wages, shipping costs or consumer preferences. The data describes outcomes.

## Reproduce

From the project directory:

```bash
python tools/prepare_data.py
python tools/build_specs.py
```

The curated input tables are embedded transparently in `prepare_data.py`. To rebuild geography, download the two linked Natural Earth files as `ne-states.json` and `ne-world.json`, then run:

```bash
python tools/prepare_geography.py --source-dir /path/to/downloads
```

No spreadsheet software or Python is needed to view or host the delivered site. Changing a data table may also require updating its narrative annotations. Keep the same measurement definitions and reference years when refreshing the story.
