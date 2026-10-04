# -*- coding: utf-8 -*-
"""Recreated UIs (HTML/CSS) for the SOC demo: Kibana dashboards, alert e-mail, PDF report, docker/ufw terminals.
apply(demo) swaps the corresponding IMG tabs in place. Styles: ui_soc.css (all selectors prefixed `.pc .k-`)."""
import os, random
from demos import DOC, TERM, C, O

# ------------------------------------------------------------------ helpers
KG = "#54b399"  # Kibana default series colour


def pct(v, mx):
    return "%.2f%%" % (v / mx * 100)


def kpanel(title, body, style="", badge=None, pb=""):
    b = '<em>%s</em>' % badge if badge else ""
    return ('<div class="k-p" style="%s"><div class="k-ph"><span class="k-t">%s%s</span>'
            '<span class="k-dots"><i></i><i></i><i></i></span></div><div class="k-pb" %s>%s</div></div>') % (
        style, title, b, pb, body)


def grid(cols, *panels, extra=""):
    return '<div class="k-g" style="grid-template-columns:%s;%s">%s</div>' % (cols, extra, "".join(panels))


def nav(dash):
    mag = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round">'
           '<circle cx="7" cy="7" r="5"/><path d="M11 11l3.5 3.5"/></svg>')
    return ('<div class="k-nav"><span class="k-av">D</span><span class="k-crumb"><b>Dashboard</b><span>Editing %s</span></span>'
            '<span class="k-q">%s<em>Filter your data using KQL syntax</em></span>'
            '<span class="k-pill">Last 90 days</span><span class="k-pill">10 s</span>'
            '<span class="k-btn o">Refresh</span></div>') % (dash, mag)


def wrap(inner, dash):
    return '<div class="k-wrap">%s%s</div>' % (nav(dash), inner)


def hbars(rows, maxv, ticks, lw, xlabel, ylabel=None, rh=15):
    """rows: (label, value) ; ticks: (value, text)."""
    gl = "".join('<i style="left:%s"></i>' % pct(v, maxv) for v, _ in ticks)
    out = ['<div class="k-hb%s" style="--lw:%dpx;--rh:%dpx">' % (" k-wl" if ylabel else "", lw, rh)]
    if ylabel:
        out.append('<div class="k-axl">%s</div>' % ylabel)
    out.append('<div class="k-gl">%s</div>' % gl)
    for lab, v in rows:
        out.append('<div class="k-hr"><span class="k-hl">%s</span><span class="k-ht"><i style="--w:%s"></i></span></div>' % (
            lab, pct(v, maxv)))
    xa = "".join('<span style="left:%s">%s</span>' % (pct(v, maxv), t) for v, t in ticks)
    out.append('<div class="k-hr"><span></span><span class="k-xa">%s</span></div>' % xa)
    out.append('</div><div class="k-xt2">%s</div>' % xlabel)
    return "".join(out)


def chart(inner, yticks, ytop, xt_html, h=140, ylab="Count of records", xlab="@timestamp per day", xclass=""):
    yt = "".join('<span style="bottom:%s">%s</span>' % (pct(v, ytop), t) for v, t in yticks)
    hg = "".join('<div class="k-hg" style="bottom:%s"></div>' % pct(v, ytop) for v, _ in yticks if v)
    return ('<div class="k-ch" style="--h:%dpx"><div class="k-yl">%s</div><div class="k-yt">%s</div>'
            '<div class="k-pl">%s%s</div><div class="k-xt %s">%s</div><div class="k-xl">%s</div></div>') % (
        h, ylab, yt, hg, inner, xclass, xt_html, xlab)


def xticks(items):
    return "".join('<span style="left:%s%%">%s</span>' % (x, t) for x, t in items)


def donut(slices, size=""):
    acc, st = 0.0, []
    for _, c, v in slices:
        st.append("%s %.3f%% %.3f%%" % (c, acc, acc + v))
        acc += v
    return '<div class="k-dn %s" style="background:conic-gradient(%s)"></div>' % (size, ",".join(st))


def dlegend(slices, order=None):
    items = order or slices
    return '<div class="k-dl">%s</div>' % "".join(
        '<div><i style="background:%s"></i>%s<b>%s%%</b></div>' % (c, n, fmtp(v)) for n, c, v in items)


def fmtp(v):
    s = "%.2f" % v
    if s.endswith("0") and not s.endswith(".00"):
        s = s[:-1]
    if s.endswith(".00"):
        s = s[:-3]
    return s


