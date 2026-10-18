#!/usr/bin/env python3
"""Maintenance-only asset resizing. Requires Pillow; deployment requires no build."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
ROOT=Path(__file__).resolve().parents[1]
source=Image.open(ROOT/'assets/brand/official-logo-source.png').convert('RGB')
# Fit the entire supplied square artwork. No redraw, trace, recolor, crop or skew.
def icon(size):
 out=Image.new('RGB',(size,size),'white')
 copy=source.copy();copy.thumbnail((size,size),Image.Resampling.LANCZOS)
 out.paste(copy,((size-copy.width)//2,(size-copy.height)//2))
 return out
for name,size in [('assets/logo-128.png',128),('assets/logo-256.png',256),('assets/logo-512.png',512),('favicon-16x16.png',16),('favicon-32x32.png',32),('apple-touch-icon.png',180),('icon-192.png',192),('icon-512.png',512)]:
 icon(size).save(ROOT/name,optimize=True)
icon(64).save(ROOT/'favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
manifest={'name':'Dual Duty Junk Removal','short_name':'Dual Duty','id':'/','start_url':'/','scope':'/','display':'standalone','background_color':'#F7FAF9','theme_color':'#18364A','description':'Pre-launch junk removal in Sanpete County, Utah.','icons':[{'src':'/icon-192.png','sizes':'192x192','type':'image/png','purpose':'any'},{'src':'/icon-512.png','sizes':'512x512','type':'image/png','purpose':'any'}]}
(ROOT/'site.webmanifest').write_text(json.dumps(manifest,indent=2)+'\n')
# The social composition uses the supplied mark directly inside a white tile.
im=Image.new('RGB',(1200,630),'#18364A');d=ImageDraw.Draw(im)
fontpath='/usr/share/fonts/truetype/dejavu/'
def font(size,bold=False):return ImageFont.truetype(fontpath+('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'),size)
d.rectangle((0,0,1200,10),fill='#147E83')
d.text((62,62),'DUAL DUTY',font=font(35,True),fill='#F7FAF9')
d.text((65,110),'J U N K  R E M O V A L',font=font(14),fill='#D9E9E5')
d.text((58,215),'YOUR JUNK.',font=font(63,True),fill='#F7FAF9')
d.text((58,290),'OUR DUTY.',font=font(63,True),fill='#D9E9E5')
d.text((64,402),'Locally founded. Getting ready.',font=font(22),fill='#D9E9E5')
d.rounded_rectangle((780,145,1125,490),radius=8,fill='#147E83')
im.paste(icon(320),(768,130))
d.line((64,531,1134,531),fill='#147E83',width=2)
d.text((64,565),'PRE-LAUNCH / SANPETE COUNTY, UTAH',font=font(15,True),fill='#D9E9E5')
d.text((930,565),'dualdutyjunk.com',font=font(17),fill='#F7FAF9')
im.save(ROOT/'assets/social.png',optimize=True)
print('Generated faithful logo sizes, full favicon package, manifest, and social card.')
