from pathlib import Path
import os,io,json,math,re,base64,hashlib,zipfile,shutil,argparse
if Path('/workspace/work/fontconfig/fonts.conf').exists(): os.environ.setdefault('FONTCONFIG_FILE','/workspace/work/fontconfig/fonts.conf')
import cairosvg,uharfbuzz as hb
from PIL import Image,ImageDraw,ImageFont,ImageCms
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import fitz
P=argparse.ArgumentParser();P.add_argument('--output',default=str(Path(__file__).resolve().parents[1]));P.add_argument('--font',default=str(Path(__file__).resolve().parents[1]/'fonts/inter-4-variable.ttf'));args=P.parse_args()
OUT=Path(args.output);OUT.mkdir(parents=True,exist_ok=True)
for d in ['svg','pdf','png','favicons','avatar','fonts','source','proofs']: (OUT/d).mkdir(exist_ok=True)
INK='#10243E';BLUE='#0A66D6';LIGHT='#7CC0FF';PAPER='#F3F1EC';CARD='#FDFCFA';RULE='#DED9CF'
LEFT=[(20,14),(41,14),(41,50),(63,50),(63,90),(20,90),(8,78),(8,26)]
RIGHT=[(47,6),(76,6),(88,18),(88,70),(76,82),(69,82),(69,44),(47,44)]
SMALL_LEFT=[(20,14),(39,14),(39,52),(61,52),(61,90),(20,90),(8,78),(8,26)]
SMALL_RIGHT=[(49,6),(76,6),(88,18),(88,70),(76,82),(71,82),(71,42),(49,42)]
COLORS={'color':(INK,BLUE),'reversed':('#FFFFFF',LIGHT),'black':('#000000','#000000'),'white':('#FFFFFF','#FFFFFF')}
font=TTFont(args.font);assert font['name'].getDebugName(5).startswith('Version 4.')
font=instantiateVariableFont(font,{'wght':640,'opsz':32},inplace=True)
fontpath=OUT/'fonts/inter-4-opsz32-wght640.ttf';font.save(fontpath)
if Path(args.font).resolve()!=(OUT/'fonts/inter-4-variable.ttf').resolve(): shutil.copy2(args.font,OUT/'fonts/inter-4-variable.ttf')
lic=Path(args.font).parent/'inter-ofl.txt'
if not lic.exists():lic=Path(args.font).parent/'Inter-OFL.txt'
if lic.exists() and lic.resolve()!=(OUT/'fonts/inter-ofl.txt').resolve():shutil.copy2(lic,OUT/'fonts/inter-ofl.txt')
U=font['head'].unitsPerEm;CAP=font['OS/2'].sCapHeight
gs=font.getGlyphSet();blob=fontpath.read_bytes();face=hb.Face(blob);hf=hb.Font(face);hf.scale=(U,U)
buf=hb.Buffer();buf.add_str('Granite');buf.guess_segment_properties();hb.shape(hf,buf,{'kern':True})
glyphs=[];cursor=0;bounds=[];tracking=-.01*U
for i,(info,pos) in enumerate(zip(buf.glyph_infos,buf.glyph_positions)):
 name=font.getGlyphName(info.codepoint);pen=SVGPathPen(gs);gs[name].draw(pen)
 bp=BoundsPen(gs);gs[name].draw(bp);x=cursor+pos.x_offset;y=pos.y_offset
 glyphs.append((pen.getCommands(),x,y,name))
 if bp.bounds:
  a,b,c,d=bp.bounds;bounds.append((a+x,b+y,c+x,d+y))
 cursor+=pos.x_advance+(tracking if i<len(buf.glyph_infos)-1 else 0)
WB=(min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds))
word_ratio=(WB[2]-WB[0])/CAP