legend_dot = '<span class="k-lg k-lgs"><i></i>%s</span>'


# ------------------------------------------------------------------ data transcribed from the screenshots
TACT = {  # name: (colour, share %)  -- Tactiques ATT&CK donut
    "Credential Access": ("#6dccb1", 26.49), "Discovery": ("#79aad9", 16.56), "Initial Access": ("#ee789d", 14.9),
    "Defense Evasion": ("#a987d1", 12.25), "Exfiltration": ("#e4a6c7", 9.93), "Execution": ("#f1d86f", 8.28),
    "Impact": ("#d3bfa0", 6.62), "Persistence": ("#f5a35c", 2.65), "Privilege Escalation": ("#c97b6a", 2.32)}
DONUT_ORDER = ["Discovery", "Initial Access", "Defense Evasion", "Exfiltration", "Execution", "Impact", "Persistence",
               "Privilege Escalation", "Credential Access"]
TECH = [  # (name as in Kibana, MITRE id, tactic, count)
    ("Password Guessing", "T1110.001", "Credential Access", 80), ("Network Service Scanning", "T1046", "Discovery", 50),
    ("Exploit Public-Facing App", "T1190", "Initial Access", 40), ("Exfiltration Over C2", "T1041", "Exfiltration", 30),
    ("Command Scripting", "T1059", "Execution", 25), ("Network DoS", "T1498", "Impact", 20),
    ("Valid Accounts", "T1078", "Defense Evasion", 15), ("Indicator Removal", "T1070", "Defense Evasion", 12),
    ("Process Injection", "T1055", "Defense Evasion", 10), ("Create Account", "T1136", "Persistence", 8),
    ("Abuse Elevation Control", "T1548", "Privilege Escalation", 7), ("Phishing", "T1566", "Initial Access", 5)]
MX_ORDER = ["Initial Access", "Execution", "Persistence", "Privilege Escalation", "Defense Evasion", "Credential Access",
            "Discovery", "Exfiltration", "Impact"]


def hist_bars():
    """Shape of the anomaly-score distribution (0.5 -> 1.0); no labelled values."""
    r = random.Random(11)
    out = []
    n = 120
    for k in range(n):
        x = k / n  # 0..1 over score axis 0.5..1.0
        if x < 0.07:
            out.append(0); continue
        dens = .97 if x < .58 else (.7 if x < .8 else .3)
        if r.random() > dens:
            out.append(0); continue
        h = r.choice([1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 6])
        if r.random() < .06 and x < .8:
            h = r.choice([7, 8, 9])
        out.append(h)
    out[16] = 9; out[28] = 8; out[44] = 7
    return out


# ------------------------------------------------------------------ Kibana tabs
def k_overview(lang):
    i = 0 if lang == "fr" else 1
    T = lambda fr, en: (fr, en)[i]
    kpi = kpanel(T("Compteur alertes critiques", "Critical alerts counter"),
                 '<div class="k-kpi k-r"><h4>%s</h4><b>2,644</b></div>' % T("Alertes Critiques", "Critical Alerts"),
                 pb='style="min-height:112px"')
    # bar chart over time
    bars = ('<svg viewBox="0 0 100 100" preserveAspectRatio="none"><rect x="42" y="0" width="1.7" height="100" fill="%s"/>'
            '<rect x="97.4" y="0" width="1.6" height="100" fill="#d9dce3" opacity=".7"/></svg>') % KG
    ch = chart(bars, [(0, "0"), (.5, "0.5"), (1, "1"), (1.5, "1.5"), (2, "2")], 2,
               xticks([(6, "8th"), (29, "15th"), (52, "22nd"), (75, "29th"), (97, "6th")]) +
               '<span style="left:0;transform:none;top:14px;display:none"></span>', h=118)
    ts = kpanel(T("Anomalies IA dans le temps (converted)", "AI anomalies over time (converted)"),
                legend_dot % "Count of records" + ch, badge=T("Last 30 days rounded to the day", "Last 30 days rounded to the day"))
    tot = kpanel(T("Total événements", "Total events"),
                 '<div class="k-kpi k-xl"><b>58,109</b><small style="margin-top:-6px">Count</small></div>', pb='style="justify-content:center"')
    left = '<div style="display:grid;gap:8px;grid-template-rows:auto 1fr;min-width:0">%s%s</div>' % (kpi, ts)
    return wrap(grid("1fr 1fr", left, tot, extra="align-items:stretch"), "SOC PFE - Dashboard Principal")


