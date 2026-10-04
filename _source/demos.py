# -*- coding: utf-8 -*-
"""Données des démos « PC » (contenu tiré des 3 rapports). Tuples (fr, en) = texte bilingue."""
import html

S = "assets/screenshots/"
def e(s): return html.escape(s, quote=True)

def conv(o):
    """tuple (fr,en) -> {"fr":..,"en":..} ; récursif."""
    if isinstance(o, tuple): return {"fr": conv(o[0]), "en": conv(o[1])}
    if isinstance(o, list): return [conv(x) for x in o]
    if isinstance(o, dict): return {k: conv(v) for k, v in o.items()}
    return o

# -- lignes de terminal
def C(t, p=None):
    o = {"k": "cmd", "t": t}
    if p: o["p"] = p
    return o                       # commande tapée
def O(t, c=""): return {"k": "out", "t": t, "c": c}           # sortie
def EV(ts, t, d=""): return {"k": "evt", "ts": ts, "t": t, "d": d}  # évènement horodaté (délai long)
def IMG(src, label, cap): return {"type": "img", "src": S + src, "label": label, "cap": cap}
def TERM(label, lines, shot=None, cap=None):
    t = {"type": "term", "label": label, "lines": lines}
    if shot: t["shot"] = S + shot; t["cap"] = cap or ("", "")
    return t
def DOC(label, fr, en, shot=None, cap=None):
    t = {"type": "html", "label": label, "html": (fr, en)}
    if shot: t["shot"] = S + shot; t["cap"] = cap or ("", "")
    return t

def fmt(v, lang, dec=1):
    s = (f"{v:.{dec}f}" if v != int(v) else f"{int(v)}")
    return s.replace(".", ",") if lang == "fr" else s

# =====================================================================  SOC (PFE)
def results_before_after(lang):
    rows = [(("Précision","Precision"), 65, 94.2, "%", 100, 1),
            (("Rappel","Recall"), 100, 88.1, "%", 100, 1),
            (("F1-score","F1-score"), 0.79, 0.91, "", 1, 2),
            (("Faux positifs","False positives"), 35, 4.8, "%", 100, 1),
            (("Temps moyen de détection (MTTD)","Mean time to detect (MTTD)"), 120, 35, " s", 120, 0)]
    i = 0 if lang == "fr" else 1
    out = ['<div class="doc">']
    out.append('<div class="rs-leg"><span><i class="a"></i>%s</span><span><i class="b"></i>%s</span></div>' % (
        ("Sans IA (règles Suricata / Wazuh seules)", "Without AI (Suricata / Wazuh rules only)")[i],
        ("Avec IA (Isolation Forest + Random Forest)", "With AI (Isolation Forest + Random Forest)")[i]))
    for lab, a, b, unit, mx, dec in rows:
        out.append('<div class="rs-row"><div class="rs-label">%s</div><div class="rs-bars">'
                   '<div class="rs-bar a" style="--w:%.1f%%"><i></i><b>%s%s</b></div>'
                   '<div class="rs-bar b" style="--w:%.1f%%"><i></i><b>%s%s</b></div></div></div>' % (
                       lab[i], a / mx * 100, fmt(a, lang, dec), unit, b / mx * 100, fmt(b, lang, dec), unit))
    out.append('<p class="fine">%s</p>' % (
        "Le rappel recule (100 % → 88,1 %) par choix de conception : le filtrage par seuil de confiance écarte des cas ambigus afin de réduire la charge de triage (faux positifs 35 % → 4,8 %). F1-score global : 0,79 → 0,91.",
        "Recall drops (100% → 88.1%) by design: confidence-threshold filtering discards ambiguous cases to cut the analyst's triage load (false positives 35% → 4.8%). Overall F1-score: 0.79 → 0.91.")[i])
    out.append('</div>')
    return "".join(out)

