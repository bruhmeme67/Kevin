# Australia in Bloom

An original, single-page Vega / Vega-Lite data story for **FIT3179 Data Visualisation 2, Semester 2 2026**.

Topic 19: Australian Flowers and Horticulture. This project focuses on **cut flowers, nursery plants and turf**, comparing production, growing regions and international trade through 2024/25.

## GitHub location

This project is in the `australia-in-bloom` folder of [bruhmeme67/Kevin](https://github.com/bruhmeme67/Kevin/tree/main/australia-in-bloom).

Website: https://bruhmeme67.github.io/Kevin/australia-in-bloom/

The repository already uses GitHub Pages. Keep this project folder and its internal relative paths together. The publishing instructions below also explain how to host a separate copy in a new repository.

## What is included

- 13 charts in four sections, including choropleth, proportional-symbol and geographic flow maps.
- Readable JSON specifications in `specs/`, linked below every chart.
- Local data, plotting libraries and font: no CDN or account is needed to load the website after hosting.
- Four useful selectors, hover details and expandable accessible value tables.
- `submission/Submission_Companion.pdf`: What/Why/Who/How, rationale, checks and interview notes.
- `submission/submission-text.md`: editable text to transfer into the unit's Moodle template.
- `submission/Sketch_Layout_Guide.pdf`: a **digital planning guide**, not the required hand-drawn sketch.
- `data/README.md`: sources, units, calculations and limitations.
- `THIRD_PARTY_NOTICES.md`: source and software credits.

## Open the preview

The separate **Australia_in_Bloom.html** deliverable can be downloaded and opened directly in a modern browser. It contains its data and dependencies in one file.

For the repository version, serve this folder using a local web server. For example, if Python is installed:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`. Opening the repository's `index.html` with `file://` may prevent its JSON files from loading; use the standalone preview or a web server.

## Publish on your GitHub account

The brief requires **GitHub Pages**. A local HTML preview is not the submitted URL.

1. Create a **public** repository, for example `australia-in-bloom`.
2. Upload the **contents** of this folder to the repository root. `index.html`, `app.js`, `styles.css`, `specs/`, `data/`, `assets/`, `vendor/` and `submission/` must keep their relative paths. Upload the extracted files, not just the ZIP archive.
3. In the repository, open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select **main**, select **/(root)** and save.
4. Wait for GitHub to display the published URL. Open it in a private/incognito window and check all 13 charts. No sign-in should be required.
5. Add a clear photo/scan of your own hand-drawn A4 sketch as `submission/sketch.pdf`. Confirm that PDF is publicly accessible too. Do not rename the digital guide to pretend it is your hand-drawn sketch.
6. Put your actual website and sketch URLs into the unit's submission template, along with the description in `submission/submission-text.md`.

If the repository is named `australia-in-bloom`, the expected URL pattern is `https://YOUR-USERNAME.github.io/australia-in-bloom/`. This is a pattern, not a deployed link. The sketch URL pattern is `https://YOUR-USERNAME.github.io/australia-in-bloom/submission/sketch.pdf`.

Official GitHub instructions, checked 30 September 2026:

- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Required personal completion

- Confirm the displayed author name (`Kevin`) and replace it with the name you want assessed. A student ID is not required for the public page unless your tutor requests it.
- Compare this page against any sketch you already submitted or received feedback on. That sketch was not supplied with this task, so adherence to it cannot be verified.
- Draw and scan your own A4 sketch. The rubric gives the sketch component **0 if created digitally**. The provided guide helps you plan but does not satisfy this requirement.
- Retain an accurate AI acknowledgement. The page and companion describe ChatGPT's actual assistance; add any further tools or changes you use.
- Understand the design and code for the Week 12 interview. Practice questions are in the companion.
- Transfer the description into the unit's actual Moodle template, which was not supplied.
- Submit by **Sunday 25 October 2026, 11:55 pm**, as stated in the supplied brief. Verify the Moodle timezone and any course updates.

## Implementation

Static HTML/CSS/JavaScript. Vega 5.30.0, Vega-Lite 5.23.0 and Vega-Embed 6.29.0 are bundled locally. No framework, build service, database or API key is needed. `tools/` contains readable scripts for preparing data and chart specifications; Python is only needed if you want to regenerate these files.

`specs/01-sector-treemap.json` uses Vega; the remaining specifications use Vega-Lite. The page's loader replaces local data URLs with cached in-memory values before embedding, avoiding repeated network downloads. The readable originals remain available in the repository.

## Authorship and acknowledgement

Prepared for Kevin with OpenAI ChatGPT assistance in research, data preparation, visual design, coding and writing. All marks and layouts were authored for this project. The original numerical sources and public-domain boundaries are credited; no existing chart graphics were copied. The student must review the work and be able to explain it.