def k_details(lang):
    i = 0 if lang == "fr" else 1
    T = lambda fr, en: (fr, en)[i]
    ips = [("192.168.56.100", 100), ("45.33.32.156", 95.6), ("185.220.101.50", 93.5), ("10.0.0.55", 93),
           ("192.168.56.2", 91.7), ("192.168.56.3", 91.6), ("192.168.56.1", 86.9), ("192.168.56.9", 76.8),
           ("192.168.56.4", 75.4), ("192.168.56.5", 71.8)]
    p1 = kpanel(T("Top 10 IPs attaquantes", "Top 10 attacking IPs"),
                hbars(ips, 100, [(0, "0"), (28, "200"), (56, "400"), (84, "600")], 96, "Count", "source.ip: Descending"))
    sev = [("low", "#6dccb1", 31.84), ("high", "#79aad9", 29.72), ("critical", "#ee789d", 21.54), ("medium", "#a987d1", 16.9)]
    sevl = [sev[0], sev[1], sev[2], sev[3]]
    p2 = kpanel(T("Répartition par sévérité", "Severity breakdown"),
                '<div class="k-dwrap">%s%s</div>' % (donut(sev), dlegend(sevl)))
    ag = kpanel(T("Alertes par agent Wazuh", "Alerts per Wazuh agent"),
                chart('<div class="k-vbs"><i style="--h:99%"></i><i style="--h:99%"></i><i style="--h:99%"></i></div>',
                      [(0, "0"), (500, "500"), (1000, "1,000"), (1500, "1,500"), (2000, "2,000")], 2000,
                      '<span>web-server-01</span><span>linux-server-01</span><span>linux-server-02</span>',
                      h=100, ylab="Count", xlab="agent_name.keyword: Descending", xclass="k-fl"))
    sig = [("ET SCAN SSH BruteForce Tool Detected", 881), ("ET SCAN Nmap SYN Scan Detected", 751),
           ("ET POLICY Outbound Large Data Transfer", 331), ("ET SCAN SSH BruteForce Tool", 320),
           ("Directory Traversal Attempt", 121), ("ET POLICY Large Outbound Transfer", 120),
           ("SQL Injection Detected", 119), ("Command Injection Detected", 102),
           ("XSS Attack Detected", 99), ("SSH BruteForce", 81)]
    p4 = kpanel(T("Types d'attaques Suricata", "Suricata attack types"),
                hbars(sig, 900, [(0, "0"), (200, "200"), (400, "400"), (600, "600"), (800, "800")], 218, "Count"))
    return wrap(grid("1fr 1fr", p1, p2) + grid("1fr 1fr", ag, p4), "SOC PFE - Dashboard Principal")


def k_ia(lang):
    i = 0 if lang == "fr" else 1
    T = lambda fr, en: (fr, en)[i]
    k1 = kpanel(T("Score anomalie moyen (IA)", "Mean anomaly score (AI)"),
                '<div class="k-kpi k-c"><small>Median of anomaly_score</small><b>0.679</b></div>')
    k2 = kpanel(T("Anomalies Critiques IA", "Critical AI anomalies"),
                '<div class="k-kpi k-c"><small>Count of severity</small><b>134</b></div>')
    k3 = kpanel(T("Total anomalies IA", "Total AI anomalies"),
                '<div class="k-kpi k-r"><h4 style="font-size:19px">Count of records</h4><b>548</b></div>')
    hs = hist_bars()
    hist = '<div class="k-hist">%s</div>' % "".join(
        '<i class="%s" style="--h:%s"></i>' % ("z" if v == 0 else "", pct(v, 10)) for v in hs)
    h1 = kpanel(T("Distribution scores anomalie", "Anomaly score distribution"),
                chart(hist, [(0, "0"), (2, "2"), (4, "4"), (6, "6"), (8, "8"), (10, "10")], 10,
                      xticks([(0, "0.5"), (21.5, "0.6"), (42.5, "0.7"), (63.5, "0.8"), (84.5, "0.9"), (99, "1")]),
                      h=165, xlab="anomaly_score"))
    tl = ('<svg viewBox="0 0 100 100" preserveAspectRatio="none">'
          '<polyline points="0,100 100,100" fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="4 3" vector-effect="non-scaling-stroke"/>'
          '<polygon points="62.5,100 63.8,0 65.1,100" fill="%s" fill-opacity=".25" stroke="%s" stroke-width="1.4" stroke-dasharray="4 3" vector-effect="non-scaling-stroke"/>'
          '<polygon points="79.5,100 80.9,0 82.2,100" fill="%s" fill-opacity=".35" stroke="%s" stroke-width="1.6" vector-effect="non-scaling-stroke"/></svg>') % (KG, KG, KG, KG, KG)
    t1 = kpanel(T("Timeline anomalies IA", "AI anomalies timeline"),
                chart(tl, [(0, "0%"), (20, "20%"), (40, "40%"), (60, "60%"), (80, "80%"), (100, "100%")], 100,
                      xticks([(5, "Apr 2026"), (27, "May 2026"), (61, "Jun 2026"), (91, "Jul 2026")]), h=165))
    return wrap(grid("1.05fr 1fr 1.15fr", k1, k2, k3) + grid("1.1fr 1fr", h1, t1), "SOC PFE - Partie Intelligence Artificielle")


