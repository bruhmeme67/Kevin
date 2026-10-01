"""Generate the submission companion and a clearly labelled digital sketch guide."""
from pathlib import Path
from xml.sax.saxutils import escape
import re
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'submission'
INK=colors.HexColor('#193c32'); GREEN=colors.HexColor('#147d64'); PINK=colors.HexColor('#b63468')
MUTED=colors.HexColor('#566c60'); PALE=colors.HexColor('#eef4ed'); RULE=colors.HexColor('#d6e1d8')
FONT='/usr/share/fonts/truetype/dejavu'
for name,file in [('Body','DejaVuSans.ttf'),('BodyBold','DejaVuSans-Bold.ttf'),('Display','DejaVuSerif.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path(FONT)/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleBloom',fontName='Display',fontSize=29,leading=34,textColor=INK,spaceAfter=18))
styles.add(ParagraphStyle(name='ChapterBloom',fontName='Display',fontSize=21,leading=27,textColor=INK,spaceAfter=14))
styles.add(ParagraphStyle(name='SubBloom',fontName='BodyBold',fontSize=11,leading=15,textColor=INK,spaceBefore=11,spaceAfter=6))
styles.add(ParagraphStyle(name='BodyBloom',fontName='Body',fontSize=9.5,leading=14.2,textColor=INK,spaceAfter=9))
styles.add(ParagraphStyle(name='SmallBloom',fontName='Body',fontSize=8.1,leading=11.4,textColor=MUTED,spaceAfter=7))
styles.add(ParagraphStyle(name='TableBloom',fontName='Body',fontSize=8.0,leading=11,textColor=INK,spaceAfter=0))
styles.add(ParagraphStyle(name='EyebrowBloom',fontName='BodyBold',fontSize=8,leading=12,textColor=PINK,spaceAfter=12))
def clean(s):return s.replace('–','-').replace('—','-').replace('‑','-').replace('’',"'").replace('“','"').replace('”','"')
def p(s,style='BodyBloom'):return Paragraph(clean(s),styles[style])
def table(rows,widths):
    data=[[p(str(c),'TableBloom') for c in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('LINEBELOW',(0,0),(-1,0),0.7,INK),
       ('LINEBELOW',(0,1),(-1,-1),0.4,RULE),('VALIGN',(0,0),(-1,-1),'TOP'),
       ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
       ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    return t
def footer(c,doc):
    c.saveState();c.setStrokeColor(RULE);c.line(42,40,A4[0]-42,40)
    c.setFont('Body',8);c.setFillColor(MUTED)
    c.drawString(42,26,'Australia in Bloom | FIT3179 | 30 September 2026')
    c.drawRightString(A4[0]-42,26,str(doc.page));c.restoreState()

story=[]
story += [p('FIT3179 DATA VISUALISATION 2','EyebrowBloom'),p('Australia in Bloom','TitleBloom'),
 p('Submission companion','ChapterBloom'),
 p('Topic 19: Australian Flowers and Horticulture. Prepared for Kevin, with the AI assistance described in this document.'),
 p('The project delivers a scrolling website with 13 charts, including three different map idioms, plus readable specifications and documented data. This companion explains the design and the remaining personal submission steps.'),
 table([['Deliverable','Where to find it'],
 ['Interactive website','index.html, styles.css and app.js'],
 ['Readable chart specifications','specs/01-sector-treemap.json through specs/13-nursery-value-volume.json'],
 ['Source tables and calculations','data/ and data/README.md; preparation scripts in tools/'],
 ['Text for the Moodle template','submission/submission-text.md'],
 ['Hand-drawn sketch planning','submission/Sketch_Layout_Guide.pdf (digital guide only)'],
 ['Offline preview','Separate Australia_in_Bloom.html deliverable']], [158,353]),
 Spacer(1,13),p('Finish these before submission','SubBloom'),
 p('<b>1.</b> Publish the extracted project on your public GitHub account and verify the page and all chart files without signing in.'),
 p('<b>2.</b> Draw, photograph or scan your own A4 sketch. The rubric gives the sketch component 0 if it was created digitally. The supplied layout guide is not an assessable hand-drawn sketch.'),
 p('<b>3.</b> Confirm your author name, check against any earlier tutor-approved sketch, insert both real URLs into the Moodle template and retain an accurate AI acknowledgement.'),
 p('<b>Due:</b> Sunday 25 October 2026, 11:55 pm, as stated in the supplied specifications. Check Moodle for the applicable timezone and any later course changes.'),
 p('A previous sketch, tutor feedback and the official Moodle template were not supplied. No claim is made that those personal requirements have already been completed.','SmallBloom'),PageBreak()]

story += [p('01 / SUBMISSION DESCRIPTION','EyebrowBloom'),p('Domain, why, who and what','ChapterBloom')]
text=(OUT/'submission-text.md').read_text()
# The main description is also available as a directly editable Markdown file.
part=text.split('## Domain, why and who')[1].split('## How:')[0]
for para in part.strip().split('\n\n'):
    if para.startswith('## '):story.append(p(escape(para[3:]),'SubBloom'))
    else:
        html=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',escape(para))
        story.append(p(html))
story += [PageBreak(),p('02 / DESIGN RATIONALE','EyebrowBloom'),p('How each chart serves the story','ChapterBloom')]
chart_rows=[
 ['01','Treemap','Area shows each sector\'s share of the three-sector production total. Reveals nursery dominance.'],
 ['02','Indexed line','Position compares relative production-value change despite different sector sizes. Selector highlights a sector.'],
 ['03','Heatmap','Diverging colour and signed labels show positive and negative annual changes across sectors and years.'],
 ['04','Choropleth map','Fill encodes production per resident. Combines Hort Innovation and ABS using matching state/year keys.'],
 ['05','Proportional-symbol map','Circle area encodes absolute production. Sector selector contrasts flowers and nursery plants.'],
 ['06','Marimekko','Column width shows regional scale; segment height shows local sector mix; area shows regional sector value.'],
 ['07','Dumbbell','Connected positions compare state shares of national production and national exports. Different shapes reinforce the roles.'],
 ['08','Geographic flow map','Geodesic links locate import connections; width encodes value. Links do not claim actual routes or ports.'],
 ['09','Bump chart','Vertical position shows rank across three years; country highlight makes a changing order easy to follow.'],
 ['10','Waterfall','Floating bars explain how origin-specific changes add to the national import increase.'],
 ['11','Ranked bar','Aligned lengths compare export destination shares precisely. Published shares avoid inventing values below $1m.'],
 ['12','Butterfly','Mirrored bars share a dollar scale and show the persistent import/export imbalance.'],
 ['13','Connected scatter','Two quantitative positions relate nursery units and value. Chronological labels show the path over time.'],
]
story.append(table([['No.','Idiom','Encoding and reader task']]+chart_rows,[30,123,358]))
story += [Spacer(1,11),p('Complexity and originality','SubBloom'),
 p('The design includes eight candidate advanced idioms: treemap, heatmap, choropleth, proportional-symbol map, Marimekko, geographic flow map, bump chart and waterfall. The tutor determines the rubric classification. The other five charts provide simpler comparisons where those are easier to read. A particular mark is not guaranteed by a chart count.','SmallBloom'),
 p('All chart specifications and the narrative layout were authored for this project. Source publications supplied numerical facts, not ready-made chart images.','SmallBloom'),PageBreak()]

story += [p('03 / HOW AND DATA QUALITY','EyebrowBloom'),p('Design decisions and checks','ChapterBloom'),
 p('Four sections move from industry scale to geography, international trade and interpretation of change. All major content remains on one scrollable page. Local data, local plotting libraries and a bundled font reduce external dependencies.'),
 p('Australian maps use an equal-area conic projection adapted to Australia (standard parallels -18° and -36°, central meridian 134°E). The world map uses Equal Earth, centred to keep the trade connections readable. Normalised values use a choropleth; absolute values use proportional symbol area.'),
 p('Pink identifies cut flowers, green nursery plants and ochre turf in sector comparisons. Legends and text identify local trade palettes. Shape distinguishes production from exports in the dumbbell. Headings use Fraunces and body text uses a familiar sans-serif; spacing and alignment establish hierarchy.'),
 p('Selectors support focused comparison. Hover tooltips reveal values; expandable data tables allow readers to inspect numbers without relying on colour or mouse hover. The narrow-screen layout stacks panels. The page includes a skip link, semantic headings and visible focus indicators.'),
 table([['Check','Interpretation'],
 ['Latest relevant periods','Horticulture: 2024/25 handbook; population: June 2025 observations from the March 2026 ABS release.'],
 ['Two independent data sources','Hort Innovation supplies industry values; ABS supplies the population denominator. Geography is a third source.'],
 ['Geographic missing values','Separate flower figures for NT/ACT are unavailable. They are not treated as zero or assigned a share of rounding differences.'],
 ['Different price stages','Production, wholesale supply and international trade value are identified separately. They are not added into a physical supply-flow diagram.'],
 ['Rounding','Flower states total $324.6m versus the $324.7m national figure. Nursery states total $2756.9m versus $2757.0m. Published precision is retained.'],
 ['Small trade values','Exports reported as <1 are kept as ranges. Export share percentages sum to 99.9% due to rounding and are not rescaled.'],
 ['What is not established','The data does not establish climate, cost or consumer-preference causes. Monetary growth does not by itself measure growth in stems or plants.']], [136,375]),
 Spacer(1,10),p('Key reproducible calculations','SubBloom'),
 p('Net flower imports: 108.1 - 8.0 = <b>A$100.1m</b>. Import increase: 108.1 - 96.7 = <b>A$11.4m</b>. Vietnam\'s contribution: (18.7 - 9.8) / 11.4 = <b>78.1%</b>. Nursery share: 2757.0 / 3382.5 = <b>81.5%</b>. Per-resident production: state production (A$m) × 1,000,000 / state population.','SmallBloom'),PageBreak()]

story += [p('04 / PUBLISHING AND PERSONAL REQUIREMENTS','EyebrowBloom'),p('Make the submission accessible','ChapterBloom'),
 p('<b>GitHub Pages.</b> Create a public repository, upload the extracted project contents to its root, then choose Settings > Pages > Deploy from a branch > main > /(root) > Save. Keep index.html, data/, specs/, vendor/ and assets/ at their supplied relative paths. The complete instructions are in README.md.'),
 p('Use the URL GitHub actually displays after publishing. Open it in a private/incognito window and check all 13 charts, selectors, source files and the sketch PDF. An HTML file on your computer or a ZIP file alone does not satisfy the public URL requirement.'),
 p('<b>Sketch.</b> Use the supplied guide to plan an A4 drawing with four clear sections. Include headings, prose positions, all 13 chart positions, three different map idioms, representative marks, axes/legends, colour notes and interactions. Draw it yourself, then scan it to submission/sketch.pdf. If a previous sketch exists, reconcile this design with that sketch and your tutor\'s feedback.'),
 p('<b>Submission template.</b> The exact Moodle template was not provided. Transfer the explanation from submission-text.md, add the actual public webpage and sketch URLs, and confirm the name displayed on the website. Do not invent a Week 7 discussion, approval or feedback record.'),
 p('AI acknowledgement','SubBloom'),
 p('OpenAI ChatGPT assisted with source research, data transcription and preparation, calculations, visual design, Vega/Vega-Lite and website code, narrative writing and supporting documentation. The charts were created for this project from cited numerical data; published chart graphics were not copied. Update this acknowledgement if other tools or assistance are used.'),
 p('Sources and external elements','SubBloom'),
 p('Hort Innovation / Freshlogic by Kynetec (2026). <i>Australian Horticulture Statistics Handbook 2024/25: All Other Horticulture</i>, v1.0, printed pp. 406, 409-411, 413-415, 419. <link href="https://prod2.thegoodmoodfood.com.au/globalassets/hort-innovation/australian-horticulture-statistics-handbook/australian-horticulture-statistics-handbook-2024-25-other.pdf" color="#147d64">Publisher-hosted PDF</link>.','SmallBloom'),
 p('Australian Bureau of Statistics (2026). <i>National, state and territory population, March 2026</i>, Table 4 (310104.xlsx), June 2025 persons observations. <link href="https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/mar-2026" color="#147d64">ABS release and downloads</link>.','SmallBloom'),
 p('Natural Earth. Public-domain 1:50m administrative regions and 1:110m countries. <link href="https://www.naturalearthdata.com/" color="#147d64">Natural Earth</link>. Coordinate precision is reduced for the display scale; observations are not inferred from geography.','SmallBloom'),
 p('Vega 5.30.0, Vega-Lite 5.23.0 and Vega-Embed 6.29.0: BSD 3-Clause licences retained in vendor/. Fraunces: SIL Open Font License retained in assets/. No external photos or decorative image assets are used. Full URLs and notices are in THIRD_PARTY_NOTICES.md and data/README.md.','SmallBloom'),
 p('GitHub setup instructions were checked against <link href="https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site" color="#147d64">GitHub\'s official documentation</link> on 30 September 2026. Industry, population and geography sources were accessed on 29 September 2026.','SmallBloom'),PageBreak()]

story += [p('05 / INTERVIEW PREPARATION','EyebrowBloom'),p('Be ready to explain the choices','ChapterBloom')]
qas=[
 ('What is the main story?','Nursery plants dominate the value of this part of horticulture. Flower production and exporting have different regional concentrations. Import origins are changing, especially Vietnam, while money and physical output can move differently.'),
 ('How does this use two data sources?','Hort Innovation provides state flower production in A$m. ABS provides residents at the matching June 2025 date. A state-name join allows production per resident to be calculated. Natural Earth provides a separate geography layer.'),
 ('Why use two different Australian maps?','The choropleth compares a normalised per-resident value. The symbol map compares absolute dollar totals through circle area. Raw totals as choropleth fill could make a large region appear disproportionately important.'),
 ('What makes the three map idioms different?','Choropleth: colour on areas. Proportional symbols: area of circles at geographic anchors. Flow map: width of links connecting origins to Australia. They support different spatial tasks.'),
 ('Why does the indexed chart start at 100?','Each sector is divided by its own 2020/21 value and multiplied by 100. This removes differences in starting scale. It compares proportional monetary change rather than dollar totals.'),
 ('What does the Marimekko encode?','Column width is the region\'s share of included flower-plus-nursery production. Segment height is the local sector share. Their product makes rectangle area proportional to that region-sector value.'),
 ('Does Queensland export 58.9% of its flowers?','No. Queensland accounts for 58.9% of Australian flower export value. The chart does not measure the fraction of Queensland output exported; production and export shares use different national denominators.'),
 ('How does the waterfall reconcile?','The origin-specific changes sum to $11.4m: 0.0 + 2.7 + 8.9 + 0.3 + 1.8 - 2.3. The rounded component totals differ from national totals by $0.1m in both years, so that residual cancels in the difference.'),
 ('What would you avoid claiming?','That the trade map shows actual shipment routes; that all flower varieties are measured in stems; that wholesale supply equals retail demand; that monetary growth proves volume growth; or that this descriptive data proves a cause.'),
 ('How would you update the page?','Use the next handbook edition consistently, match the population date and vintage, retain missing-value rules, regenerate derived data/specifications and update every narrative annotation. Then check the page and public links again.'),
]
for q,a in qas:
    story.append(KeepTogether([p(q,'SubBloom'),p(a,'SmallBloom')]))
doc=SimpleDocTemplate(str(OUT/'Submission_Companion.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=54,title='Australia in Bloom - Submission Companion',author='Prepared for Kevin with OpenAI ChatGPT assistance')
doc.build(story,onFirstPage=footer,onLaterPages=footer)

# A clean schematic guide, explicitly not a simulated hand-drawn submission.
c=canvas.Canvas(str(OUT/'Sketch_Layout_Guide.pdf'),pagesize=A4)
c.setTitle('Australia in Bloom - Digital Layout Guide for a Hand-drawn Sketch')
c.setAuthor('Prepared for Kevin with OpenAI ChatGPT assistance')
W,H=A4
c.setFillColor(PINK);c.setFont('BodyBold',8);c.drawString(34,H-34,'DIGITAL PLANNING GUIDE - DO NOT SUBMIT AS YOUR HAND-DRAWN SKETCH')
c.setFillColor(INK);c.setFont('Display',22);c.drawString(34,H-66,'Australia in Bloom')
c.setFont('Body',9);c.drawString(34,H-84,'Draw this structure on A4 paper. Add representative marks, axes, legends and notes.')
def box(x,y,w,h,title,detail=None,color=PALE):
    c.setFillColor(color);c.setStrokeColor(RULE);c.roundRect(x,y,w,h,3,fill=1,stroke=1)
    para=Paragraph('<b>'+escape(title)+'</b>'+('<br/>'+escape(detail) if detail else ''),styles['SmallBloom'])
    _,ph=para.wrap(w-16,h-10);para.drawOn(c,x+8,y+h-8-ph)
def label(y,n,title):
    c.setFillColor(PINK);c.setFont('BodyBold',8);c.drawString(34,y,n)
    c.setFillColor(INK);c.setFont('BodyBold',10);c.drawString(60,y,title)
box(34,H-149,527,48,'TITLE + INTRODUCTION + THREE KEY NUMBERS','$3.38bn group production | $324.7m flowers | $100.1m net imports')
label(H-172,'01','THE INDUSTRY: scale, then change')
box(34,H-237,257,53,'01 Treemap','Nursery / flowers / turf; area = value')
box(304,H-237,257,53,'02 Indexed lines','Three sectors; 2020/21 = 100; sector selector')
box(34,H-285,527,36,'03 Heatmap: annual changes','Sector rows, year columns; signed % labels')
label(H-309,'02','THE GROWING REGIONS: totals and regional roles')
box(34,H-379,257,57,'04 Choropleth map','Australia; colour = flower A$ per resident')
box(304,H-379,257,57,'05 Proportional-symbol map','Australia; circle area = value; sector selector')
box(34,H-428,257,37,'06 Marimekko','Width = scale; height = sector mix')
box(304,H-428,257,37,'07 Dumbbell','Production vs export shares of national totals')
label(H-452,'03','THE FLOWER TRADE: origins, changes and destinations')
box(34,H-520,527,56,'08 Geographic flow map','World map; links from five origins to Australia; line width = import value; highlight origin')
box(34,H-569,257,37,'09 Bump chart','Origin ranks over three years')
box(304,H-569,257,37,'10 Waterfall','Origin contributions to the $11.4m rise')
box(34,H-618,527,37,'11 Ranked bars: export destinations','Share of flower export value; show exact percentage labels')
label(H-642,'04','WHAT IS CHANGING: interpret the recovery')
box(34,H-708,257,54,'12 Butterfly','Imports left / exports right; shared A$m scale')
box(304,H-708,257,54,'13 Connected scatter','Nursery units vs value; label each year')
box(34,H-752,527,32,'TAKEAWAYS + SOURCES + AUTHOR + DATE + AI ACKNOWLEDGEMENT')
c.setFont('Body',8);c.setFillColor(MUTED)
c.drawString(34,66,'Use pink for flowers, green for nursery plants, ochre for turf. Mark where hover details appear.')
c.drawString(34,52,'Your sketch should show four clear sections, all chart positions, text, legends and interactions.')
c.drawString(34,38,'If you already submitted a sketch, reconcile the webpage with that sketch and tutor feedback.')
c.save()
print('Created:',OUT/'Submission_Companion.pdf',OUT/'Sketch_Layout_Guide.pdf')
