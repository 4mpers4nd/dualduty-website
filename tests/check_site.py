"""Dependency-free structural QA for the shipped static site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Doc(HTMLParser):
 def __init__(self,path):
  super().__init__();self.path=path;self.ids=[];self.refs=[];self.h1=0;self.meta={};self.title=False;self.forms=[];self.inputs=[];self.feed(path.read_text())
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t=='h1':self.h1+=1
  if t=='title':self.title=True
  if t=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
  if t in ('a','link','script','img'):
   if a.get('src') or a.get('href'):self.refs.append(a.get('src',a.get('href')))
  if t=='img':assert 'alt' in a, (self.path,'Missing alt')
  if t=='form':self.forms.append(a)
  if t in ('input','textarea','button') and a.get('id','').startswith('preview-'):self.inputs.append(a)
docs={p:Doc(p) for p in ROOT.rglob('*.html')}
refs=0
for p,d in docs.items():
 assert d.h1==1,(p,'h1 count')
 assert d.title and d.meta.get('description'),(p,'missing metadata')
 assert len(d.ids)==len(set(d.ids)),(p,'duplicate IDs')
 assert d.meta.get('og:image','').endswith('/assets/social.png')
 for ref in d.refs:
  u=urlparse(ref)
  if u.scheme or u.netloc:continue
  target=ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)
  if not u.path:target=p
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(p,ref,'missing local target')
  if u.fragment and target in docs:assert u.fragment in docs[target].ids,(p,ref,'missing anchor')
  refs+=1
 for a in d.forms:assert not a.get('action'),(p,'unexpected submission endpoint')
 for a in d.inputs:assert 'disabled' in a,(p,'active personal field')
site=json.loads((ROOT/'data/config.json').read_text())
assert len(site['areas'])==13
assert all(v is False for v in site['features'].values())
assert all(v is None for v in site['pricing']['travelCharges'].values())
assert (ROOT/'CNAME').read_text()=='dualdutyjunk.com\n'
assert (ROOT/'.nojekyll').exists()
urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').findall('.//{*}loc')]
assert len(urls)==8 and len(set(urls))==8
for url in urls:
 assert url.startswith('https://dualdutyjunk.com/')
 assert (ROOT/urlparse(url).path.lstrip('/')/'index.html').exists()
for p in (ROOT/'assets').glob('*.svg'):ET.parse(p)
assert not any('innerHTML' in p.read_text() for p in (ROOT/'assets').glob('*.js'))
print(f'PASS: {len(docs)} HTML pages; {refs} local links/assets/anchors; sitemap; SVG XML; disabled contact fields; initial config.')