def k_mitre(lang):
    i = 0 if lang == "fr" else 1
    T = lambda fr, en: (fr, en)[i]
    rows = [(n, v) for n, _, _, v in TECH]
    p1 = kpanel(T("Top techniques MITRE ATT&CK", "Top MITRE ATT&CK techniques"),
                hbars(rows, 80, [(0, "0"), (20, "20"), (40, "40"), (60, "60"), (80, "80")], 150, "Count of records", "Top 12 values of mitre.name.keyword"))
    sl = [(n, TACT[n][0], TACT[n][1]) for n in DONUT_ORDER]
    leg = sorted(sl, key=lambda s: -s[2])
    p2 = kpanel(T("Tactiques ATT&CK", "ATT&CK tactics"),
                '<div class="k-dwrap">%s%s</div>' % (donut(sl, "k-sm"), dlegend(sl, leg)))
    # tactic x technique matrix
    cols = []
    for tac in MX_ORDER:
        c, p = TACT[tac]
        chips = "".join('<div class="k-mt" style="--c:%s"><b>%d</b>%s<s>%s</s></div>' % (c, v, n, tid)
                        for n, tid, tc, v in TECH if tc == tac)
        cols.append('<div class="k-mc"><div class="k-mh" style="--c:%s"><b>%s</b><span>%s%%</span></div>%s</div>' % (
            c, tac, fmtp(p), chips))
    mx = kpanel(T("Matrice tactiques × techniques (comptes de la période)", "Tactic × technique matrix (period counts)"),
                '<div class="k-mx">%s</div>' % "".join(cols))
    return wrap(grid("1.2fr 1fr", p1, p2) + grid("1fr", mx), "SOC PFE - MITRE ATT&CK")


