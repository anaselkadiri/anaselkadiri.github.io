# -*- coding: utf-8 -*-
"""SOC demo / app « arch » : diagrammes recréés en HTML + CSS + SVG inline (plus d'images).
Les vraies captures restent accessibles via le bouton « shot » de DOC()."""
import html
from demos import DOC

def esc(s): return html.escape(s, quote=False)

# --------------------------------------------------------------------------- helpers SVG
class K:
    """Contexte de génération (langue + préfixe d'ids uniques)."""
    def __init__(self, lang, diag):
        self.i = 0 if lang == "fr" else 1
        self.lang = lang
        self.d = diag
    def t(self, pair):
        return pair if isinstance(pair, str) else pair[self.i]
    def mk(self, kind):
        return "a-%s-%s-%s" % (self.d, self.lang, kind)

def defs(k):
    out = ['<defs>']
    for kind, cls in (("g", "a-mk-g"), ("a", "a-mk-a"), ("r", "a-mk-r"), ("y", "a-mk-y")):
        out.append('<marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" '
                   'markerWidth="9" markerHeight="9" orient="auto"><path class="%s" d="M0,0.5 L10,5 L0,9.5 z"/></marker>'
                   % (k.mk(kind), cls))
    out.append('</defs>')
    return "".join(out)

def txt(x, y, s, cls="a-s", anchor="middle", extra=""):
    return '<text x="%s" y="%s" class="%s" text-anchor="%s"%s>%s</text>' % (x, y, cls, anchor, extra, esc(s))

def box(k, x, y, w, h, title, subs=(), cls="blue", tcls="a-t"):
    """subs : liste de str (sans) ou ('m', str) (mono)."""
    n = len(subs)
    block = 17 + 17 * n
    y0 = y + (h - block) / 2 + 14
    o = ['<g class="a-box a-c-%s"><rect class="a-r" x="%s" y="%s" width="%s" height="%s" rx="9"/>' % (cls, x, y, w, h)]
    o.append(txt(x + w / 2, "%.1f" % y0, k.t(title), tcls))
    for j, sline in enumerate(subs):
        mono = False
        if isinstance(sline, tuple) and sline[0] == "m":
            mono, sline = True, sline[1]
        o.append(txt(x + w / 2, "%.1f" % (y0 + 18 + 17 * j), k.t(sline), "a-s a-m" if mono else "a-s"))
    o.append('</g>')
    return "".join(o)

def line(k, d, kind="g", flow=True, arrow=True, extra_cls=""):
    c = "a-ln" + (" flow" if flow else "") + (" " + extra_cls if extra_cls else "") + (" a-ln-" + kind)
    m = ' marker-end="url(#%s)"' % k.mk(kind) if arrow else ""
    return '<path class="%s" d="%s"%s/>' % (c, d, m)

def svg(k, w, h, body, cls="a-svg"):
    return ('<svg class="%s" viewBox="0 0 %d %d" role="img" xmlns="http://www.w3.org/2000/svg" '
            'preserveAspectRatio="xMidYMin meet">%s%s</svg>' % (cls, w, h, defs(k), body))