def results_rf(lang):
    i = 0 if lang == "fr" else 1
    rows = [("brute_force", .97, .95, .96), ("exfiltration", .96, .97, .96), ("network_scan", .94, .93, .94),
            ("normal", .95, .97, .96), ("web_attack", .93, .90, .91), ("dos", .96, .95, .95)]
    h = ("Classe","Précision","Rappel","F1-score") if i == 0 else ("Class","Precision","Recall","F1-score")
    t = "".join('<tr><td class="m">%s</td><td>%s</td><td>%s</td><td>%s</td><td><i style="--w:%d%%"></i></td></tr>' % (
        n, fmt(p, lang, 2), fmt(r, lang, 2), fmt(f, lang, 2), f * 100) for n, p, r, f in rows)
    return ('<div class="doc"><div class="big"><b>%s %%</b><span>%s</span></div>'
            '<table class="tb"><thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th></th></tr></thead><tbody>%s</tbody></table>'
            '<p class="fine">%s</p></div>') % (
        fmt(95.3, lang), ("exactitude globale · validation croisée stratifiée 5-fold · 900 échantillons, 6 classes équilibrées",
                          "overall accuracy · stratified 5-fold cross-validation · 900 samples, 6 balanced classes")[i],
        *h, t,
        ("Écart-type 1,8 pt (93,6 % – 96,9 %). Jeu de données synthétique + bruit gaussien (15 %) : à lire comme une borne prudente, pas comme une performance garantie en production.",
         "Standard deviation 1.8 pt (93.6% – 96.9%). Synthetic dataset + 15% Gaussian noise: read it as a cautious bound, not a guaranteed production figure.")[i])

def results_volumes(lang):
    i = 0 if lang == "fr" else 1
    rows = [("Suricata (IDS réseau)", "Suricata (network IDS)", 8800), ("Zeek (connexions + DNS)", "Zeek (connections + DNS)", 11286),
            ("Wazuh (alertes endpoint)", "Wazuh (endpoint alerts)", 4400), ("Authentification système (réel)", "System authentication (real)", 9343),
            ("Alertes IA (Isolation Forest)", "AI alerts (Isolation Forest)", 2300)]
    mx = 11286
    t = "".join('<tr><td>%s</td><td class="m">%s</td><td><i style="--w:%d%%"></i></td></tr>' % (
        (fr, en)[i], f"{n:,}".replace(",", " " if lang == "fr" else ","), n / mx * 100) for fr, en, n in rows)
    return ('<div class="doc"><div class="big"><b>%s</b><span>%s</span></div>'
            '<table class="tb"><tbody>%s</tbody></table>'
            '<div class="pills"><span>%s</span><span>%s</span><span>%s</span></div></div>') % (
        "36 129" if lang == "fr" else "36,129",
        ("événements traités · ~2 300 alertes IA (taux d'alerte 6,5 %)", "events processed · ~2,300 AI alerts (6.5% alert rate)")[i], t,
        ("Seuil 0,7 → e-mail", "Threshold 0.7 → email")[i], ("Seuil 0,85 → blocage UFW", "Threshold 0.85 → UFW block")[i],
        ("Déblocage auto. après 24 h", "Auto-unblock after 24 h")[i])

