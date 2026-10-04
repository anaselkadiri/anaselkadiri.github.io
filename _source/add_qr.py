#!/usr/bin/env python3
"""Génère le QR code du portfolio et l'ajoute au CV (haut à droite de la page 1).

Usage :  python3 add_qr.py https://ton-adresse.github.io
Entrées : assets/CV_Anas_El_Kadiri_sans_QR.pdf  (CV d'origine, sans QR)
Sorties : assets/CV_Anas_El_Kadiri.pdf (CV avec QR, lien cliquable)
          assets/qr-portfolio.png / .svg / .pdf (QR seul)
"""
import io, os, sys
import pikepdf
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.graphics.barcode import qrencoder
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets") if os.path.basename(HERE) == "_source" else os.path.join(HERE, "assets")
URL = (sys.argv[1] if len(sys.argv) > 1 else "https://anaselkadiri.github.io").strip()
DARK = "#0b1f4d"

def matrix(url):
    q = qrencoder.QRCode(None, qrencoder.QRErrorCorrectLevel.M)
    q.addData(url); q.make()
    return q.modules

M = matrix(URL); N = len(M)

def draw(c, x, y, size, quiet=1):
    """dessine le QR en vectoriel : (x, y) = coin bas-gauche, size = côté total (quiet zone comprise)"""
    u = size / (N + 2 * quiet)
    c.setFillColor(white); c.rect(x, y, size, size, stroke=0, fill=1)
    c.setFillColor(HexColor(DARK))
    for r in range(N):
        for k in range(N):
            if M[r][k]:
                c.rect(x + (k + quiet) * u, y + size - (r + quiet + 1) * u, u + .02, u + .02, stroke=0, fill=1)

# --- QR seul : PNG, SVG, PDF
S = 1000; u = S // (N + 2); S = u * (N + 2)
im = Image.new("RGB", (S, S), "white"); d = ImageDraw.Draw(im)
for r in range(N):
    for k in range(N):
        if M[r][k]: d.rectangle([(k + 1) * u, (r + 1) * u, (k + 2) * u - 1, (r + 2) * u - 1], fill=DARK)
im.save(os.path.join(ASSETS, "qr-portfolio.png"))
cells = "".join(f'<rect x="{k+1}" y="{r+1}" width="1.02" height="1.02"/>' for r in range(N) for k in range(N) if M[r][k])
open(os.path.join(ASSETS, "qr-portfolio.svg"), "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {N+2} {N+2}" shape-rendering="crispEdges"><rect width="{N+2}" height="{N+2}" fill="#fff"/><g fill="{DARK}">{cells}</g></svg>')
c = canvas.Canvas(os.path.join(ASSETS, "qr-portfolio.pdf"), pagesize=(300, 300)); draw(c, 0, 0, 300); c.save()

# --- CV : overlay en haut à droite de la page 1
base = os.path.join(ASSETS, "CV_Anas_El_Kadiri_sans_QR.pdf")
out = os.path.join(ASSETS, "CV_Anas_El_Kadiri.pdf")
pdf = pikepdf.open(base)
pg = pdf.pages[0]
W = float(pg.MediaBox[2]); H = float(pg.MediaBox[3])
SZ = 60; X = W - 36 - SZ + 3; Y = H - 20 - SZ        # marge droite ≈ 36 pt
buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(W, H))
draw(c, X, Y, SZ)
c.setFillColor(HexColor(DARK)); c.setFont("Helvetica-Bold", 6.6)
c.drawCentredString(X + SZ / 2, Y - 7, "PORTFOLIO"); c.save()
buf.seek(0)
ov = pikepdf.open(buf)
pg.add_overlay(ov.pages[0])
link = pikepdf.Dictionary(Type=pikepdf.Name.Annot, Subtype=pikepdf.Name.Link, Rect=[X, Y - 10, X + SZ, Y + SZ], Border=[0, 0, 0],
                          A=pikepdf.Dictionary(S=pikepdf.Name.URI, URI=pikepdf.String(URL)))
annots = pg.get("/Annots", None)
if annots is None: pg.Annots = pdf.make_indirect(pikepdf.Array([pdf.make_indirect(link)]))
else: annots.append(pdf.make_indirect(link))
pdf.save(out)
print("QR ajouté au CV pour :", URL)