# --------------------------------------------------------------------------- 1. pipeline
def pipeline(lang):
    k = K(lang, "pipe")
    X0, W = 134, 666
    o = []
    stages = [
        (29, (("Sources", "Sources"),)),
        (105, (("Collecte &", "Collection &"), ("traitement", "processing"))),
        (183, (("Stockage", "Storage"),)),
        (261, (("Analyse IA", "AI analysis"),)),
        (341, (("Restitution", "Delivery"),)),
    ]
    o.append('<path class="a-rail" d="M13 42 V 328"/>')
    for n, (cy, lab) in enumerate(stages, 1):
        o.append('<circle class="a-dot" cx="13" cy="%d" r="11"/>' % cy)
        o.append(txt(13, cy + 4, str(n), "a-n"))
        for j, l in enumerate(lab):
            off = (-8 if len(lab) == 2 else 0) + j * 15
            o.append(txt(32, cy + 4 + off, k.t(l), "a-stg", "start"))
    srcs = [("Suricata", "EVE JSON"), ("Zeek", "conn, dns logs"), ("Wazuh", ("logs endpoint", "endpoint logs")),
            (("Logs système", "System logs"), "CPU, auth")]
    cw, gap = 153, 18
    cx = []
    for j, (t, s_) in enumerate(srcs):
        x = X0 + j * (cw + gap)
        o.append(box(k, x, 4, cw, 50, t, [("m", k.t(s_))], "warm"))
        cx.append(x + cw / 2)
    for a_, b_ in zip(cx, [250, 390, 540, 680]):
        o.append(line(k, "M%s 56 L%s 77" % (a_, b_)))
    o.append(box(k, 150, 80, 632, 50, ("Filebeat puis Logstash", "Filebeat then Logstash"),
                 [("parsing, normalisation, GeoIP", "parsing, normalization, GeoIP")], "blue"))
    mid = 466
    o.append(line(k, "M%s 132 V 156" % mid))
    o.append(box(k, 296, 158, 340, 50, "Elasticsearch", [("stockage et indexation soc-*", "storage and indexing soc-*")], "blue"))
    o.append(line(k, "M%s 210 V 234" % mid))
    o.append(box(k, 296, 236, 340, 50, ("Module IA (FastAPI)", "AI module (FastAPI)"),
                 [("détection, classification, résumé, prédiction", "detection, classification, summary, prediction")], "purple"))
    o.append(line(k, "M400 288 L 262 314", "a"))
    o.append(line(k, "M532 288 L 670 314", "a"))
    o.append(box(k, X0 + 16, 316, 232, 50, "Kibana", [("tableaux de bord", "dashboards")], "teal"))
    o.append(box(k, 556, 316, 232, 50, "Notifications", [("email, UFW, PDF", "email, UFW, PDF")], "teal"))
    return '<div class="a-wrap">%s</div>' % svg(k, 800, 370, "".join(o))

# --------------------------------------------------------------------------- 2. déploiement
def deployment(lang):
    k = K(lang, "dep")
    o = []
    # hôte / réseau
    o.append('<text x="400" y="14" class="a-hd2" text-anchor="middle">%s</text>' % esc(k.t(("Hôte WSL2 / Ubuntu 22.04", "WSL2 / Ubuntu 22.04 host"))))
    o.append('<rect class="a-zone" x="2" y="22" width="796" height="340" rx="16"/>')
    o.append(txt(400, 44, k.t(("Réseau Docker soc-network (172.20.0.0/16)", "Docker network soc-network (172.20.0.0/16)")), "a-zl"))
    o.append('<rect class="a-zone in" x="10" y="54" width="690" height="298" rx="14"/>')
    bw, bh = 146, 60
    xs = [40, 208, 376, 544]
    r1, r2, r3 = 88, 170, 262
    def cont(x, y, name, ip, port=None, cls="blue"):
        subs = [("m", ip)]
        if port: subs.append(("m", port))
        return box(k, x, y, bw, bh, name, subs, cls)
    o.append(cont(xs[0], r1, "Elasticsearch", "172.20.0.10", ":9200"))
    o.append(cont(xs[1], r1, "Kibana", "172.20.0.11", ":5601"))
    o.append(cont(xs[2], r1, "Logstash", "172.20.0.12", ":5044"))
    o.append(cont(xs[3], r1, "Filebeat", "172.20.0.14"))
    o.append(cont(xs[0], r2, "Wazuh Manager", "172.20.0.13", ":1514 / :1515"))
    o.append(cont(xs[1], r2, "Suricata", "172.20.0.15"))
    o.append(cont(xs[2], r2, "Zeek", "172.20.0.15"))
    o.append(cont(xs[3], r2, "NGINX", "172.20.0.17", ":80"))
    o.append(cont(120, r3, "Python-AI", "172.20.0.16", ":8000", "purple"))
    o.append(cont(330, r3, "Ollama", "172.20.0.19", ":11434", "purple"))
    # flèches
    ymid = r1 + bh / 2
    o.append(line(k, "M%s %s H %s" % (xs[3], ymid, xs[2] + bw + 1)))                    # Filebeat -> Logstash
    o.append(line(k, "M%s %s H %s" % (xs[1], ymid, xs[0] + bw + 1)))                    # Kibana -> Elasticsearch
    o.append(line(k, "M%s %s V 72 H %s V %s" % (xs[2] + bw / 2, r1, xs[0] + bw / 2, r1 - 1)))  # Logstash -> ES (par-dessus)
    bus = 159
    fb = xs[3] + bw / 2
    for x in (xs[0], xs[1], xs[2]):
        o.append(line(k, "M%s %s V %s H %s" % (x + bw / 2, r2, bus, fb), arrow=False))
    o.append(line(k, "M%s %s V %s" % (fb, bus, r1 + bh + 1)))                           # bus -> Filebeat
    o.append(line(k, "M%s %s H 24 V %s H %s" % (xs[0], r1 + bh / 2 + 14, r3 + bh / 2, 120 - 1), "a"))  # ES -> Python-AI
    o.append(line(k, "M%s %s H %s" % (120 + bw, r3 + bh / 2, 330 - 1), "a"))            # Python-AI -> Ollama
    # NGINX -> port 80 / Windows host
    o.append(line(k, "M%s %s H 744" % (xs[3] + bw, r2 + bh / 2), "y"))
    o.append(txt(722, r2 + bh / 2 - 8, "port 80", "a-s", "middle"))
    o.append(txt(752, 250, "Windows", "a-s", "middle"))
    o.append(txt(752, 267, "host", "a-s", "middle"))
    return '<div class="a-wrap">%s</div>' % svg(k, 800, 366, "".join(o))