SOC = dict(
    host="soc-lab", logo="SOC", sub="WSL2 / Ubuntu 22.04 · Docker Compose", accent="#2dd4bf", wall="radial-gradient(ellipse at 20% 10%,#12403f 0,transparent 55%),radial-gradient(ellipse at 90% 90%,#1b2c63 0,transparent 55%),#0a1020",
    boot=["[  OK  ] Started Docker Application Container Engine", "[  OK  ] Started Uncomplicated Firewall (ufw)",
          "[  OK  ] elasticsearch:8.11  (healthy)", "[  OK  ] wazuh-manager 4.7 · suricata · zeek",
          "[  OK  ] soc-pfe-python-ai  :8000", "[  OK  ] ollama  llama3.2:3b", "Welcome to soc-lab"],
    apps=[
        dict(id="term", icon="i-term", name=("Terminal", "Terminal"), chrome="term", title="root@soc-lab:~/soc-pfe", tabs=[
            TERM(("Scénario d'exfiltration", "Exfiltration scenario"), [
                O(("# Rejeu de la chronologie mesurée — exfiltration vers le port 4444", "# Replay of the measured timeline — exfiltration to port 4444"), "dim"),
                C("soc-replay --scenario exfiltration --port 4444"),
                EV("T+0s", ("Début du transfert de données", "Data transfer starts"), "Suricata / Zeek · capture du trafic"),
                EV("T+8s", ("Alerte IDS générée", "IDS alert raised"), "Suricata · EVE JSON → soc-suricata-*"),
                EV("T+12s", ("Alerte Wazuh générée", "Wazuh alert raised"), ("Wazuh Agent · règle niveau 9", "Wazuh Agent · level-9 rule")),
                EV("T+35s", ("Détection IA — score d'anomalie 0,849", "AI detection — anomaly score 0.849"), "Isolation Forest → soc-ai-alerts"),
                EV("T+42s", ("E-mail d'alerte envoyé à l'analyste", "Alert email sent to the analyst"), "Gmail SMTP · [ALERTE CRITIQUE]"),
                EV("T+58s", ("IP bloquée automatiquement", "IP blocked automatically"), "UFW Active Response · ufw insert deny from <IP>"),
                EV("T+60s", ("Traçabilité indexée", "Traceability indexed"), "Elasticsearch · soc-blocked-ips"),
                EV("T+24h", ("Déblocage automatique", "Automatic unblock"), "ufw delete deny from <IP>"),
                O(("✔ Détection → blocage : 58 s  (MTTD classique : 120 s, soit −51,7 %)", "✔ Detection → block: 58 s  (classic MTTD: 120 s, i.e. −51.7%)"), "ok"),
            ]),
            TERM(("API IA (FastAPI)", "AI API (FastAPI)"), [
                C("curl -s http://localhost:8000/health | python3 -m json.tool"),
                O('{\n    "status": "ok",\n    "model_ready": true,\n    "es_connected": true\n}'),
                C('curl -s "http://localhost:8000/detect?minutes=480"'),
                O('{\n    "total_events": 5000,\n    "anomalies_found": 502,\n    "alerts": [{ "anomaly_score": 0.849, "severity": "critical",\n                 "alert_type": "ANOMALY_ISOLATION_FOREST",\n                 "features": { "dst_port": 4444.0, "is_night": 1.0 } }]\n}'),
                C("curl -s -X POST localhost:8000/summarize-llm -d '{\"alerts\":[…]}'"),
                O('{\n    "niveau_risque": "Critique",\n    "mitre_technique": "T1041 - Exfiltration Over C2",\n    "recommandations": ["Bloquer immediatement l\'IP source au niveau firewall", …],\n    "llm_source": "ollama"\n}'),
            ]),
            IMG("soc-10-docker-ps.png", ("docker ps", "docker ps"), ("Conteneurs de la plateforme (Elasticsearch, Kibana, Logstash, Filebeat, Wazuh, Python-AI, Ollama, NGINX).", "Platform containers (Elasticsearch, Kibana, Logstash, Filebeat, Wazuh, Python-AI, Ollama, NGINX).")),
            IMG("soc-11-ufw-status.png", ("ufw status", "ufw status"), ("Pare-feu hôte : politique par défaut deny, ports SOC autorisés.", "Host firewall: default deny policy, SOC ports allowed.")),
        ]),
        dict(id="kibana", icon="i-globe", name=("Kibana", "Kibana"), chrome="browser", url="localhost:5601/app/dashboards", tabs=[
            IMG("soc-01-kibana-overview.png", ("Vue d'ensemble", "Overview"), ("Tableau de bord Kibana — vue d'ensemble du SOC.", "Kibana dashboard — SOC overview.")),
            IMG("soc-02-kibana-details.png", ("Détails", "Details"), ("Top signatures, répartition par sévérité, alertes par agent Wazuh.", "Top signatures, severity breakdown, alerts per Wazuh agent.")),
            IMG("soc-03-kibana-ia.png", ("Module IA", "AI module"), ("Anomalies détectées par l'Isolation Forest : score moyen, distribution, chronologie.", "Anomalies detected by the Isolation Forest: mean score, distribution, timeline.")),
            IMG("soc-04-kibana-mitre.png", ("MITRE ATT&CK", "MITRE ATT&CK"), ("Techniques et tactiques MITRE ATT&CK détectées.", "MITRE ATT&CK techniques and tactics detected.")),
            IMG("soc-05-kibana-mitre-timeline.png", ("Chronologie MITRE", "MITRE timeline"), ("Chronologie des tactiques et matrice MITRE complète.", "Tactics timeline and full MITRE matrix.")),
            IMG("soc-06-kibana-active-response.png", ("Active Response", "Active Response"), ("IP bloquées, score moyen de menace, statut bloqué / débloqué.", "Blocked IPs, mean threat score, blocked / unblocked status.")),
            IMG("soc-07-kibana-blocages.png", ("Blocages", "Blocks"), ("Raisons de blocage et activité du pare-feu dans le temps.", "Blocking reasons and firewall activity over time.")),
        ]),
        dict(id="arch", icon="i-layers", name=("Architecture", "Architecture"), chrome="plain", title=("Architecture du SOC", "SOC architecture"), tabs=[
            IMG("soc-13-pipeline.png", ("Pipeline de données", "Data pipeline"), ("Des sources (Suricata, Zeek, Wazuh, logs système) à la restitution (Kibana, notifications).", "From sources (Suricata, Zeek, Wazuh, system logs) to delivery (Kibana, notifications).")),
            IMG("soc-14-deployment.png", ("Déploiement Docker", "Docker deployment"), ("Réseau Docker soc-network (172.20.0.0/16) sur hôte WSL2 / Ubuntu 22.04.", "Docker network soc-network (172.20.0.0/16) on a WSL2 / Ubuntu 22.04 host.")),
            IMG("soc-15-sequence.png", ("Réponse automatique", "Automated response"), ("Diagramme de séquence : exfiltration détectée puis IP bloquée en 58 secondes.", "Sequence diagram: exfiltration detected, then IP blocked in 58 seconds.")),
            IMG("soc-16-api-classes.png", ("API IA (UML)", "AI API (UML)"), ("Classes de l'API : AnomalyDetector, AttackClassifier, IncidentSummarizer.", "API classes: AnomalyDetector, AttackClassifier, IncidentSummarizer.")),
            IMG("soc-12-architecture.png", ("Architecture globale", "Global architecture"), ("Architecture globale par couches (détail : cliquer pour agrandir).", "Layered global architecture (click to enlarge).")),
        ]),
        dict(id="res", icon="i-chart", name=("Résultats", "Results"), chrome="plain", title=("Résultats mesurés", "Measured results"), tabs=[
            DOC(("Avant / après IA", "Before / after AI"), results_before_after("fr"), results_before_after("en")),
            DOC(("Random Forest", "Random Forest"), results_rf("fr"), results_rf("en")),
            DOC(("Volumes & seuils", "Volumes & thresholds"), results_volumes("fr"), results_volumes("en")),
        ]),
        dict(id="mail", icon="i-mail", name=("Alertes", "Alerts"), chrome="plain", title=("Notifications automatiques", "Automatic notifications"), tabs=[
            IMG("soc-08-email-alert.png", ("E-mail critique", "Critical email"), ("Courrier d'alerte critique reçu par l'analyste.", "Critical alert email received by the analyst.")),
            IMG("soc-09-pdf-report.png", ("Rapport PDF quotidien", "Daily PDF report"), ("Rapport quotidien : volumes, top signatures, anomalies IA, recommandations du LLM.", "Daily report: volumes, top signatures, AI anomalies, LLM recommendations.")),
        ]),
    ])

