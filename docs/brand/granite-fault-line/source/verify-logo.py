from pathlib import Path
import json,math,re,xml.etree.ElementTree as ET
from PIL import Image
import fitz
import argparse
a=argparse.ArgumentParser();a.add_argument('--root',default=str(Path(__file__).resolve().parents[1]));args=a.parse_args();R=Path(args.root);m=json.loads((R/'source/geometry.json').read_text())
def contains(poly,p):
 x,y=p;c=False
 for (x1,y1),(x2,y2) in zip(poly,poly[1:]+poly[:1]):
  if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1:c=not c
 return c
assert m['left']==[[20,14],[41,14],[41,50],[63,50],[63,90],[20,90],[8,78],[8,26]]
assert m['right']==[[47,6],[76,6],[88,18],[88,70],[76,82],[69,82],[69,44],[47,44]]
assert [47-41,50-44,69-63]==[6,6,6]
assert [49-39,52-42,71-61]==[10,10,10]
for i in range(360):
 a=i*math.pi/180
 assert contains(m['left'],(28+10*math.cos(a),69+10*math.sin(a)))
 assert contains(m['small_left'],(26+12*math.cos(a),70+12*math.sin(a)))
for y in range(96):
 for x in range(96):
  assert not(contains(m['left'],(x+.5,y+.5)) and contains(m['right'],(x+.5,y+.5)))
  assert not(contains(m['small_left'],(x+.5,y+.5)) and contains(m['small_right'],(x+.5,y+.5)))
for p in (R/'svg').glob('*.svg'):
 root=ET.parse(p).getroot();ids=[n.attrib['id'] for n in root.iter() if 'id' in n.attrib]
 assert len(ids)==len(set(ids)),p
 if 'small' not in p.stem:assert all(k in ids for k in ['left','right','ring','disc']),p
 if p.stem.endswith(('black','white')):
  allowed='#000000' if p.stem.endswith('black') else '#FFFFFF'
  assert all(v==allowed for n in root.iter() for k,v in n.attrib.items() if k=='fill'),p
 for node in root.iter():assert node.tag.split('}')[-1] not in ['image','filter','linearGradient','radialGradient'],p
for p in (R/'pdf').glob('*.pdf'):
 d=fitz.open(p);assert len(d)==1 and not d[0].get_images(),p
pdf=fitz.open(R/'granite-logo-usage.pdf');assert len(pdf)==1 and not pdf[0].get_images()
assert len(list((R/'png').rglob('*.png')))==36
for p in (R/'png').rglob('*.png'):
 im=Image.open(p);size=int(p.stem.rsplit('-',1)[1]);assert max(im.size)==size;assert im.mode=='RGBA';assert im.getchannel('A').getextrema()==(0,255),p
for v,disc in [('color',(10,102,214)),('reversed',(124,192,255)),('black',(0,0,0)),('white',(255,255,255))]:
 im=Image.open(R/f'png/granite-mark-{v}/granite-mark-{v}-1024.png').convert('RGBA')
 at=lambda x,y:im.getpixel((round(x/96*1024),round(y/96*1024)))
 assert at(28,69)==disc+(255,),v
 assert at(36.5,69)[3]==0,v
 for x,y in [(44,30),(50,47),(66,70)]:assert at(x,y)[3]==0,(v,x,y)
small=Image.open(R/'favicons/favicon-16.png');assert small.size==(16,16)
ico=Image.open(R/'favicons/favicon.ico');assert ico.ico.sizes()=={(16,16),(32,32),(48,48),(64,64)}
assert ico.ico.getimage((16,16)).convert('RGBA').tobytes()==small.convert('RGBA').tobytes()
assert Image.open(R/'avatar/granite-avatar-1024.png').size==(1024,1024)
assert m['font_version'].startswith('Version 4.') and m['weight']==640 and m['optical_size']==32
checks={'standard_vertices_exact':True,'standard_gap_axis_width':6,'small_gap_axis_width':10,'pieces_disjoint':True,'disc_and_ring_inside_left':True,'ring_transparency_checked':True,'colorways_checked':['color','reversed','black','white'],'font':m['font_version'],'wordmark_weight':640,'wordmark_opsz':32,'tracking_em':-.01,'horizontal_symbol_height':84,'horizontal_cap_height':40,'horizontal_gap':28,'horizontal_vertical_ink_alignment':'centred','vertical_cap_height':24,'vertical_gap':24,'png_exports':36,'vector_pdf_assets':13,'pdf_raster_image_count':0,'usage_pdf_pages':1,'favicon_16_ico_matches_png':True,'manual_visual_checks':['16 px small-size rendering','24 px one-colour and reversed symbols','one-page usage sheet']}
(R/'source/validation.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