# --------------------------------------------------------------------------- 3. séquence
def sequence(lang):
    k = K(lang, "seq")
    P = [(100, ("Attaquant", "Attacker")), (300, "Suricata / Zeek"), (500, ("Module IA", "AI module")), (700, "UFW + Email")]
    o = []
    for x, name in P:
        o.append('<rect class="a-ph" x="%d" y="4" width="168" height="34" rx="8"/>' % (x - 84))
        o.append(txt(x, 26, k.t(name), "a-t"))
        o.append('<path class="a-life" d="M%d 38 V 480"/>' % x)
    def msg(i, y, x1, x2, label, d, red=False):
        kind = "r" if red else "g"
        mx = (x1 + x2) / 2
        g = ['<g class="x" style="--d:%ss">' % d]
        g.append('<path class="a-ln a-ln-%s a-sol" d="M%d %d H %d" marker-end="url(#%s)"/>' % (kind, x1, y, x2, k.mk(kind)))
        g.append(txt(mx, y - 9, k.t(label), "a-s a-ms" + (" red" if red else ""), "middle"))
        g.append('</g>')
        return "".join(g)
    def mark(y, x, tlabel, note, d, side="r", mono=False):
        g = ['<g class="x" style="--d:%ss">' % d]
        g.append('<rect class="a-tag" x="%d" y="%d" width="52" height="22" rx="6"/>' % (x - 26, y - 15))
        g.append(txt(x, y, tlabel, "a-tg"))
        if note:
            if side == "r": g.append(txt(x + 38, y, k.t(note), "a-s a-nt" + (" a-m" if mono else ""), "start"))
            else:           g.append(txt(x - 38, y, k.t(note), "a-s a-nt" + (" a-m" if mono else ""), "end"))
        g.append('</g>')
        return "".join(g)
    o.append(msg(1, 74, 100, 300, ("T+0s exfiltration 45 Mo", "T+0s exfiltration 45 MB"), 0.3, False))
    o.append(mark(112, 300, "T+8s", ("Alerte EVE JSON indexée", "EVE JSON alert indexed"), 0.9))
    o.append(msg(2, 150, 300, 500, ("requête /detect", "/detect request"), 1.4))
    o.append(mark(190, 500, "T+35s", ("Score anomalie 0,849", "Anomaly score 0.849"), 2.0))
    o.append(msg(3, 226, 500, 700, ("alerte critique", "critical alert"), 2.5, True))
    o.append(mark(268, 700, "T+42s", ("Email envoyé à l'analyste", "Email sent to the analyst"), 3.1, "l"))
    o.append(mark(302, 700, "T+58s", "ufw insert deny from IP", 3.7, "l", True))
    o.append(msg(4, 346, 700, 100, ("trafic bloqué dès T+60s", "traffic blocked from T+60s"), 4.2, True))
    o.append(mark(388, 700, "T+24h", ("Déblocage automatique UFW", "Automatic UFW unblock"), 5.0, "l"))
    # bilan
    g = ['<g class="x" style="--d:5.6s"><rect class="a-sum" x="30" y="408" width="740" height="76" rx="12"/>']
    g.append('<text class="a-sl" x="60" y="434">%s <tspan class="a-hl">%s</tspan></text>' % (
        esc(k.t(("Temps total détection → blocage :", "Total detection → block time:"))), esc(k.t(("58 secondes", "58 seconds")))))
    g.append(txt(60, 454, k.t(("MTTD moyen approche classique (règles statiques) : 120 secondes",
                                                "Mean MTTD, classic approach (static rules): 120 seconds")), "a-sl", "start"))
    g.append('<text class="a-sl" x="60" y="474">%s <tspan class="a-hl">%s</tspan></text>' % (
        esc(k.t(("Réduction mesurée :", "Measured reduction:"))), esc(k.t(("51,7 %", "51.7%")))))
    g.append('</g>')
    o.append("".join(g))
    return '<div class="a-wrap a-seq">%s</div>' % svg(k, 800, 492, "".join(o))