# =====================================================================  PENTEST (stage SOFRECOM)
def vuln_cards(lang):
    i = 0 if lang == "fr" else 1
    V = [("SQL Injection", ("Du code SQL injecté dans une requête non filtrée manipule la base de données.", "SQL injected into an unfiltered query manipulates the database."),
          ("Requêtes paramétrées · validation des entrées", "Parameterized queries · input validation")),
         ("XSS", ("Du JavaScript injecté (reflected, stored, DOM) s'exécute chez les autres utilisateurs.", "Injected JavaScript (reflected, stored, DOM) runs in other users' browsers."),
          ("Échappement des sorties · CSP", "Output escaping · CSP")),
         ("LFI", ("Un fichier local est chargé sans validation stricte du chemin.", "A local file is loaded without strict path validation."),
          ("Liste blanche de chemins · validation", "Path allow-listing · validation")),
         ("RCE", ("Du code arbitraire est exécuté sur le serveur victime.", "Arbitrary code is executed on the victim server."),
          ("Ne jamais passer d'entrée brute à un shell · WAF", "Never pass raw input to a shell · WAF")),
         ("File Upload", ("Un fichier malveillant (ex. webshell PHP) est téléversé à la place d'une image.", "A malicious file (e.g. PHP webshell) is uploaded instead of an image."),
          ("Contrôle de type / extension · stockage isolé", "Type / extension checks · isolated storage")),
         ("CSRF", ("Un utilisateur authentifié est amené à exécuter une action non voulue.", "An authenticated user is tricked into performing an unwanted action."),
          ("Jetons anti-CSRF · en-têtes de sécurité", "Anti-CSRF tokens · security headers"))]
    cards = "".join('<div class="vc"><h6>%s</h6><p>%s</p><div class="fix"><span>%s</span>%s</div></div>' % (
        n, m[i], ("Parade", "Fix")[i], f[i]) for n, m, f in V)
    return '<div class="doc"><div class="vgrid">%s</div></div>' % cards

