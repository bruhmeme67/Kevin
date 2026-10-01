# Submission description — Australia in Bloom

**Author:** Kevin — confirm your preferred/full submission name.

**Visualisation URL:** https://bruhmeme67.github.io/Kevin/australia-in-bloom/

**Hand-drawn sketch PDF URL:** Insert the verified public URL to your own scanned A4 sketch.

The supplied unit template was not attached. Transfer the relevant text below into that template after completing the two URLs. The digital layout guide is not a substitute for the required hand-drawn sketch.

## Domain, why and who

**Domain.** Australia in Bloom investigates Australian flowers and horticulture, focusing on the Australian Horticulture Statistics Handbook's “other horticulture” group: cut flowers, nursery plants and turf. It compares production value, growing regions and international flower trade through 2024/25. This narrower scope creates a coherent story within topic 19. Fruit, vegetables and nuts are excluded from the group totals.

**Why.** The visualisation helps readers understand the industry behind familiar products such as bouquets and garden plants. It addresses four connected questions: which sector contributes the most value, where production is concentrated, how import origins and export destinations differ, and whether higher monetary value corresponds to more physical output. In Munzner's framework, the principal tasks are to discover trends, compare categories and regions, identify extremes, and understand part-to-whole relationships. The story highlights nursery dominance, the difference between growing and exporting roles, and Vietnam's rising contribution to flower imports.

**Who.** The audience is the average Australian reader, particularly people familiar with buying flowers, gardening or public landscapes. No specialist horticultural or statistical knowledge is assumed. Financial years, index values, production per resident and the difference between wholesale supply and retail spending are explained where needed.

## What: data and preparation

The primary source is **Hort Innovation's Australian Horticulture Statistics Handbook 2024/25**, produced by **Freshlogic by Kynetec**. The Other Horticulture tables provide five-year production and trade comparisons, state production values and flower trading partners. The handbook attributes international trade figures to Global Trade Atlas. The latest handbook edition located at the research date is used throughout, avoiding inconsistent historical vintages.

An independent source, the **Australian Bureau of Statistics' National, state and territory population, March 2026**, provides revised June 2025 estimated resident populations. Those observations match the production year. Joining the sources by state allows flower production value to be compared per resident. Natural Earth supplies public-domain geographic boundaries and representative country coordinates.

The data consists mainly of category-by-year tables, state attributes and origin/destination categories, combined with geographic geometry. Sector, state and country are nominal attributes; financial year is ordered temporal information; monetary values, population and units are quantitative. Existing clean tables were transcribed or extracted into small local JSON/CSV files. Derived fields include growth rates, indices, per-resident values, ranks and component changes. Transformations and source pages are documented in the data dictionary and reproducible scripts. Monetary figures retain source rounding. Missing values remain missing, and “less than $1m” remains a range rather than an invented numeric estimate.

## How: visual design and interaction

Four sections guide readers from industry scale to regional roles, global flower trade and the interpretation of change. Thirteen charts use complementary idioms: a treemap for sector composition; an indexed line chart and heatmap for growth; a choropleth, proportional-symbol map and Marimekko for geography and regional mix; a dumbbell for production versus export shares; a geographic flow map and bump chart for trade connections and rankings; a waterfall for contributions to import growth; a ranked bar chart for export destinations; a butterfly chart for the trade imbalance; and a connected scatter plot for nursery value versus volume.

Australian maps use an equal-area conic projection adapted to Australia. The world map uses Equal Earth. Choropleth colour encodes a normalised per-resident measure, while symbol area encodes absolute production. Flow width represents import value. Position and length support more precise comparisons where appropriate. Pink consistently identifies flowers, green nurseries and ochre turf in sector comparisons. Other palettes are locally labelled.

Selectors highlight sectors and countries or switch the symbol map's production measure. Hover details reveal exact values, and expandable tables provide a non-graphical alternative. All major sections remain visible on one scrolling page. Concise annotations explain key findings and limits. A responsive layout, generous spacing, serif headings and readable body type establish hierarchy. The numerical data and dependencies are stored locally to keep the page small and reliable. Every chart links to its readable Vega or Vega-Lite JSON specification.

## AI acknowledgement

OpenAI ChatGPT was used to assist with source research, data transcription and preparation, calculations, visual design, Vega/Vega-Lite and website code, narrative writing and supporting documentation. The charts were created specifically for this project from the cited numerical data; existing published chart graphics were not copied. Retain this acknowledgement and add any further tools or assistance used. Do not claim a tutor review or a hand-drawn sketch that has not occurred.

## References

1. Hort Innovation / Freshlogic by Kynetec. (2026). *Australian Horticulture Statistics Handbook 2024/25: All Other Horticulture*, version 1.0, pp. 406, 409–411, 413–415, 419. https://prod2.thegoodmoodfood.com.au/globalassets/hort-innovation/australian-horticulture-statistics-handbook/australian-horticulture-statistics-handbook-2024-25-other.pdf
2. Australian Bureau of Statistics. (2026). *National, state and territory population, March 2026*, Table 4, June 2025 persons observations. https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/mar-2026
3. Natural Earth. *Admin-1 states and provinces, 1:50m; countries, 1:110m*. https://www.naturalearthdata.com/

Sources accessed 29 September 2026. Website prepared 30 September 2026.