# --------------------------------------------------------------------------- 4. classes UML
def uml_card(name, attrs, methods, cls="a-c-blue", two=False):
    def rows(items):
        return "".join('<li><i>%s</i>%s</li>' % (esc(v), esc(rest)) for v, rest in items)
    a = '<ul class="a-attr">%s</ul>' % rows(attrs) if attrs else ""
    return ('<div class="a-uml %s%s"><div class="a-un">%s</div>%s<ul class="a-meth%s">%s</ul></div>'
            % (cls, " a-router" if two else "", esc(name), a, " a-two" if two else "", rows(methods)))

def classes(lang):
    k = K(lang, "cls")
    P, M = "+", "–"
    router = uml_card("FastAPIRouter", [(M, " es_client : Elasticsearch")],
                      [(P, " health()"), (P, " detect(minutes)"), (P, " classify(minutes)"),
                       (P, " summarize_llm(alerts)"), (P, " predict(hours)"), (P, " stats()")], "a-c-teal", True)
    ad = uml_card("AnomalyDetector", [(M, " model : IsolationForest"), (M, " scaler : StandardScaler")],
                  [(P, " train(events)"), (P, " detect(events)"), (P, " extract_features(events)")], "a-c-blue")
    ac = uml_card("AttackClassifier", [(M, " model : RandomForestClassifier"), (M, " label_encoder : LabelEncoder")],
                  [(P, " train(X, y)"), (P, " classify(events)"), (P, " feature_importance()")], "a-c-purple")
    isum = uml_card("IncidentSummarizer", [(M, " ollama_url : str"), (M, ' model_name : str = "llama3.2:3b"')],
                    [(P, " summarize(alerts)"), (P, " fallback_summary(alerts)")], "a-c-warm")
    arrows = "".join(line(k, "M%s 2 L%s 52" % (x1, x2), "g", False) for x1, x2 in ((340, 128), (400, 400), (460, 672)))
    s = svg(k, 800, 56, arrows, "a-svg a-arr")
    return ('<div class="a-wrap"><div class="a-uml-wrap">%s%s<div class="a-uml-row">%s%s%s</div></div></div>'
            % (router, s, ad, ac, isum))