def compare_table(lang):
    i = 0 if lang == "fr" else 1
    h = (("Critère", "Scan manuel", "Scan Burp Suite (automatisé)"), ("Criterion", "Manual scan", "Burp Suite scan (automated)"))[i]
    R = [(("Précision", "Precision"), ("Très précise, dépend de l'expertise", "Very precise, depends on expertise"), ("Bonne, risque de faux positifs", "Good, risk of false positives")),
         (("Temps d'exécution", "Execution time"), ("Long", "Long"), ("Rapide", "Fast")),
         (("Failles détectées", "Flaws detected"), ("Logiques et complexes", "Logic flaws, complex cases"), ("Vulnérabilités techniques connues", "Known technical vulnerabilities")),
         (("Compétence requise", "Skill required"), ("Très élevée", "Very high"), ("Moyenne", "Medium")),
         (("Rapport final", "Final report"), ("Notes non structurées", "Unstructured notes"), ("Automatisé, exportable", "Automated, exportable"))]
    body = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (a[i], b[i], c[i]) for a, b, c in R)
    concl = ("Méthode retenue : un scan automatisé pour cartographier les failles connues, puis un audit manuel ciblé pour confirmer les résultats et trouver les failles logiques.",
             "Method retained: an automated scan to map known flaws, then a targeted manual audit to confirm findings and uncover logic flaws.")[i]
    return '<div class="doc"><table class="tb"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table><p class="fine">%s</p></div>' % (*h, body, concl)

