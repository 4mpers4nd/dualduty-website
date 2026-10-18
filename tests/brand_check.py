"""Asset, palette, and contrast checks for the official brand update (Pillow needed)."""
from pathlib import Path
from PIL import Image,ImageChops
from html.parser import HTMLParser
import json,re
ROOT=Path(__file__).resolve().parents[1]
files={'favicon-16x16.png':16,'favicon-32x32.png':32,'apple-touch-icon.png':180,'icon-192.png':192,'icon-512.png':512,'assets/logo-128.png':128,'assets/logo-256.png':256,'assets/logo-512.png':512}
source=Image.open(ROOT/'assets/brand/official-logo-source.png').convert('RGB')
for name,size in files.items():
 im=Image.open(ROOT/name).convert('RGB');assert im.size==(size,size)
 # This source is square: the whole original must survive exactly as a resize.
 expected=source.resize((size,size),Image.Resampling.LANCZOS)
 # thumbnail and resize may use different reduction paths, so compare to the actual production pipeline.
 expected=source.copy();expected.thumbnail((size,size),Image.Resampling.LANCZOS)
 assert ImageChops.difference(im,expected).getbbox() is None,(name,'changed artwork')
assert Image.open(ROOT/'assets/social.png').size==(1200,630)
assert {(16,16),(32,32),(48,48),(64,64)}<=Image.open(ROOT/'favicon.ico').ico.sizes()
manifest=json.loads((ROOT/'site.webmanifest').read_text())
assert manifest['theme_color']=='#18364A'
for i in manifest['icons']:assert (ROOT/i['src'].lstrip('/')).is_file()
class Head(HTMLParser):
 def __init__(self,text):super().__init__();self.links=[];self.theme=None;self.feed(text)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='link':self.links.append(a.get('href'))
  if t=='meta' and a.get('name')=='theme-color':self.theme=a.get('content')
for p in ROOT.rglob('*.html'):
 d=Head(p.read_text());assert d.theme=='#18364A'
 for ref in ['/favicon.ico','/favicon-32x32.png','/favicon-16x16.png','/apple-touch-icon.png','/site.webmanifest']:assert ref in d.links,(p,ref)
 assert '/assets/logo.svg' not in p.read_text()
css=(ROOT/'assets/style.css').read_text()
for name,value in [('navy','#18364A'),('teal','#147E83'),('white','#F7FAF9'),('mint','#D9E9E5')]:assert f'--brand-{name}: {value}' in css
old=['#2865ff','#ff8a45','#ff7a35','#ff7b36','#3875ff','#518cff','#1243ba','#2061ff']
for p in list(ROOT.rglob('*.html'))+list((ROOT/'assets').glob('*.css'))+list((ROOT/'assets').glob('*.svg'))+list((ROOT/'assets').glob('*.js')):
 assert not any(c in p.read_text().lower() for c in old),(p,'old palette')
def luminance(h):
 rgb=[int(h[i:i+2],16)/255 for i in (1,3,5)]
 rgb=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
 return sum(a*b for a,b in zip(rgb,[.2126,.7152,.0722]))
def contrast(a,b):
 lo,hi=sorted([luminance(a),luminance(b)]);return (hi+.05)/(lo+.05)
pairs=[('Primary button','#FFFFFF','#147E83',4.5),('Body text','#18364A','#F7FAF9',4.5),('Muted text on mint','#526871','#D9E9E5',4.5),('Teal text on mint','#10676B','#D9E9E5',4.5),('Hero/footer text','#D9E9E5','#18364A',4.5),('Input outline','#71858C','#FFFFFF',3),('Focus on white','#147E83','#FFFFFF',3),('Focus on mint','#147E83','#D9E9E5',3)]
for name,a,b,minimum in pairs:
 value=contrast(a,b);assert value>=minimum,(name,value);print(f'{name}: {value:.2f}:1')
print('PASS: logo resize fidelity, favicon sizes, manifest, all-page metadata, obsolete palette scan, and specified contrast pairs.')