# --------------------------------------------------------------------------- 5. architecture globale
def architecture(lang):
    k = K(lang, "arch")
    o = []
    cx = 400
    # chaîne hôte
    o.append(box(k, 325, 4, 150, 38, "Internet", [], "gray"))
    o.append(line(k, "M%s 44 V 70" % cx))
    o.append(box(k, 270, 72, 260, 52, ("NAT WSL2 (Windows)", "WSL2 NAT (Windows)"), [("m", "172.17.99.237/20")], "blue"))
    o.append(line(k, "M%s 126 V 152" % cx))
    o.append(box(k, 235, 154, 330, 56, ("Firewall UFW (hôte)", "UFW firewall (host)"),
                 [("Deny par défaut, ports SOC autorisés", "Default deny, SOC ports allowed")], "red"))
    o.append(line(k, "M%s 212 V 238" % cx))
    o.append(box(k, 235, 240, 330, 56, ("Suricata + Zeek (coupure)", "Suricata + Zeek (inline cut)"),
                 [("IDS/IPS réseau, capture passive", "Network IDS/IPS, passive capture")], "warm"))
    o.append(txt(225, 272, "eth0 (WAN)", "a-s", "end"))
    o.append(txt(575, 272, "br0 (Docker)", "a-s", "start"))
    # flèches vers les zones
    o.append(line(k, "M300 298 V 330", "g"))
    o.append(txt(312, 318, k.t(("Filebeat · Syslog / EVE JSON (logs IDS)", "Filebeat · Syslog / EVE JSON (IDS logs)")), "a-s a-nt", "start"))
    o.append(line(k, "M530 298 L 640 336 ", "g"))
    # zone interne
    o.append('<rect class="a-zone" x="4" y="334" width="546" height="524" rx="16"/>')
    o.append(txt(22, 362, k.t(("Réseau interne (Administration SOC)", "Internal network (SOC administration)")), "a-zt", "start"))
    o.append(txt(22, 382, k.t(("172.20.0.0/16 — soc-network (Docker)", "172.20.0.0/16 — soc-network (Docker)")), "a-s", "start"))
    c1, c2, cw = 34, 288, 230
    ys = [404, 490, 576, 672]
    bh = 54
    o.append(box(k, c1, ys[0], cw, bh, "Logstash", [("Parsing, GeoIP", "Parsing, GeoIP")], "blue"))
    o.append(box(k, c2, ys[0], cw, bh, "Wazuh Manager", [("m", "172.20.0.13")], "blue"))
    o.append(box(k, c1, ys[1], cw, bh, "Elasticsearch", [("m", "172.20.0.10")], "blue"))
    o.append(box(k, c2, ys[1], cw, bh, "Kibana", [("m", "172.20.0.11")], "blue"))
    o.append(box(k, c1, ys[2], cw, 62, ("Module IA (Python)", "AI module (Python)"),
                 [("Isolation + Random Forest", "Isolation + Random Forest"), ("m", "FastAPI :8000")], "purple"))
    o.append(box(k, c2, ys[2], cw, 62, "Ollama LLM", [("llama3.2:3b local", "llama3.2:3b local"), ("m", "172.20.0.19")], "purple"))
    o.append(box(k, c1, ys[3], cw, 62, "Active Response", [("m", "ufw deny from IP"), ("si score >= 0.85", "if score >= 0.85")], "red"))
    o.append(box(k, c2, ys[3], cw, 62, ("Notification email", "Email notification"), [("m", "Gmail SMTP"), ("si critical/high", "if critical/high")], "yellow"))
    yb = 772
    o.append(box(k, c1, yb, 484, 56, "soc-blocked-ips (Elasticsearch)",
                 [("Traçabilité, déblocage auto après 24h", "Traceability, automatic unblock after 24h")], "gray"))
    # flèches internes (sens du flux)
    o.append(line(k, "M%s %s H %s" % (c2, ys[0] + 27, c1 + cw + 1), "g"))                 # Wazuh -> Logstash
    o.append(line(k, "M%s %s V %s" % (c1 + 115, ys[0] + bh, ys[1] - 1)))                  # Logstash -> ES
    o.append(line(k, "M%s %s H %s" % (c2, ys[1] + 27, c1 + cw + 1)))                      # Kibana -> ES
    o.append(line(k, "M%s %s V %s" % (c1 + 115, ys[1] + bh, ys[2] - 1), "a"))             # ES -> IA
    o.append(line(k, "M%s %s H %s" % (c1 + cw, ys[2] + 31, c2 - 1), "a"))                 # IA -> Ollama
    o.append(line(k, "M%s %s V %s" % (c1 + 115, ys[2] + 62, ys[3] - 1), "a"))             # IA -> Active Response
    o.append(line(k, "M%s %s L %s %s" % (c1 + cw - 20, ys[2] + 62, c2 + 24, ys[3] - 1), "a"))  # IA -> Notification
    o.append(line(k, "M%s %s V %s" % (c1 + 115, ys[3] + 62, yb - 1), "g"))
    o.append(txt(c1 + 126, yb - 8, k.t(("historise", "logs")), "a-s a-nt", "start"))
    # commande ufw (pointillés rouges) : Active Response -> UFW
    o.append(line(k, "M%s %s H 18 V 182 H 234" % (c1, ys[3] + 31), "r"))
    o.append(txt(32, 174, k.t(("commande ufw insert deny", "ufw insert deny command")), "a-s a-red", "start"))
    # zone cible
    o.append('<rect class="a-zone" x="570" y="334" width="226" height="524" rx="16"/>')
    o.append(txt(588, 362, k.t(("Zone cible / attaquant", "Target / attacker zone")), "a-zt", "start"))
    o.append(txt(588, 382, k.t(("192.168.56.0/24 (simulé)", "192.168.56.0/24 (simulated)")), "a-s", "start"))
    o.append(box(k, 584, 404, 198, 62, ("Serveur cible (DVWA)", "Target server (DVWA)"), [("m", "192.168.56.10")], "blue"))
    o.append(box(k, 584, 504, 198, 76, ("Machine attaquante", "Attacker machine"),
                 [("Ubuntu (nmap, hydra)", "Ubuntu (nmap, hydra)"), ("m", "192.168.56.100")], "warm"))
    o.append(line(k, "M683 502 V 468", "r"))
    o.append('<rect class="a-ghost" x="584" y="604" width="198" height="54" rx="9"/>')
    o.append(txt(683, 627, k.t(("Bloqué par UFW", "Blocked by UFW")), "a-s", "middle"))
    o.append(txt(683, 645, k.t(("après détection IA", "after AI detection")), "a-s", "middle"))
    hd = ('<div class="a-hd"><b>%s</b><span>%s</span></div>' % (
        esc(k.t(("Environnement de test — SOC PFE", "Test environment — SOC PFE"))),
        esc(k.t(("WSL2 / Ubuntu 22.04 — Docker Compose, sans VM", "WSL2 / Ubuntu 22.04 — Docker Compose, no VM")))))
    leg_items = [("blue", ("Collecte et stockage", "Collection and storage")), ("warm", ("Détection / cible", "Detection / target")),
                 ("purple", ("Intelligence artificielle", "Artificial intelligence")), ("yellow", ("Notification", "Notification")),
                 ("red", ("Firewall / réponse auto", "Firewall / auto response"))]
    leg = '<div class="a-leg">%s</div>' % "".join('<span><i class="a-sw a-c-%s"></i>%s</span>' % (c, esc(k.t(t))) for c, t in leg_items)
    return '<div class="a-wrap">%s%s%s</div>' % (hd, svg(k, 800, 868, "".join(o)), leg)

