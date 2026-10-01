# Validation record

Checked on 30 September 2026 against the supplied FIT3179 Data Visualisation 2 brief.

## Completed checks

- All 13 readable chart specifications compile and execute in the bundled Vega/Vega-Lite versions.
- The standalone HTML loads all 13 charts without a web server. The repository version was also tested with HTTP paths using a local-file routing harness; no missing assets or JavaScript errors were reported.
- All 13 chart JSON links and all three data/document links returned successfully in the repository test.
- The four selectors change the intended chart signals: trend sector, production-map sector, import origin and origin ranking. Each chart has an expandable numerical table.
- Page widths of 1366, 1024 and 390 pixels were checked. The page has no horizontal overflow at those widths. Narrow-screen labels were adjusted after visual inspection.
- The three map idioms are a normalised choropleth, proportional symbols and geographic flows. All are implemented in Vega-Lite.
- Checked the group total, nursery share, net flower imports, import-change reconciliation and per-resident calculation. Confirmed the documented A$0.1m rounding differences, missing state values, the 99.9% rounded export-share total and the preserved `<1` values.
- Visually reviewed all six pages of the submission companion and the one-page digital sketch guide after rendering to images. No clipped or overlapping document text was found.
- Data source pages, units, joins, derived calculations and limitations are documented in `data/README.md`. The website includes sources, preparation date and an AI acknowledgement.

## Still requires personal completion

- Publish the repository on the student's public GitHub Pages account and verify the real URL without signing in. This local test is not a production deployment check.
- Draw and scan the student's own A4 sketch. The digital guide is only a planning aid.
- Confirm the author name, check against any previously submitted sketch/tutor feedback and insert the actual URLs into the official Moodle template.
- Review the code and be prepared to explain it in the interview. Chart count does not guarantee a particular rubric classification or mark.