PENTEST = dict(
    host="pentest-lab", logo="PENTEST LAB", sub="Docker · Laravel · DVWA · Burp Suite", accent="#f59e0b", wall="radial-gradient(ellipse at 15% 15%,#3d2a0a 0,transparent 55%),radial-gradient(ellipse at 90% 90%,#2a1450 0,transparent 55%),#0b0d14",
    boot=["[  OK  ] Started Docker Application Container Engine", "[  OK  ] network lab-net created (isolated)",
          "[  OK  ] container  laravel-vulnerable  :8000", "[  OK  ] container  mysql:5.7", "[  OK  ] container  dvwa",
          "[  OK  ] Burp Suite proxy 127.0.0.1:8080", "Lab ready — isolated from the internal network"],
    apps=[
        dict(id="term", icon="i-term", name=("Terminal", "Terminal"), chrome="term", title="user@pentest-lab:~/lab", tabs=[
            TERM(("Laboratoire Docker", "Docker lab"), [
                O(("# Environnement isolé : aucune exposition du réseau interne", "# Isolated environment: no exposure of the internal network"), "dim"),
                C("cat docker-compose.yml"),
                O("version: '3'\nservices:\n  web:\n    build: .\n    ports:\n      - \"8000:80\"\n  db:\n    image: mysql:5.7\n    environment:\n      MYSQL_DATABASE: testdb"),
                C("docker compose up -d"),
                O("[+] Running 2/2\n ✔ Container lab-db-1   Started\n ✔ Container lab-web-1  Started", "ok"),
                O(("# Burp Suite écoute sur 127.0.0.1:8080 — navigateur configuré via ce proxy", "# Burp Suite listens on 127.0.0.1:8080 — browser configured to use this proxy"), "dim"),
            ]),
            IMG("pentest-10-docker-compose.png", ("docker-compose.yml", "docker-compose.yml"), ("Configuration Docker du laboratoire vulnérable (extrait du rapport).", "Docker configuration of the vulnerable lab (from the report).")),
        ]),
        dict(id="burp", icon="i-shield", name=("Burp Suite", "Burp Suite"), chrome="plain", title="Burp Suite", tabs=[
            IMG("pentest-06-burp-proxy.png", ("Proxy", "Proxy"), ("Interception et historique HTTP : modifier un paramètre (ex. productId) pour tester une injection.", "HTTP interception and history: tamper with a parameter (e.g. productId) to test an injection.")),
            IMG("pentest-07-burp-repeater.png", ("Repeater", "Repeater"), ("Rejouer une requête et comparer les réponses (payloads progressifs).", "Replay a request and compare responses (incremental payloads).")),
            IMG("pentest-08-burp-intruder.png", ("Intruder", "Intruder"), ("Automatisation par listes de payloads : sniper, battering ram, pitchfork, cluster bomb.", "Payload-list automation: sniper, battering ram, pitchfork, cluster bomb.")),
            IMG("pentest-09-burp-sequencer.png", ("Sequencer", "Sequencer"), ("Analyse de l'aléa des jetons de session.", "Randomness analysis of session tokens.")),
        ]),
        dict(id="dvwa", icon="i-bug", name=("DVWA", "DVWA"), chrome="browser", url="localhost/dvwa/vulnerabilities/", tabs=[
            IMG("pentest-01-dvwa-sqli.png", ("SQL Injection", "SQL Injection"), ("Injection SQL sur DVWA : la condition toujours vraie renvoie tous les utilisateurs.", "SQL injection on DVWA: an always-true condition returns every user.")),
            IMG("pentest-02-xss-stored.png", ("XSS stockée", "Stored XSS"), ("XSS stockée : le script injecté s'exécute à chaque affichage.", "Stored XSS: the injected script runs on every page view.")),
            IMG("pentest-03-lfi.png", ("File Inclusion", "File Inclusion"), ("Inclusion de fichier local sur DVWA.", "Local file inclusion on DVWA.")),
            IMG("pentest-04-file-upload.png", ("File Upload", "File Upload"), ("Upload non contrôlé : un fichier PHP est accepté à la place d'une image.", "Unchecked upload: a PHP file is accepted instead of an image.")),
            IMG("pentest-05-rce-schema.png", ("RCE (schéma)", "RCE (diagram)"), ("Principe d'une exécution de code à distance via une requête HTTP.", "How remote code execution works through an HTTP request.")),
        ]),
        dict(id="vuln", icon="i-doc", name=("Failles & parades", "Flaws & fixes"), chrome="plain", title=("Failles étudiées & contre-mesures", "Flaws studied & countermeasures"), tabs=[
            DOC(("6 vulnérabilités", "6 vulnerabilities"), vuln_cards("fr"), vuln_cards("en")),
            DOC(("Manuel vs Burp", "Manual vs Burp"), compare_table("fr"), compare_table("en")),
        ]),
    ])