def k_mitre_tl(lang):
    i = 0 if lang == "fr" else 1
    T = lambda fr, en: (fr, en)[i]
    comp = kpanel(T("Composant ayant détecté", "Detecting component"),
                  chart('<div class="k-vbs k-n4"><i style="--h:97%"></i><i style="--h:96%"></i><i style="--h:93.5%"></i><i style="--h:90%"></i></div>',
                        [(0, "0"), (20, "20"), (40, "40"), (60, "60"), (80, "80")], 80,
                        '<span>Zeek</span><span>Suricata</span><span>Wazuh</span><span>IsolationForest</span>',
                        h=126, xlab="Top 10 values of detection_source.keyword", xclass="k-fl"))
    # stacked areas, one-day spike on ~June 5th
    layers = [("#e6c15a", 24), ("#79aad9", 20), ("#a987d1", 17), ("#ee789d", 13), ("#e4a6c7", 8)]
    tac_svg = ['<svg viewBox="0 0 100 100" preserveAspectRatio="none">']
    tac_svg.append('<polygon points="64.5,100 66.5,10 69,56 69.2,100" fill="#6dccb1" fill-opacity=".55" stroke="#6dccb1" stroke-width="1.2" vector-effect="non-scaling-stroke"/>')
    for col, top in layers:
        y = 100 - top / 40 * 100
        tac_svg.append('<polygon points="64.5,100 66.5,%.1f 69,%.1f 69,100" fill="%s" fill-opacity=".8" vector-effect="non-scaling-stroke"/>' % (y, y + 14, col))
    tac_svg.append('</svg>')
    legend = ''.join('<div><i style="background:%s"></i>%s</div>' % (c, n) for n, c in [
        ("Credential Access", "#6dccb1"), ("Discovery", "#79aad9"), ("Initial Access", "#ee789d"),
        ("Defense Evasion", "#a987d1"), ("Exfiltration", "#e4a6c7"), ("Other", "#f1d86f")])
    tl = kpanel(T("Timeline des tactiques ATT&CK", "ATT&CK tactics timeline"),
                '<div style="display:grid;grid-template-columns:1fr 112px;gap:6px;flex:1">%s<div class="k-dl" style="font-size:11.5px;gap:6px;padding-top:4px">%s</div></div>' % (
                    chart("".join(tac_svg), [(0, "0"), (10, "10"), (20, "20"), (30, "30"), (40, "40")], 40,
                          xticks([(6, "Apr 2026"), (31, "May 2026"), (66, "Jun 2026")]), h=126), legend))
    tdata = [("T1110.001", "Password Guessing", "Credential Access", "medium", 27),
             ("T1110.001", "Password Guessing", "Credential Access", "high", 22),
             ("T1110.001", "Password Guessing", "Credential Access", "critical", 16),
             ("T1110.001", "Password Guessing", "Credential Access", "low", 15)]
    sevc = {"medium": "#a987d1", "high": "#79aad9", "critical": "#ee789d", "low": "#6dccb1"}
    body = ('<table class="k-tb"><thead><tr><th>Top 100 values of mitre.id.keyword</th><th>Top 100 values of mitre.name.keyword</th>'
            '<th>Top 100 values of mitre.tactic.keyword</th><th>Top 100 values of severity</th><th class="r">Count of records</th></tr></thead><tbody>%s</tbody></table>'
            '<div class="k-note">%s</div>') % (
        "".join('<tr><td class="m">%s</td><td>%s</td><td>%s</td><td><span class="k-sev" style="background:%s33;color:%s">%s</span></td><td class="r m">%d</td></tr>' % (
            a, b, c, sevc[d], sevc[d], d, e) for a, b, c, d, e in tdata),
        T("… défilement : la matrice complète contient une ligne par couple technique × sévérité.",
          "… scrolls: the full matrix holds one row per technique × severity pair."))
    mt = kpanel(T("Matrice MITRE complète", "Full MITRE matrix"), body)
    return wrap(grid("1fr 1.15fr", comp, tl) + grid("1fr", mt), "SOC PFE - MITRE ATT&CK")


def k_ar(lang):
    i = 0 if lang == "fr" else 1
    T = lambda fr, en: (fr, en)[i]
    a = kpanel(T("Total IP bloquées", "Total blocked IPs"), '<div class="k-kpi k-c"><b>8</b><small>Count</small></div>')
    b = kpanel(T("Score moyen de menace", "Mean threat score"),
               '<div class="k-kpi k-c"><small>Average of anomaly_score</small><b>0.916</b></div>')
    c = kpanel("Blocked vs Unblocked",
               '<div class="k-dwrap">%s%s</div>' % (donut([("unblocked", "#6dccb1", 100)], "k-sm"),
                                                    dlegend([("unblocked", "#6dccb1", 100)])))
    rows = [("198.51.100.2", "iptables DROP", .95, 1), ("203.0.113.99", "iptables DROP", .95, 2),
            ("203.0.113.99", "ufw deny", .95, 1), ("198.51.100.1", "iptables DROP", .92, 1),
            ("203.0.113.50", "iptables DROP", .88, 1), ("203.0.113.51", "iptables DROP", .87, 1),
            ("203.0.113.52", "iptables DROP", .86, 1)]
    body = ('<table class="k-tb"><thead><tr><th>Top 10 values of ip.keyword</th><th>Top 5 values of action.keyword</th>'
            '<th>Top 5 values of status.keyword</th><th class="r">Average of anomaly_score</th><th class="r">Count of records</th></tr></thead><tbody>%s</tbody></table>') % "".join(
        '<tr><td class="m">%s</td><td>%s</td><td>unblocked</td><td class="r m">%.2f</td><td class="r m">%d</td></tr>' % (ip, ac, s, n)
        for ip, ac, s, n in rows)
    t = kpanel("[No Title]", body)
    return wrap(grid("1fr 1.1fr 1.7fr", a, b, c) + grid("1fr", t), "SOC PFE - Firewall Active Response")


