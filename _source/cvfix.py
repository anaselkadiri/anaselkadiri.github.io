import sys, io; sys.path.insert(0,'.')
import pikepdf, cvdump
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Car','/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf'))
SRC='cv_orig_sans_QR.pdf'; OUT='cv_fixed_sans_QR.pdf'
FS=9.5; RIGHT=559.5
def wrap(text, widths):
    words=text.split(' '); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip(); k=min(len(lines),len(widths)-1)
        if pdfmetrics.stringWidth(t,'Car',FS)<=widths[k] or not cur: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def draw(c, x0, ys, text, first_x=None):
    """ys: baselines ; first_x: x de la 1re ligne (sinon x0). justifié sauf dernière ligne"""
    xs=[first_x or x0]+[x0]*(len(ys)-1)
    widths=[RIGHT-x for x in xs]
    lines=wrap(text, widths)
    assert len(lines)<=len(ys), (len(lines), len(ys), text[:40])
    for i,l in enumerate(lines):
        t=c.beginText(xs[i], ys[i]); t.setFont('Car',FS); t.setFillColorRGB(0,0,0)
        if i<len(lines)-1 and ' ' in l:
            extra=(widths[i]-pdfmetrics.stringWidth(l,'Car',FS))/l.count(' ')
            t.setWordSpace(extra)
        t.textOut(l); c.drawText(t)
    return lines
pdf=pikepdf.open(SRC)
REMOVE={0:{10,11,12,13,22,23,30,31,37,59,60}}
pg=pdf.pages[0]; ops=pikepdf.parse_content_stream(pg)
bl={b['mcid']:b for b in cvdump.blocks(pdf,0)}
drop=set()
for m in REMOVE[0]:
    drop.update(range(bl[m]['start'],bl[m]['end']+1))
new=[(o,op) for i,(o,op) in enumerate(ops) if i not in drop]
pg.Contents=pdf.make_stream(pikepdf.unparse_content_stream(new))
buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(595.3,841.89))
out=[]
out+=draw(c,36.1,[704.989,693.389,681.789,670.189],
 "Ingénieur d'État en Réseaux, Systèmes et Sécurité, diplômé de l'ISGA Rabat. Expérience en conception et déploiement d'infrastructures sécurisées : routage avancé (BGP, OSPF, MPLS L3VPN), pare-feu pfSense en haute disponibilité et virtualisation VMware. Complété par la réalisation d'une plateforme SOC (Wazuh, ELK, Suricata), conçue et validée en environnement de test dans le cadre du PFE chez SOFRECOM (Groupe Orange).")
out+=draw(c,49.1,[576.4,564.8],
 "Développé un module de détection par machine learning en Python / FastAPI : classification multi-classes des attaques (Random Forest, 95,3 % d'exactitude en validation croisée 5-fold, données synthétiques) et détection d'anomalies (Isolation Forest).")
out+=draw(c,49.1,[512.4,500.8],
 "Conçu les tableaux de bord Kibana de supervision : KPI sécurité, anomalies détectées par IA, chronologie MITRE ATT&CK et suivi des blocages Active Response.")
out+=draw(c,49.1,[458.4],
 "Réalisé des tests d'intrusion applicatifs (Burp Suite) sur un laboratoire de démonstration isolé (DVWA, Docker).")
out+=draw(c,36.1,[277.8,266.2],
 "SIEM (Wazuh, Elastic Security), IDS / NDR (Suricata, Zeek), pare-feu pfSense en cluster HA (CARP / pfsync), durcissement Linux & Windows, tests d'intrusion (Burp Suite, Nmap), OWASP Top 10, gouvernance & conformité (ISO/IEC 27001:2022)", first_x=75.2)
c.save(); buf.seek(0)
ov=pikepdf.open(buf)
pg.add_overlay(pikepdf.Page(ov.pages[0]))
pdf.save(OUT)
for l in out: print(repr(l))