# =====================================================================  OCP — Cité Verte
def ocp_doc(lang):
    i = 0 if lang == "fr" else 1
    def L(a): return "<ul>" + "".join("<li>%s</li>" % x[i] for x in a) + "</ul>"
    h = lambda t: "<h5>%s</h5>" % t[i]
    rules = [("Un collaborateur obtient un seul lot ; un lot n'est attribué qu'à un seul collaborateur.", "A collaborator gets one plot only; a plot is allocated to one collaborator only."),
             ("Un collaborateur effectue une seule cession, et un versement par collaborateur.", "A collaborator makes a single transfer (cession), and a single payment record."),
             ]
    sections = [("Collaborateurs", "Collaborators"), ("Versements", "Payments"), ("Cessions (CRUD complet)", "Cessions (full CRUD)"), ("Lots", "Plots"), ("Archives", "Archives")]
    feats = [("Recherche, ajout, modification et suppression pour chaque entité.", "Search, add, edit and delete for each entity."),
             ("Suivi des versements et avances ; fichiers de contrats.", "Tracking of payments, advances and contract files."),
             ("Génération de formulaires (fiche technique pour contrat de vente).", "Form generation (technical sheet for a sales contract).")]
    stack = ["Laravel (API REST)", "React", "MySQL", "PHP", "XAMPP", "VS Code", "Microsoft Access", "Excel"]
    persp = [("Reporting et statistiques sur collaborateurs et lots.", "Reporting and statistics on collaborators and plots."),
             ("Amélioration de l'interface (animations, drag-and-drop).", "UI improvements (animations, drag-and-drop)."),
             ("Interconnexion avec les systèmes internes.", "Integration with internal systems.")]
    return ('<div class="doc two">'
            '<div>%s<div class="pills">%s</div>%s%s</div>'
            '<div>%s%s%s%s<p class="fine">%s</p></div></div>') % (
        h(("Cinq sections clés", "Five key sections")), "".join("<span>%s</span>" % s[i] for s in sections),
        h(("Fonctionnalités", "Features")), L(feats),
        h(("Règles de gestion", "Business rules")), L(rules),
        h(("Pile technique", "Tech stack")) + '<div class="pills">' + "".join("<span>%s</span>" % s for s in stack) + "</div>", h(("Perspectives", "Next steps")) + L(persp),
        ("Données personnelles des collaborateurs floutées dans toutes les captures.", "Collaborators' personal data is blurred in every screenshot.")[i])