def k_blocks(lang):
    i = 0 if lang == "fr" else 1
    T = lambda fr, en: (fr, en)[i]
    rows = [("Exfiltration", 3), ("Test blocage firewall", 2), ("Brute force SSH", 1), ("Scan reseau", 1), ("Test UFW", 1)]
    p1 = kpanel(T("Top raisons de blocage", "Top blocking reasons"),
                hbars(rows, 3, [(0, "0"), (.5, "0.5"), (1, "1"), (1.5, "1.5"), (2, "2"), (2.5, "2.5"), (3, "3")], 130,
                      "Count of records", "Top 8 values of reason.keyword", rh=40))
    line = ('<svg viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="82.5,66.7 84.5,0" fill="none" stroke="%s" '
            'stroke-width="2" vector-effect="non-scaling-stroke"/><rect x="98" y="0" width="1.2" height="100" fill="#d9dce3" opacity=".6"/></svg>') % KG
    p2 = kpanel(T("Activité du firewall dans le temps", "Firewall activity over time"),
                chart(line, [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6")], 6,
                      xticks([(3, "Apr 2026"), (31, "May 2026"), (62, "Jun 2026")]), h=270))
    return wrap(grid("1fr 1fr", p1, p2), "SOC PFE - Firewall Active Response")


# ------------------------------------------------------------------ mail tabs
def m_email(lang):
    i = 0 if lang == "fr" else 1
    T = lambda fr, en: (fr, en)[i]
    acts = [T("Vérifier les hôtes sources dans le dashboard Kibana", "Check the source hosts in the Kibana dashboard"),
            T("Analyser les logs bruts via Discover", "Analyse the raw logs via Discover"),
            T("Isoler les machines avec score > 0.8 si non autorisées", "Isolate machines with score > 0.8 if unauthorised"),
            T("Croiser avec les alertes Suricata et Wazuh", "Cross-check with the Suricata and Wazuh alerts")]
    return ('<div class="k-ml"><div class="k-mh1"><span class="k-mav">S</span><div class="k-mfrom">SOC PFE<small>%s</small></div>'
            '<span class="k-mdate">%s</span></div>'
            '<div class="k-msub">%s<i>%s</i></div>'
            '<div class="k-mbg"><div class="k-mcard"><div class="k-mtop"><h3>\U0001F6A8 SOC PFE — %s</h3><p>SOFRECOM Maroc / Orange Maroc</p></div>'
            '<div class="k-mbody"><div class="k-malert"><b>%s</b> %s<small>%s</small></div>'
            '<div class="k-mst"><div><b>1</b><span>%s</span></div><div><b>1</b><span>%s</span></div><div class="w"><b>0</b><span>%s</span></div></div>'
            '<h4>%s</h4><table class="k-mtb"><thead><tr><th>Timestamp</th><th>%s</th><th>Score</th><th>%s</th></tr></thead>'
            '<tbody><tr><td>N/A</td><td class="c">CRITICAL</td><td>0.95</td><td>4444</td></tr></tbody></table>'
            '<div class="k-mact"><h5>\U0001F50D %s</h5><ul>%s</ul></div>'
            '<div class="k-mcta"><span>%s</span></div></div></div></div></div>') % (
        T("à moi", "to me"), T("ven. 19 juin 11:05", "Fri, Jun 19, 11:05"),
        T("[ALERTE CRITIQUE] SOC PFE — Alerte de Sécurité", "[ALERTE CRITIQUE] SOC PFE — Security Alert"),
        T("Boîte de réception", "Inbox"),
        T("Alerte de Sécurité", "Security Alert"),
        T("1 anomalie(s) détectée(s)", "1 anomaly detected"), T("par le module IA Isolation Forest", "by the Isolation Forest AI module"),
        T("Généré le 2026-06-19 à 11:05:27", "Generated on 2026-06-19 at 11:05:27"),
        T("Anomalies totales", "Total anomalies"), T("Critiques", "Critical"), T("Élevées", "High"),
        T("Détail des anomalies", "Anomaly details"), T("Sévérité", "Severity"), T("Port cible", "Target port"),
        T("Actions recommandées", "Recommended actions"), "".join("<li>%s</li>" % a for a in acts),
        T("Ouvrir le Dashboard SOC", "Open the SOC Dashboard"))


def m_pdf(lang):
    i = 0 if lang == "fr" else 1
    T = lambda fr, en: (fr, en)[i]
    vols = [("Suricata IDS", "3,180"), ("Zeek NSM", "11,575"), ("Wazuh Endpoint", "6,000"), (T("Module IA", "AI module"), "548")]
    sigs = [("ET SCAN SSH BruteForce Tool Detected", 880), ("ET SCAN Nmap SYN Scan Detected", 750),
            ("ET POLICY Outbound Large Data Transfer", 330), ("ET SCAN SSH BruteForce Tool", 320),
            ("Directory Traversal Attempt", 121), ("ET POLICY Large Outbound Transfer", 120),
            ("SQL Injection Detected", 119), ("Command Injection Detected", 101)]
    an = [("1.0", 55472, 84), ("0.997", 55160, 128), ("0.992", 65197, 91), ("0.99", 54838, 43), ("0.955", 52432, 41)]
    st = T("Actif", "Active")
    return ('<div class="k-pdf"><div class="k-pdfbar"><b>PDF</b><span>SOC_PFE_Rapport_20260701_1152.pdf</span><span class="k-sp"></span>'
            '<span class="pg">%s 1 / 2</span></div><div class="k-page">'
            '<div class="k-ph1"><h3>SOC Intelligence Platform<small>%s — 01/07/2026</small></h3>'
            '<p>SOFRECOM Maroc / Orange Maroc<br>%s 01/07/2026 %s 11:52<br>%s 30/06/2026 11:52 → 01/07/2026 11:52</p></div>'
            '<h4>%s</h4><div class="k-sum"><span class="r">111</span><span class="r">0</span><span class="g">548</span><span class="b">3,180</span></div>'
            '<h4>%s</h4><table class="k-pt b"><thead><tr><th class="l">Source</th><th>%s</th><th>%s</th></tr></thead><tbody>%s'
            '<tr><td class="l tot">TOTAL</td><td class="tot">56,563</td><td class="tot">—</td></tr></tbody></table>'
            '<h4>%s</h4><table class="k-pt t"><thead><tr><th>#</th><th class="l">Signature</th><th>%s</th></tr></thead><tbody>%s</tbody></table>'
            '<h4>%s</h4><table class="k-pt p"><thead><tr><th>Score</th><th>%s</th><th>%s</th><th>%s</th><th>Timestamp</th></tr></thead><tbody>%s</tbody></table>'
            '<h4>%s</h4><div class="k-rk">%s</div>'
            '<p class="k-rt">%s</p>'
            '<p class="k-ra"><b>Action 1</b> — %s</p><p class="k-ra"><b>Action 2</b> — %s</p></div></div>') % (
        "Page",
        T("Rapport de sécurité quotidien", "Daily security report"),
        T("Généré le", "Generated on"), T("à", "at"), T("Période :", "Period:"),
        T("Résumé exécutif", "Executive summary"),
        T("Volume par source", "Volume by source"), T("Événements", "Events"), T("Statut", "Status"),
        "".join('<tr><td class="l">%s</td><td>%s</td><td>%s</td></tr>' % (a, b, st) for a, b in vols),
        T("Top signatures IDS (Suricata)", "Top IDS signatures (Suricata)"), T("Détections", "Detections"),
        "".join('<tr><td>%d</td><td class="l">%s</td><td>%d</td></tr>' % (n + 1, s, v) for n, (s, v) in enumerate(sigs)),
        T("Top anomalies IA (Isolation Forest)", "Top AI anomalies (Isolation Forest)"),
        T("Sévérité", "Severity"), T("Port cible", "Target port"), T("Bytes réseau", "Network bytes"),
        "".join('<tr><td>%s</td><td>CRITICAL</td><td>%d</td><td>%d</td><td>2026-06-04T10:23:49</td></tr>' % a for a in an),
        T("Recommandations générées par IA (Ollama)", "AI-generated recommendations (Ollama)"),
        T("Niveau de risque : Critique", "Risk level: Critical"),
        T("Analyse de 5 anomalies détectées par l'IA (Isolation Forest). 5 alertes critiques et 0 alertes élevées identifiées. Score moyen d'anomalie : 0.987.",
          "Analysis of 5 anomalies detected by the AI (Isolation Forest). 5 critical alerts and 0 high alerts identified. Mean anomaly score: 0.987."),
        T("Isoler les hôtes avec score > 0.8 pour investigation", "Isolate the hosts with score > 0.8 for investigation"),
        T("Analyser les connexions vers les ports suspects dans Kibana", "Analyse the connections to suspicious ports in Kibana"))


# ------------------------------------------------------------------ terminal tabs
def docker_lines():
    ct = [("df11ac58ca0a", "ollama", "ollama/ollama:latest", "Up 2 weeks", "0.0.0.0:11434->11434/tcp, [::]:11434->11434/tcp"),
          ("d9d39055625f", "kibana", "docker.elastic.co/kibana/kibana:8.11.0", "Up 2 weeks", "0.0.0.0:5601->5601/tcp, [::]:5601->5601/tcp"),
          ("331b738dff1e", "nginx", "nginx:alpine", "Up 2 weeks", "0.0.0.0:80->80/tcp, [::]:80->80/tcp"),
          ("147aa35cf4f6", "python-ai", "soc-pfe-python-ai", "Up 2 weeks", "0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp"),
          ("5e890403dfd1", "logstash", "docker.elastic.co/logstash/logstash:8.11.0", "Up 2 weeks",
           "0.0.0.0:5044-5045->5044-5045/tcp, [::]:5044-5045->5044-5045/tcp, 9600/tcp"),
          ("6e53eddb5f47", "filebeat", "docker.elastic.co/beats/filebeat:8.11.0", "Up 2 weeks", ""),
          ("86488a533210", "wazuh-manager", "wazuh/wazuh-manager:4.7.0", "Up 2 weeks",
           "1514/tcp, 0.0.0.0:1515->1515/tcp, [::]:1515->1515/tcp, 514/udp, 0.0.0.0:1514->1514/udp, [::]:1514->1514/udp, 1516/tcp, "
           "0.0.0.0:55000->55000/tcp, [::]:55000->55000/tcp"),
          ("af94a573d55f", "elasticsearch", "docker.elastic.co/elasticsearch/elasticsearch:8.11.0", "Up 2 weeks (healthy)",
           "0.0.0.0:9200->9200/tcp, [::]:9200->9200/tcp, 9300/tcp")]
    w = [14, 15, 54, 0]
    l1 = "%-*s%-*s%-*s%s" % (w[0], "CONTAINER ID", w[1], "NAMES", w[2], "IMAGE", "STATUS")
    rows1 = ["%-*s%-*s%-*s%s" % (w[0], a, w[1], b, w[2], c, d) for a, b, c, d, _ in ct]
    import textwrap
    l2 = "%-*s%s" % (15, "NAMES", "PORTS")
    rows2 = []
    for _, b, _, _, p in ct:
        if not p:
            rows2.append(b); continue
        parts = textwrap.wrap(p, 88, subsequent_indent=" " * 15 if False else "")
        rows2.append("%-*s%s" % (15, b, parts[0]))
        rows2.extend(" " * 15 + x for x in parts[1:])
    return [
        C('docker ps --format "table {{.ID}}\\t{{.Names}}\\t{{.Image}}\\t{{.Status}}"'),
        O("\n".join([l1] + rows1), "k-tight"),
        C('docker ps --format "table {{.Names}}\\t{{.Ports}}"'),
        O("\n".join([l2] + rows2), "k-tight"),
    ]


def ufw_lines():
    to = [("22/tcp", ""), ("9200/tcp", ""), ("5601/tcp", ""), ("8000/tcp", ""), ("8050/tcp", "")]
    rows = ["%-27s%-14s%s" % (t, "ALLOW IN", "Anywhere") for t, _ in to] + [
        "%-27s%-14s%s" % (t + " (v6)", "ALLOW IN", "Anywhere (v6)") for t, _ in to]
    return [
        C("sudo ufw status verbose"),
        O("Status: active", "ok"),
        O("Logging: on (low)"),
        O("Default: deny (incoming), allow (outgoing), deny (routed)"),
        O("New profiles: skip"),
        O(" "),
        O("%-27s%-14s%s" % ("To", "Action", "From")),
        O("%-27s%-14s%s" % ("--", "------", "----"), "dim"),
    ] + [O(r) for r in rows]


# ------------------------------------------------------------------ apply
BUILDERS = {
    "soc-01-kibana-overview.png": k_overview, "soc-02-kibana-details.png": k_details, "soc-03-kibana-ia.png": k_ia,
    "soc-04-kibana-mitre.png": k_mitre, "soc-05-kibana-mitre-timeline.png": k_mitre_tl,
    "soc-06-kibana-active-response.png": k_ar, "soc-07-kibana-blocages.png": k_blocks,
    "soc-08-email-alert.png": m_email, "soc-09-pdf-report.png": m_pdf}
TERMS = {"soc-10-docker-ps.png": docker_lines, "soc-11-ufw-status.png": ufw_lines}


def apply(demo):
    for app in demo["apps"]:
        if app["id"] not in ("kibana", "mail", "term"):
            continue
        new = []
        for t in app["tabs"]:
            fn = os.path.basename(t.get("src", "")) if t.get("type") == "img" else ""
            if fn in BUILDERS:
                f = BUILDERS[fn]
                new.append(DOC(t["label"], f("fr"), f("en"), shot=fn, cap=t["cap"]))
            elif fn in TERMS:
                new.append(TERM(t["label"], TERMS[fn]()))
            else:
                new.append(t)
        app["tabs"] = new