def poly(points):return ' '.join(f'{x},{y}' for x,y in points)
def group(id,body):return f'<g id="{id}" inkscape:groupmode="layer" inkscape:label="{id}">{body}</g>'
def mark_body(stone,disc,prefix='',small=False):
 ids=lambda s:prefix+s
 if small:
  return group(ids('left'),f'<polygon points="{poly(SMALL_LEFT)}" fill="{stone}" opacity=".76"/>')+group(ids('right'),f'<polygon points="{poly(SMALL_RIGHT)}" fill="{stone}" opacity=".76"/>')+group(ids('disc'),f'<circle cx="26" cy="70" r="12" fill="{disc}"/>')
 # Rectangle winding and circle winding are opposite. The ring is true negative
 # space controlled by an editable vector clip, never white paint or a raster mask.
 clip=ids('origin-cutout')
 ring=group(ids('ring'),f'<defs><clipPath id="{clip}" clipPathUnits="userSpaceOnUse"><path d="M0 0H96V96H0Z M38 69A10 10 0 1 0 18 69A10 10 0 1 0 38 69Z" clip-rule="evenodd" fill-rule="evenodd"/></clipPath></defs>')
 return ring+group(ids('left'),f'<polygon points="{poly(LEFT)}" fill="{stone}" clip-path="url(#{clip})"/>')+group(ids('right'),f'<polygon points="{poly(RIGHT)}" fill="{stone}"/>')+group(ids('disc'),f'<circle cx="28" cy="69" r="7" fill="{disc}"/>')
def word_body(cap,xleft,baseline,color,live=False):
 scale=cap/CAP
 if live:
  # xleft is the desired visible ink edge; compensate the glyph sidebearing.
  x=xleft-WB[0]*scale
  return f'<g id="wordmark" inkscape:groupmode="layer" inkscape:label="wordmark"><text x="{x}" y="{baseline}" fill="{color}" font-family="Inter" font-weight="640" font-size="{U*scale}" letter-spacing="{-0.01*U*scale}" style="font-variation-settings: &apos;opsz&apos; 32, &apos;wght&apos; 640; font-optical-sizing:none">Granite</text></g>'
 x=xleft-WB[0]*scale
 paths=''.join(f'<path id="letter-{i+1}-{name}" d="{d}" transform="translate({gx},{gy})"/>' for i,(d,gx,gy,name) in enumerate(glyphs))
 return group('wordmark',f'<g fill="{color}" transform="translate({x},{baseline}) scale({scale},{-scale})">{paths}</g>')
