"""Produce an offline, single-file preview; source JSON files remain in the project."""
import base64
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'index.html').read_text()
css=(ROOT/'styles.css').read_text()
font=ROOT/'assets/fraunces.woff2'
if font.exists():css=css.replace('assets/fraunces.woff2','data:font/woff2;base64,'+base64.b64encode(font.read_bytes()).decode())
html=html.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>')
for name in ['vega','vega-lite','vega-embed']:
    script=(ROOT/f'vendor/{name}.min.js').read_text().replace('</script','<\\/script')
    html=html.replace(f'<script defer src="vendor/{name}.min.js"></script>','<script>'+script+'</script>')
assets={str(p.relative_to(ROOT)):json.loads(p.read_text()) for folder in ['data','specs']
        for p in (ROOT/folder).iterdir() if p.suffix in ['.json','.geojson']}
bundle=json.dumps(assets,separators=(',',':')).replace('</','<\\/')
script=(ROOT/'app.js').read_text().replace('</script','<\\/script')
html=html.replace('<script defer src="app.js"></script>',
                 '<script>window.INLINE_ASSETS='+bundle+';</script>')
head,sep,tail=html.rpartition('</body>')
html=head+'<script>'+script+'</script>'+sep+tail
for name,mime in [('data/README.md','text/markdown'),('submission/Submission_Companion.pdf','application/pdf'),('submission/Sketch_Layout_Guide.pdf','application/pdf')]:
    p=ROOT/name
    if p.exists():
        url='data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
        html=html.replace('href="'+name+'"','download="'+p.name+'" href="'+url+'"')
out=ROOT.parent/'Australia_in_Bloom.html'
out.write_text(html)
print(str(out),out.stat().st_size)