# --------------------------------------------------------------------------- apply
def apply(demo):
    app = next(a for a in demo["apps"] if a["id"] == "arch")
    old = app["tabs"]
    lab = lambda j: old[j]["label"]
    cap = [
        ("Des sources (Suricata, Zeek, Wazuh, logs système) à la restitution (Kibana, notifications).",
         "From sources (Suricata, Zeek, Wazuh, system logs) to delivery (Kibana, notifications)."),
        ("Réseau Docker soc-network (172.20.0.0/16) sur hôte WSL2 / Ubuntu 22.04.",
         "Docker network soc-network (172.20.0.0/16) on a WSL2 / Ubuntu 22.04 host."),
        ("Diagramme de séquence : exfiltration détectée puis IP bloquée en 58 secondes.",
         "Sequence diagram: exfiltration detected, then IP blocked in 58 seconds."),
        ("Classes de l'API : AnomalyDetector, AttackClassifier, IncidentSummarizer.",
         "API classes: AnomalyDetector, AttackClassifier, IncidentSummarizer."),
        ("Architecture globale par couches de l'environnement de test.",
         "Layered global architecture of the test environment."),
    ]
    gens = [(pipeline, "soc-13-pipeline.png"), (deployment, "soc-14-deployment.png"), (sequence, "soc-15-sequence.png"),
            (classes, "soc-16-api-classes.png"), (architecture, "soc-12-architecture.png")]
    app["tabs"] = [DOC(lab(j), g("fr"), g("en"), shot=f, cap=cap[j]) for j, (g, f) in enumerate(gens)]