def root(body,vb,title):
 x,y,w,h=vb
 return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="{w:.6f}" height="{h:.6f}" viewBox="{x:.6f} {y:.6f} {w:.6f} {h:.6f}" role="img"><title>{title}</title><metadata>Granite Fault Line. Inter 4; opsz 32; weight 640; tracking -1%. Geometry from supplied coordinates.</metadata>{body}</svg>'''

def asset(layout,variant,live=False):
 stone,accent=COLORS[variant];body=mark_body(stone,accent)
 if layout=='mark':return root(body,(0,0,96,96),'Granite Fault Line symbol'),(0,0,96,96)
 if layout=='horizontal':
  # 84-unit visible symbol height, 28-unit gap, 40-unit cap height.
  cap=40.;x=88+28;baseline=48+(WB[3]+WB[1])*(cap/CAP)/2
  b=(8,6,x+word_ratio*cap,90);vb=(b[0]-20,b[1]-20,b[2]-b[0]+40,b[3]-b[1]+40)
 else:
  cap=24.;ww=word_ratio*cap;x=48-ww/2;baseline=90+24+WB[3]*(cap/CAP)
  b=(min(8,x),6,max(88,x+ww),baseline-WB[1]*(cap/CAP));vb=(b[0]-20,b[1]-20,b[2]-b[0]+40,b[3]-b[1]+40)
 body+=word_body(cap,x,baseline,stone,live)
 return root(body,vb,f'Granite Fault Line {layout} combination logo'),vb

def save_svg_pdf(name,s,vb):
 (OUT/'svg'/f'{name}.svg').write_text(s)
 # A design unit becomes one PDF point; no bitmap content is introduced.
 ss=s.replace(f'width="{vb[2]:.6f}" height="{vb[3]:.6f}"',f'width="{vb[2]:.6f}pt" height="{vb[3]:.6f}pt"',1)
 cairosvg.svg2pdf(bytestring=ss.encode(),write_to=str(OUT/'pdf'/f'{name}.pdf'))
def png(s,path,w,h):
 cairosvg.svg2png(bytestring=s.encode(),write_to=str(path),output_width=w,output_height=h)
 # Write an explicit sRGB profile without adding a matte.
 im=Image.open(path).convert('RGBA');profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes();im.save(path,icc_profile=profile)

assets={}
for layout in ['mark','horizontal','vertical']:
 for variant in COLORS:
  name=f'granite-{layout}-{variant}';s,vb=asset(layout,variant);save_svg_pdf(name,s,vb);assets[name]=(s,vb)
  folder=OUT/'png'/name;folder.mkdir(exist_ok=True)
  for size in [512,1024,2048]:
   scale=size/max(vb[2:]);w=round(vb[2]*scale);h=round(vb[3]*scale)
   png(s,folder/f'{name}-{size}.png',w,h)
for layout in ['horizontal','vertical']:
 s,vb=asset(layout,'color',True);(OUT/'svg'/f'granite-{layout}-live-text.svg').write_text(s)
small=root(group('tile',f'<rect width="96" height="96" rx="20" fill="{INK}"/>')+mark_body('#FFFFFF',LIGHT,small=True),(0,0,96,96),'Granite small-size mark on ink tile')
save_svg_pdf('granite-small-size',small,(0,0,96,96));assets['granite-small-size']=(small,(0,0,96,96))
for size in [16,24,32,48,64,180,192,512]:png(small,OUT/'favicons'/f'favicon-{size}.png',size,size)
(OUT/'favicons'/'favicon.svg').write_text(small)
import struct
icon_sizes=[16,32,48,64];ico_data=[(OUT/'favicons'/f'favicon-{n}.png').read_bytes() for n in icon_sizes];offset=6+16*len(icon_sizes);entries=[]
for n,data in zip(icon_sizes,ico_data):
 entries.append(struct.pack('<BBBBHHII',n,n,0,0,1,32,len(data),offset));offset+=len(data)
(OUT/'favicons'/'favicon.ico').write_bytes(struct.pack('<HHH',0,1,len(entries))+b''.join(entries)+b''.join(ico_data))
shutil.copy2(OUT/'favicons'/'favicon-180.png',OUT/'favicons'/'apple-touch-icon.png')
(OUT/'favicons'/'site.webmanifest').write_text(json.dumps({'name':'Granite','short_name':'Granite','icons':[{'src':'favicon-192.png','sizes':'192x192','type':'image/png'},{'src':'favicon-512.png','sizes':'512x512','type':'image/png'}],'theme_color':INK,'background_color':INK,'display':'standalone'},indent=2))
png(small,OUT/'avatar'/'granite-avatar-1024.png',1024,1024)
# Actual minimum-size raster proofs, distinct from the large production exports.
for variant in COLORS:
 s,vb=assets['granite-mark-'+variant];png(s,OUT/'proofs'/f'mark-{variant}-24.png',24,24)
 s,vb=assets['granite-horizontal-'+variant];png(s,OUT/'proofs'/f'horizontal-{variant}-96.png',96,round(96*vb[3]/vb[2]))

# One-page A3 landscape usage sheet; each logo remains editable vector geometry.
SW,SH=1190.55,841.89;sheet=[]
def rr(x,y,w,h,fill=CARD,stroke='none',r=0):sheet.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')
def txt(s,x,y,size=12,weight=500,color=INK):
 import html
 sheet.append(f'<text x="{x}" y="{y}" font-family="Inter" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(s)}</text>')
def ln(x1,y1,x2,y2,col=BLUE,dash=None):sheet.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{col}" stroke-width=".8" fill="none"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
counter=0
def draw_asset(name,x,y,w,h):
 global counter
 s,vb=assets[name];counter+=1
 inner=s[s.index('</metadata>')+11:s.rindex('</svg>')]
 # Every placed clip and layer ID is unique within the usage-sheet SVG.
 inner=re.sub(r'id="([^"]+)"',lambda m:f'id="s{counter}-{m[1]}"',inner)
 inner=re.sub(r'url\(#([^\)]+)\)',lambda m:f'url(#s{counter}-{m[1]})',inner)
 scale=min(w/vb[2],h/vb[3]);dx=x+(w-vb[2]*scale)/2-vb[0]*scale;dy=y+(h-vb[3]*scale)/2-vb[1]*scale
 sheet.append(f'<g transform="translate({dx},{dy}) scale({scale})">{inner}</g>')
rr(0,0,SW,SH,PAPER)
txt('Granite / Fault Line',32,48,29,700);txt('LOGO USAGE / 01',1158,45,11,600);sheet[-1]=sheet[-1].replace('x="1158"','x="1015"')
txt('Precise. Forensic. Calm. Trustworthy.',32,72,13,500)
# Variation gallery: four colourways, each with symbol and both combinations.
for i,(variant,title) in enumerate([('color','01  Primary'),('reversed','02  Reversed'),('black','03  One-colour black'),('white','04  One-colour white')]):
 x=32+i*285;dark=variant in ['reversed','white'];fg='#FFFFFF' if dark else INK
 rr(x,96,272,276,INK if dark else CARD)
 txt(title,x+16,120,12,600,fg)
 draw_asset('granite-mark-'+variant,x+95,132,82,82)
 draw_asset('granite-horizontal-'+variant,x+10,218,252,81)
 draw_asset('granite-vertical-'+variant,x+91,290,90,73)
# Primary construction / clear space.
txt('Construction & clear space',32,408,19,700)
rr(32,425,552,214,CARD)
# symbol visible bounds at scaled x/y with exact 14-unit exclusion zone.
draw_asset('granite-mark-color',55,447,130,130)
scale=130/96;ix=55+8*scale;iy=447+6*scale;iw=80*scale;ih=84*scale;pad=14*scale
sheet.append(f'<rect x="{ix-pad}" y="{iy-pad}" width="{iw+2*pad}" height="{ih+2*pad}" fill="none" stroke="{BLUE}" stroke-width=".8" stroke-dasharray="3 3"/>')
txt('14 units',77,611,12,600,BLUE)
# horizontal lockup: its exported artboard already contains the 20-unit clear zone.
x,y,w,h=222,454,339,142
draw_asset('granite-horizontal-color',x,y,w,h)
sheet.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{BLUE}" stroke-width=".8" stroke-dasharray="3 3"/>')
txt('20 units around a lockup',265,617,12,600,BLUE)
txt('96 × 96 source grid · 6-unit stepped gap · sharp corners',48,658,12)
txt('Left disc: r7 · negative ring: outer r10 · right piece raised 8',48,677,12)
# Minimum sizes and small-only exception.
txt('Minimum sizes & small-size version',616,408,19,700)
rr(616,425,542,214,CARD)
draw_asset('granite-small-size',640,448,74,74)
txt('Small-size tile',735,462,13,600);txt('10-unit gap · r12 disc · no ring',735,484,12)
txt('White pieces at 76% · #7CC0FF disc',735,506,12)
draw_asset('granite-small-size',642,551,16,16);txt('16 px',674,564,12)
draw_asset('granite-mark-color',748,547,24,24);txt('24 px standard',790,565,12)
# Min horizontal lockup width excludes reserved clear-space margin.
s,vb=assets['granite-horizontal-color'];visible_w=vb[2]-40
# show the full clear-space asset with visible ink width of 96.
fullw=96*vb[2]/visible_w;draw_asset('granite-horizontal-color',640,589,fullw,fullw*vb[3]/vb[2]);txt('96 px horizontal',807,620,12)
txt('Rounded corners are used only on the specified small-size tile.',632,658,12)
txt('The standard symbol and wordmarks keep their sharp geometry.',632,677,12)
# Wordmark and colour specifications, footer compact but complete.
ln(32,703,1158,703,RULE)
txt('Wordmark',32,732,14,700);txt('Inter 4 variable · opsz 32 · weight 640 · tracking −1%',32,753,12)
txt('Horizontal: symbol 84h · cap 40 · gap 28 · vertically centred',32,774,12)
txt('Vertical: cap 24 · gap 24',32,795,12)
txt('Colour rules',616,732,14,700)
txt('Primary #10243E + #0A66D6 on a light ground',616,753,12)
txt('On #10243E: #FFFFFF + #7CC0FF. Never blue #0A66D6 on ink.',616,774,12)
txt('No gradients, effects, extra accents, animals or illustrative motifs.',616,795,12)
usage=root(''.join(sheet),(0,0,SW,SH),'Granite Fault Line one-page usage sheet')
(OUT/'granite-logo-usage.svg').write_text(usage)
physical=usage.replace(f'width="{SW:.6f}" height="{SH:.6f}"',f'width="{SW:.6f}pt" height="{SH:.6f}pt"',1)
cairosvg.svg2pdf(bytestring=physical.encode(),write_to=str(OUT/'granite-logo-usage.pdf'))
png(usage,OUT/'granite-logo-usage.png',1786,1263)

# Pixel proof contact sheet: actual-size icons plus nearest-neighbour enlargements.
board=Image.new('RGB',(1120,410),PAPER);draw=ImageDraw.Draw(board)
ff=ImageFont.truetype(str(fontpath),20)
small16=Image.open(OUT/'favicons'/'favicon-16.png').convert('RGBA')
board.paste(small16,(28,70),small16);board.paste(small16.resize((192,192),Image.Resampling.NEAREST),(28,112))
draw.text((28,25),'16 px / 12× pixels',font=ff,fill=INK)
for i,v in enumerate(COLORS):
 x=270+i*210;dark=v in ['reversed','white'];bg=INK if dark else CARD
 draw.rectangle((x,61,x+184,308),fill=bg)
 im=Image.open(OUT/'proofs'/f'mark-{v}-24.png').convert('RGBA');board.paste(im,(x+8,70),im)
 big=im.resize((168,168),Image.Resampling.NEAREST);board.paste(big,(x+8,118),big)
 draw.text((x,25),v,font=ff,fill=INK)
draw.text((28,352),'Standard proofs: 24 px actual size + 7× pixels. Production assets remain vector.',font=ff,fill=INK)
board.save(OUT/'proofs'/'granite-pixel-checks.png')
meta={'name':'Granite / Fault Line','grid':[96,96],'left':LEFT,'right':RIGHT,'small_left':SMALL_LEFT,'small_right':SMALL_RIGHT,'gap_standard':6,'gap_small':10,'origin_center':[28,69],'origin_disc_radius':7,'origin_cutout_radius':10,'small_origin_center':[26,70],'small_origin_radius':12,'font_version':TTFont(args.font)['name'].getDebugName(5),'weight':640,'optical_size':32,'tracking_em':-.01,'cap_height_font_units':CAP,'horizontal_cap':40,'horizontal_gap':28,'symbol_visible_height':84,'vertical_cap':24,'vertical_gap':24,'wordmark_font_bbox':WB,'clear_space_symbol':14,'clear_space_lockup':20,'minimum_sizes_px':{'small':16,'standard':24,'horizontal':96}}
(OUT/'source'/'geometry.json').write_text(json.dumps(meta,indent=2))
print('Logo assets written:',len(list(OUT.rglob('*'))),'paths',flush=True)
