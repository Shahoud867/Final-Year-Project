(async()=>{
// Local one-time updater for the existing Granite native-text poster.
// Makes no network requests; checks source text and section positions before returning.
const assets = [{"name": "Base", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\" width=\"1620\" height=\"2484\" viewBox=\"0 0 1620 2484\"><rect x=\"0\" y=\"0\" width=\"1620\" height=\"2484\" rx=\"0\" fill=\"#F3F1EC\"/></svg>"}, {"name": "Strata", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\" width=\"1620\" height=\"2484\" viewBox=\"0 0 1620 2484\"><defs><clipPath id=\"strata-left\"><path d=\"M0 0H24V1431H1596V2484H0Z\"/></clipPath><clipPath id=\"strata-right\"><path d=\"M24 0H1620V2484H1596V1431H24Z\"/></clipPath></defs><g clip-path=\"url(#strata-left)\"><rect x=\"0\" y=\"0.0\" width=\"1620\" height=\"496.8\" rx=\"0\" fill=\"#F3F1EC\"/><rect x=\"0\" y=\"496.8\" width=\"1620\" height=\"496.8\" rx=\"0\" fill=\"#EFECE5\"/><rect x=\"0\" y=\"993.6\" width=\"1620\" height=\"496.8\" rx=\"0\" fill=\"#F3F1EC\"/><rect x=\"0\" y=\"1490.4\" width=\"1620\" height=\"496.8\" rx=\"0\" fill=\"#EFECE5\"/><rect x=\"0\" y=\"1987.2\" width=\"1620\" height=\"496.8\" rx=\"0\" fill=\"#F3F1EC\"/></g><g clip-path=\"url(#strata-right)\"><rect x=\"0\" y=\"-14.4\" width=\"1620\" height=\"496.8\" rx=\"0\" fill=\"#F3F1EC\"/><rect x=\"0\" y=\"482.40000000000003\" width=\"1620\" height=\"496.8\" rx=\"0\" fill=\"#EFECE5\"/><rect x=\"0\" y=\"979.2\" width=\"1620\" height=\"496.8\" rx=\"0\" fill=\"#F3F1EC\"/><rect x=\"0\" y=\"1476.0\" width=\"1620\" height=\"496.8\" rx=\"0\" fill=\"#EFECE5\"/><rect x=\"0\" y=\"1972.8\" width=\"1620\" height=\"496.8\" rx=\"0\" fill=\"#F3F1EC\"/></g></svg>"}, {"name": "Fault channel", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\" width=\"1620\" height=\"2484\" viewBox=\"0 0 1620 2484\"><rect x=\"16.8\" y=\"530\" width=\"14.4\" height=\"901\" rx=\"0\" fill=\"#E9E5DC\"/><rect x=\"16.8\" y=\"1423.8\" width=\"1586.4\" height=\"14.4\" rx=\"0\" fill=\"#E9E5DC\"/><rect x=\"1588.8\" y=\"1431\" width=\"14.4\" height=\"913.6999999999998\" rx=\"0\" fill=\"#E9E5DC\"/></svg>"}, {"name": "Evidence thread", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\" width=\"1620\" height=\"2484\" viewBox=\"0 0 1620 2484\"><path d=\"M24 530V1431H1596V2344.7\" stroke=\"#0A66D6\" stroke-width=\"1.44\" stroke-linejoin=\"miter\" stroke-linecap=\"butt\" fill=\"none\"/><circle cx=\"24\" cy=\"558.8\" r=\"2.88\" fill=\"#0A66D6\"/><circle cx=\"24\" cy=\"969.8\" r=\"2.88\" fill=\"#0A66D6\"/><circle cx=\"1596\" cy=\"1445.4\" r=\"2.88\" fill=\"#0A66D6\"/><circle cx=\"1596\" cy=\"1955.2\" r=\"2.88\" fill=\"#0A66D6\"/></svg>"}];
const panels = [["Header", 0, 0, 1620, 530, 0], ["Problem", 36, 558.8, 1548, 376, 5.76], ["Architecture", 36, 969.8, 1548, 446.8, 5.76], ["Evidence", 36, 1445.4, 1548, 461.8, 5.76], ["Plan", 36, 1955.2, 1548, 360.7, 5.76], ["Footer", 0, 2344.7, 1620, 139.3, 0]];
const page=await figma.getNodeByIdAsync('31:2');
if (!page || page.type!=='PAGE') throw new Error('Open the linked Granite Figma file first.');
await figma.setCurrentPageAsync(page);
const poster=await figma.getNodeByIdAsync('31:3');
if (!poster || poster.type!=='FRAME' || Math.abs(poster.width-1620)>.01 || Math.abs(poster.height-2484)>.01) throw new Error('Poster frame 31:3 is missing or has changed dimensions. No changes made.');
const sectionIds=['31:4','31:43','31:57','31:91','31:123','31:146'];
const sections=poster.children.filter(n=>sectionIds.includes(n.id));
if(sections.length!==6) throw new Error('The original six sections have changed. No changes made.');
const texts=poster.findAllWithCriteria({types:['TEXT']});
const snap=()=>JSON.stringify(texts.map(n=>({id:n.id,text:n.characters,font:n.fontName,size:n.fontSize,line:n.lineHeight,spacing:n.letterSpacing,x:n.x,y:n.y,w:n.width,h:n.height,fills:n.fills})));
const before=snap();
const positions=sections.map(n=>({id:n.id,x:n.x,y:n.y,w:n.width,h:n.height}));
const fontMap=new Map();
for(const n of texts) for(const s of n.getStyledTextSegments(['fontName'])) fontMap.set(JSON.stringify(s.fontName),s.fontName);
await Promise.all(Array.from(fontMap.values()).map(f=>figma.loadFontAsync(f)));
// Safe to repeat: replace only this updater's two named background containers.
for(const n of poster.children.filter(n=>['Background','Content panels'].includes(n.name))) n.remove();
function absoluteFrame(name,index){
 const f=figma.createFrame(); f.name=name; f.resize(1620,2484); f.fills=[]; f.clipsContent=false;
 poster.insertChild(index,f);f.layoutPositioning='ABSOLUTE';f.x=0;f.y=0;return f;
}
const background=absoluteFrame('Background',0);
for(const a of assets){ const n=figma.createNodeFromSvg(a.svg);n.name=a.name;background.appendChild(n);n.x=0;n.y=0; }
const content=absoluteFrame('Content panels',1);
for(const [name,x,y,w,h,r] of panels){const n=figma.createRectangle();n.name=name+' panel';content.appendChild(n);n.resize(w,h);n.x=x;n.y=y;n.cornerRadius=r;n.fills=[{type:'SOLID',color:{r:253/255,g:252/255,b:250/255}}];n.strokes=[];}
// Only the two old decorative horizontal rules are superseded by the channel/gap.
for(const n of poster.findAll(n=>n.type==='VECTOR'&&n.width>1500&&n.height<2)){
 const y=n.absoluteTransform[1][2]-poster.absoluteTransform[1][2];
 if(Math.abs(y-1431)<.1 || Math.abs(y-1930)<.1) n.visible=false;
}
poster.name='Granite poster v2.1 · Strata and Fault';
if(snap()!==before) throw new Error('Unexpected text change. Undo this plugin run and report it.');
for(const s of positions){const n=await figma.getNodeByIdAsync(s.id);if(Math.abs(n.x-s.x)>.01||Math.abs(n.y-s.y)>.01||Math.abs(n.width-s.w)>.01||Math.abs(n.height-s.h)>.01)throw new Error('Unexpected section movement. Undo this plugin run.');}
figma.currentPage.selection=[poster];figma.viewport.scrollAndZoomIntoView([poster]);
figma.closePlugin('Strata and Fault applied. '+texts.length+' text layers and all six section layouts preserved.');

})().catch(e=>figma.closePlugin(e.message));