OCP = dict(
    host="ocp-pc", logo="CITÉ VERTE", sub="Laravel · React · MySQL · Access", accent="#4ade80", wall="radial-gradient(ellipse at 15% 10%,#0f3b1f 0,transparent 55%),radial-gradient(ellipse at 90% 95%,#10283f 0,transparent 55%),#0a1411",
    boot=["Starting XAMPP … Apache [OK]  MySQL [OK]", "Loading project « Cité Verte »", "composer: Laravel back-end ready", "npm: React front-end ready", "Opening workspace…"],
    apps=[
        dict(id="web", icon="i-globe", name=("Cité Verte (web)", "Cité Verte (web)"), chrome="browser", url="localhost/cite-verte", tabs=[
            IMG("cite-01-react-accueil.png", ("Accueil", "Home"), ("Page d'accueil de l'application : « Bienvenue dans la gestion des collaborateurs ».", "Application home page: “Welcome to collaborator management”.")),
            IMG("cite-02-react-collaborateurs.png", ("Collaborateurs", "Collaborators"), ("Liste des collaborateurs avec accès aux formulaires et au contrat de vente (noms floutés).", "Collaborator list with forms and sales-contract access (names blurred).")),
            IMG("cite-03-react-ajout.png", ("Ajout", "Add"), ("Formulaire d'ajout d'un collaborateur.", "Add-collaborator form.")),
            IMG("cite-04-react-modif.png", ("Modification", "Edit"), ("Formulaire de modification d'un collaborateur.", "Edit-collaborator form.")),
            IMG("cite-05-react-lots.png", ("Lots", "Plots"), ("Gestion des lots : afficher, rechercher, ajouter, modifier, supprimer.", "Plot management: list, search, add, edit, delete.")),
            IMG("cite-06-react-versements.png", ("Versements", "Payments"), ("Gestion des versements.", "Payment management.")),
        ]),
        dict(id="access", icon="i-folder", name=("Prototype Access", "Access prototype"), chrome="plain", title=("Prototype Microsoft Access", "Microsoft Access prototype"), tabs=[
            IMG("cite-07-access-dashboard.png", ("Tableau de bord", "Dashboard"), ("Tableau de bord : agents, avances, lots, graphiques (valeurs masquées).", "Dashboard: agents, advances, plots, charts (values masked).")),
            IMG("cite-08-access-collaborateurs.png", ("Collaborateurs", "Collaborators"), ("Gestion des collaborateurs (données masquées).", "Collaborator management (data masked).")),
            IMG("cite-09-access-versements.png", ("Versements", "Payments"), ("Gestion des versements (données masquées).", "Payment management (data masked).")),
            IMG("cite-10-access-lots.png", ("Lots", "Plots"), ("Gestion des lots (données masquées).", "Plot management (data masked).")),
            IMG("cite-12-access-cessions.png", ("Cessions", "Cessions"), ("Gestion des cessions.", "Cession management.")),
            IMG("cite-11-access-fiche.png", ("Fiche technique", "Technical sheet"), ("Génération de la fiche technique pour contrat de vente.", "Generation of the technical sheet for a sales contract.")),
        ]),
        dict(id="db", icon="i-db", name=("Base de données", "Database"), chrome="plain", title=("Modélisation des données", "Data modelling"), tabs=[
            IMG("cite-13-mld.png", ("MLD", "Logical model"), ("Modèle logique de données : collaborateurs, lots, versements, cessions.", "Logical data model: collaborators, plots, payments, cessions.")),
            IMG("cite-14-table-collaborateurs.png", ("Collaborateurs", "Collaborators"), ("Dictionnaire de données — table collaborateurs.", "Data dictionary — collaborators table.")),
            IMG("cite-15-table-lots.png", ("Lots", "Plots"), ("Dictionnaire de données — table lots.", "Data dictionary — plots table.")),
            IMG("cite-16-table-versements.png", ("Versements", "Payments"), ("Dictionnaire de données — table versements.", "Data dictionary — payments table.")),
            IMG("cite-17-table-cessions.png", ("Cessions", "Cessions"), ("Dictionnaire de données — table cessions.", "Data dictionary — cessions table.")),
        ]),
        dict(id="doc", icon="i-doc", name=("Le projet", "The project"), chrome="plain", title=("Cité Verte — synthèse", "Cité Verte — overview"), tabs=[
            DOC(("Synthèse", "Overview"), ocp_doc("fr"), ocp_doc("en")),
        ]),
    ])

DEMOS = {"soc": SOC, "pentest": PENTEST, "cite": OCP}

UI = dict(
    power=("Allumer", "Power on"), off=("Éteindre", "Power off"), full=("Plein écran", "Full screen"), exit=("Quitter", "Exit"),
    press=("Appuyez sur le bouton pour allumer le PC", "Press the button to turn the PC on"),
    zoom=("Cliquer pour agrandir", "Click to enlarge"), replay=("↻ Rejouer", "↻ Replay"),
    cap=("Démo animée, recréée d'après les écrans réels du projet — clique sur une étape pour y aller, ou prends la main.","Animated demo, recreated from the project's real screens — click a step to jump to it, or take control."), real=("Voir la capture réelle","View the real screenshot"), missing=("Capture à ajouter", "Screenshot to add"), booting=("Démarrage…", "Booting…"),
)
