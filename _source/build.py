#!/usr/bin/env python3
"""Génère index.html (FR/EN) + GUIDE_CAPTURES.md à partir des données ci-dessous."""
import html, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demos, demo_mpls
demos.DEMOS["mpls"] = demo_mpls.MPLS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
SHOTDIR = "assets/screenshots"

def e(s): return html.escape(s, quote=True)
def T(fr, en):  # texte brut -> bloc bilingue
    return f'<span class="fr">{e(fr)}</span><span class="en">{e(en)}</span>'

def chips(items, hl=()):
    return "".join(f'<span class="chip{" hl" if i in hl else ""}">{e(i)}</span>' for i in items)

# ---------------------------------------------------------------- COMPÉTENCES
SKILLS = [
 ("i-net", ("Réseaux","Networking"), ["BGP","OSPF","EIGRP","RSTP","LACP","MPLS L3VPN","VRF · RD/RT","MP-BGP VPNv4","LDP","VLAN","NAT","GRE","OpenVPN","IPsec","Cisco IOS","Arista vEOS"], {"BGP","OSPF","MPLS L3VPN"}),
 ("i-shield", ("Sécurité","Security"), ["Wazuh","Elastic Security","Suricata","Zeek","pfSense HA (CARP/pfsync)","Linux & Windows hardening","Burp Suite","DVWA","Nmap","OWASP Top 10","ISO/IEC 27001:2022"], {"Wazuh","Suricata","Zeek"}),
 ("i-server", ("Systèmes & Virtualisation","Systems & Virtualization"), ["Ubuntu","Debian","Windows Server","Active Directory","VMware ESXi","vCenter","Workstation","PNetLab","Docker","Docker Compose","Oracle Cloud (OCI)","DNS / DHCP / NTP"], {"Docker","VMware ESXi"}),
 ("i-code", ("Automatisation & Développement","Automation & Development"), ["Python","FastAPI","Pandas","NumPy","Scikit-learn","Bash","NGINX","Git / GitHub","SQL (MySQL)","Laravel","React"], {"Python","FastAPI"}),
 ("i-chart", ("Supervision & Analyse","Monitoring & Analysis"), ["Elasticsearch","Logstash","Kibana","Filebeat","Wireshark","Random Forest","Isolation Forest","ARIMA"], {"Elasticsearch","Kibana"}),
]
def skills_html():
    out=[]
    for ic,(tf,te),items,hl in SKILLS:
        out.append(f'''      <div class="skill rv"><div class="skill-h"><span class="ico"><svg class="ic"><use href="#{ic}"/></svg></span><h3>{T(tf,te)}</h3></div><div class="chips">{chips(items,hl)}</div></div>''')
    return "\n".join(out)

# ---------------------------------------------------------------- PROJETS
# (fr, en) partout ; shots: (fichier, (titre fr, en), "quoi capturer" FR pour le guide)
PROJECTS = [
 dict(
  id="soc", cat="secu", featured=True, demo="soc",
  badge=("Projet de fin d'études","Final-year project"),
  meta=("SOFRECOM Maroc (Groupe Orange) · Fév. – Août 2026","SOFRECOM Morocco (Orange Group) · Feb – Aug 2026"),
  title=("SOC intelligent basé sur l'intelligence artificielle","AI-based intelligent SOC"),
  desc=("Conception et déploiement d'une plateforme SOC complète et conteneurisée : collecte et corrélation des événements, détection réseau, détection par machine learning, synthèse des incidents par LLM local et réponse automatisée avec blocage d'IP.",
        "Design and deployment of a complete, containerized SOC platform: event collection and correlation, network detection, machine-learning detection, incident summaries by a local LLM and automated response with IP blocking."),
  kpis=[(("95,3 %","95.3%"),("Exactitude Random Forest (5-fold, données synthétiques)","Random Forest accuracy (5-fold, synthetic data)")),
        (("58 s","58 s"),("De la détection au blocage automatique de l'IP","From detection to automatic IP block")),
        (("−51,7 %","−51.7%"),("Temps moyen de détection vs approche classique (120 s)","Mean time to detect vs classic approach (120 s)")),
        (("36 129","36,129"),("Événements traités pendant les mesures","Events processed during measurements"))],
  bullets=[
   ("Plateforme SOC sous Docker Compose : Wazuh 4.7, Elasticsearch 8.11, Logstash, Filebeat, Kibana, Suricata 7 et Zeek, derrière un reverse proxy NGINX.","SOC platform on Docker Compose: Wazuh 4.7, Elasticsearch 8.11, Logstash, Filebeat, Kibana, Suricata 7 and Zeek, behind an NGINX reverse proxy."),
   ("Module IA en Python / FastAPI : Isolation Forest (détection d'anomalies) et Random Forest (classification de 6 classes d'attaques).","AI module in Python / FastAPI: Isolation Forest (anomaly detection) and Random Forest (6-class attack classification)."),
   ("Synthèse des incidents par un LLM local (Ollama, llama3.2:3b) : niveau de risque, technique MITRE ATT&CK, recommandations.","Incident summaries by a local LLM (Ollama, llama3.2:3b): risk level, MITRE ATT&CK technique, recommendations."),
   ("Réponse automatisée : e-mail à l'analyste (seuil 0,7), blocage UFW via Active Response (seuil 0,85), déblocage automatique après 24 h.","Automated response: analyst email (0.7 threshold), UFW block via Active Response (0.85 threshold), automatic unblock after 24 h."),
   ("Tableaux de bord Kibana : vue d'ensemble, module IA, MITRE ATT&CK, Active Response ; rapport PDF quotidien.","Kibana dashboards: overview, AI module, MITRE ATT&CK, Active Response; daily PDF report."),
   ("Bilan mesuré : faux positifs de 35 % à 4,8 %, F1-score de 0,79 à 0,91 (rappel 100 % → 88,1 %, compromis assumé).","Measured outcome: false positives from 35% to 4.8%, F1-score from 0.79 to 0.91 (recall 100% → 88.1%, a deliberate trade-off)."),
  ],
  stack=["Wazuh 4.7","Elasticsearch 8.11","Logstash","Filebeat","Kibana","Suricata 7","Zeek","Docker Compose","Python","FastAPI","Scikit-learn","Isolation Forest","Random Forest","Ollama","NGINX","UFW"],
  shots=[
   ("soc-01-kibana-overview.png",("Kibana — vue d'ensemble","Kibana — overview"),"Fourni (rapport PFE)"),
   ("soc-02-kibana-details.png",("Kibana — détails","Kibana — details"),"Fourni (rapport PFE)"),
   ("soc-03-kibana-ia.png",("Kibana — module IA","Kibana — AI module"),"Fourni (rapport PFE)"),
   ("soc-04-kibana-mitre.png",("Kibana — MITRE ATT&CK","Kibana — MITRE ATT&CK"),"Fourni (rapport PFE)"),
   ("soc-05-kibana-mitre-timeline.png",("Chronologie MITRE","MITRE timeline"),"Fourni (rapport PFE)"),
   ("soc-06-kibana-active-response.png",("Active Response","Active Response"),"Fourni (rapport PFE)"),
   ("soc-07-kibana-blocages.png",("Blocages","Blocks"),"Fourni (rapport PFE)"),
   ("soc-08-email-alert.png",("E-mail d'alerte critique","Critical alert email"),"Fourni (rapport PFE)"),
   ("soc-09-pdf-report.png",("Rapport PDF quotidien","Daily PDF report"),"Fourni (rapport PFE)"),
   ("soc-10-docker-ps.png",("docker ps","docker ps"),"Fourni (rapport PFE)"),
   ("soc-11-ufw-status.png",("ufw status","ufw status"),"Fourni (rapport PFE)"),
   ("soc-12-architecture.png",("Architecture globale","Global architecture"),"Fourni (rapport PFE)"),
   ("soc-13-pipeline.png",("Pipeline de données","Data pipeline"),"Fourni (rapport PFE)"),
   ("soc-14-deployment.png",("Déploiement Docker","Docker deployment"),"Fourni (rapport PFE)"),
   ("soc-15-sequence.png",("Diagramme de séquence","Sequence diagram"),"Fourni (rapport PFE)"),
   ("soc-16-api-classes.png",("Classes de l'API IA","AI API classes"),"Fourni (rapport PFE)"),
   ("soc-17-wazuh-alerts.png",("Alertes Wazuh","Wazuh alerts"),"OPTIONNEL — Wazuh Dashboard : Security events (règles + MITRE)."),
   ("soc-18-api-swagger.png",("API IA — Swagger","AI API — Swagger"),"OPTIONNEL — Swagger UI FastAPI (/docs) avec /detect, /classify, /summarize-llm."),
  ],
  links=[("GitHub","https://github.com/anaselkadiri","gh")],
 ),
 dict(
  id="mpls", cat="reseau", featured=False, demo="mpls",
  badge=("Réseaux avancés","Advanced networking"),
  meta=("Projet de fin d'année · ISGA Rabat · 2025–2026","End-of-year project · ISGA Rabat · 2025–2026"),
  title=("Réseau opérateur MPLS L3VPN multi-clients, extranet et sécurisation","Multi-customer MPLS L3VPN carrier network with extranet and hardening"),
  desc=("Conception et mise en œuvre sous GNS3 d'une dorsale MPLS reliant trois clients sur neuf sites : isolation par VRF, quatre modes de routage PE–CE, extranet contrôlé par route-target, puis sécurisation (MD5, limite de routes, IPsec).",
        "Design and implementation in GNS3 of an MPLS backbone connecting three customers over nine sites: VRF isolation, four PE–CE routing modes, route-target-controlled extranet, then hardening (MD5, route limits, IPsec)."),
  kpis=[(("14","14"),("Routeurs Cisco 7200 : 3 PE, 2 P, 9 CE","Cisco 7200 routers: 3 PE, 2 P, 9 CE")),
        (("9","9"),("Sites clients répartis sur 3 VPN isolés","Customer sites spread over 3 isolated VPNs")),
        (("4","4"),("Modes de routage PE–CE : RIPv2, EIGRP, OSPF, statique","PE–CE routing modes: RIPv2, EIGRP, OSPF, static")),
        (("17 / 17","17 / 17"),("Tests de connectivité et d'isolation conformes","Connectivity and isolation tests as expected"))],
  bullets=[
   ("Dorsale OSPF (aire 0) + LDP ; les routeurs P commutent sur les labels sans connaître aucune route client.","OSPF backbone (area 0) + LDP; the P routers switch on labels without knowing any customer route."),
   ("Un VPN par client : VRF avec RD / RT sur les 3 PE et sessions MP-BGP VPNv4 (iBGP en maillage complet).","One VPN per customer: VRFs with RD / RT on the 3 PEs and MP-BGP VPNv4 sessions (full-mesh iBGP)."),
   ("Raccordement des sites en RIPv2, EIGRP, OSPF et routage statique, redistribués dans BGP.","Sites attached with RIPv2, EIGRP, OSPF and static routing, redistributed into BGP."),
   ("Extranet A1 ↔ C3 via le RT 1:400, volontairement restreint à ces deux sites.","A1 ↔ C3 extranet through RT 1:400, deliberately restricted to those two sites."),
   ("Sécurisation : authentification MD5 d'OSPF / LDP / BGP, 100 routes maximum par VRF, tunnel IPsec AES-256 entre deux sites du client B.","Hardening: MD5 authentication of OSPF / LDP / BGP, 100 routes max per VRF, AES-256 IPsec tunnel between two customer-B sites."),
   ("Preuve par Wireshark : double label MPLS ; paquet ICMP lisible sans IPsec, paquet ESP illisible avec IPsec. Limites de la maquette analysées.","Wireshark evidence: double MPLS label; readable ICMP packet without IPsec, unreadable ESP packet with IPsec. Lab limitations analysed."),
  ],
  stack=["GNS3 2.2","Cisco 7200 (IOS 12.4)","MPLS L3VPN","LDP","OSPF","VRF · RD · RT","MP-BGP VPNv4","RIPv2","EIGRP","IPsec / IKE","MD5","Wireshark"],
  shots=[
   ("mpls-01-topologie-gns3.png",("Topologie sous GNS3","GNS3 topology"),"Fourni (rapport MPLS)"),
   ("mpls-08-bgp-vpnv4-table.png",("Table BGP VPNv4 de R1","R1 VPNv4 BGP table"),"Fourni (rapport MPLS)"),
   ("mpls-09-route-vrfa.png",("Table de la VRFA (extranet vers C3)","VRFA table (extranet to C3)"),"Fourni (rapport MPLS)"),
   ("mpls-24-extranet-a1-c3.png",("Extranet : A1 joint C3","Extranet: A1 reaches C3"),"Fourni (rapport MPLS)"),
   ("mpls-26-isolation-a1-c1.png",("Isolation : A1 ne joint pas C1","Isolation: A1 cannot reach C1"),"Fourni (rapport MPLS)"),
   ("mpls-35-traceroute-labels.png",("Traceroute : labels MPLS dans le cœur","Traceroute: MPLS labels in the core"),"Fourni (rapport MPLS)"),
   ("mpls-16-wireshark-clair.png",("Wireshark : client A, paquet lisible","Wireshark: customer A, readable packet"),"Fourni (rapport MPLS)"),
   ("mpls-17-wireshark-esp.png",("Wireshark : client B, ESP chiffré","Wireshark: customer B, encrypted ESP"),"Fourni (rapport MPLS)"),
  ],
  links=[],
 ),
 dict(
  id="lab", cat="reseau secu", featured=False,
  badge=("Infrastructure & HA","Infrastructure & HA"),
  meta=("PNetLab / VMware · 2026","PNetLab / VMware · 2026"),
  title=("Laboratoire d'infrastructure d'entreprise","Enterprise infrastructure lab"),
  desc=("Conception d'une topologie d'entreprise à deux couches sous PNetLab / VMware : commutation Arista vEOS-lab, cluster pfSense en haute disponibilité (CARP / pfsync), serveurs Ubuntu, segmentation VLAN et tests de bascule.",
        "Design of a two-tier enterprise topology on PNetLab / VMware: Arista vEOS-lab switching, a high-availability pfSense cluster (CARP / pfsync), Ubuntu servers, VLAN segmentation and failover testing."),
  kpis=[],
  bullets=[],
  stack=["PNetLab","VMware","Arista vEOS","pfSense","CARP","pfsync","VLAN","Ubuntu"],
    shots=[],
  links=[],
 ),

 dict(
  id="pentest", cat="secu", featured=False, demo="pentest",
  badge=("Tests d'intrusion","Penetration testing"),
  meta=("SOFRECOM Maroc · Juil. – Août 2025","SOFRECOM Morocco · Jul – Aug 2025"),
  title=("Audit de sécurité applicative (OWASP Top 10)","Application security audit (OWASP Top 10)"),
  desc=("Stage de deux mois consacré à la sécurité applicative : étude des failles du Top 10 OWASP et tests d'intrusion avec Burp Suite dans un laboratoire Docker isolé (application Laravel volontairement vulnérable et DVWA).",
        "Two-month internship on application security: study of OWASP Top 10 flaws and penetration testing with Burp Suite in an isolated Docker lab (deliberately vulnerable Laravel application and DVWA)."),
  kpis=[(("6","6"),("Familles de vulnérabilités étudiées","Vulnerability families studied")),
        (("4","4"),("Modules Burp Suite utilisés (Proxy, Repeater, Intruder, Sequencer)","Burp Suite modules used (Proxy, Repeater, Intruder, Sequencer)"))],
  bullets=[
   ("Laboratoire isolé sous Docker Compose (Laravel + MySQL) : aucune exposition de l'infrastructure interne.","Isolated lab on Docker Compose (Laravel + MySQL): no exposure of the internal infrastructure."),
   ("Exploitation et analyse de l'injection SQL, XSS, LFI, upload de fichiers, RCE et CSRF sur DVWA.","Exploitation and analysis of SQL injection, XSS, LFI, file upload, RCE and CSRF on DVWA."),
   ("Burp Suite : interception (Proxy), rejeu (Repeater), automatisation par payloads (Intruder), analyse des jetons (Sequencer).","Burp Suite: interception (Proxy), replay (Repeater), payload automation (Intruder), token analysis (Sequencer)."),
   ("Comparaison scan manuel vs scan automatisé, puis démarche combinée : cartographie automatisée et confirmation manuelle.","Manual vs automated scanning comparison, then a combined approach: automated mapping followed by manual confirmation."),
   ("Pour chaque faille : mécanisme, preuve d'exploitation et contre-mesures (requêtes paramétrées, CSP, anti-CSRF, validation des fichiers).","For each flaw: mechanism, proof of exploitation and countermeasures (parameterized queries, CSP, anti-CSRF, file validation)."),
  ],
  stack=["Burp Suite","DVWA","Docker Compose","Laravel","MySQL","OWASP Top 10","SQLi","XSS","LFI","RCE"],
  shots=[
   ("pentest-01-dvwa-sqli.png",("SQL Injection (DVWA)","SQL Injection (DVWA)"),"Fourni (rapport de stage)"),
   ("pentest-02-xss-stored.png",("XSS stockée","Stored XSS"),"Fourni (rapport de stage, IP/e-mail floutés)"),
   ("pentest-03-lfi.png",("File Inclusion","File Inclusion"),"Fourni (rapport de stage)"),
   ("pentest-04-file-upload.png",("File Upload","File Upload"),"Fourni (rapport de stage)"),
   ("pentest-05-rce-schema.png",("RCE (schéma)","RCE (diagram)"),"Fourni (rapport de stage)"),
   ("pentest-06-burp-proxy.png",("Burp — Proxy","Burp — Proxy"),"Fourni (rapport de stage)"),
   ("pentest-07-burp-repeater.png",("Burp — Repeater","Burp — Repeater"),"Fourni (rapport de stage)"),
   ("pentest-08-burp-intruder.png",("Burp — Intruder","Burp — Intruder"),"Fourni (rapport de stage)"),
   ("pentest-09-burp-sequencer.png",("Burp — Sequencer","Burp — Sequencer"),"Fourni (rapport de stage)"),
   ("pentest-10-docker-compose.png",("docker-compose.yml","docker-compose.yml"),"Fourni (rapport de stage)"),
  ],
  links=[],
  note=("Travail réalisé sur un laboratoire de démonstration isolé : aucune donnée ni application interne n'est exposée.",
        "Work carried out on an isolated demo lab: no internal data or application is exposed."),
 ),

 dict(
  id="cite", cat="dev", featured=False, demo="cite",
  badge=("Développement web","Web development"),
  meta=("Groupe OCP, Khouribga · Stage de 1ʳᵉ année","OCP Group, Khouribga · 1st-year internship"),
  title=("« Cité Verte » — gestion des collaborateurs et des lots","“Cité Verte” — collaborator and plot management"),
  desc=("Application de gestion du dispositif de cession de lots aux collaborateurs : d'abord un prototype Microsoft Access (tableau de bord, formulaires, fiche technique pour contrat de vente), puis une application web Laravel (API REST) + React + MySQL.",
        "Application to manage the plot-transfer scheme for employees: first a Microsoft Access prototype (dashboard, forms, technical sheet for the sales contract), then a Laravel (REST API) + React + MySQL web application."),
  kpis=[(("4","4"),("Entités modélisées : collaborateurs, lots, versements, cessions","Modelled entities: collaborators, plots, payments, cessions")),
        (("2","2"),("Versions livrées : prototype Access puis application web","Versions delivered: Access prototype, then web app"))],
  bullets=[
   ("Analyse du processus métier de cession de lots et modélisation des données (MCD / MLD, dictionnaire de données).","Analysis of the plot-transfer business process and data modelling (conceptual / logical models, data dictionary)."),
   ("Prototype Microsoft Access : tableau de bord, gestion des collaborateurs, lots, versements et cessions, génération de fiches.","Microsoft Access prototype: dashboard, management of collaborators, plots, payments and cessions, form generation."),
   ("Application web : back-end Laravel (API REST), front-end React, base MySQL — CRUD complet, recherche et suivi des versements.","Web application: Laravel back-end (REST API), React front-end, MySQL database — full CRUD, search and payment tracking."),
   ("Données personnelles des collaborateurs floutées dans les captures publiées.","Employees' personal data is blurred in the published screenshots."),
  ],
  stack=["Laravel","React","MySQL","PHP","REST API","XAMPP","Microsoft Access","Excel","VS Code"],
  shots=[
   ("cite-01-react-accueil.png",("Application web — accueil","Web app — home"),"Fourni (rapport OCP)"),
   ("cite-02-react-collaborateurs.png",("Collaborateurs (noms floutés)","Collaborators (names blurred)"),"Fourni (rapport OCP)"),
   ("cite-03-react-ajout.png",("Ajout d'un collaborateur","Add a collaborator"),"Fourni (rapport OCP)"),
   ("cite-04-react-modif.png",("Modification","Edit"),"Fourni (rapport OCP)"),
   ("cite-05-react-lots.png",("Gestion des lots","Plot management"),"Fourni (rapport OCP)"),
   ("cite-06-react-versements.png",("Gestion des versements","Payment management"),"Fourni (rapport OCP)"),
   ("cite-07-access-dashboard.png",("Access — tableau de bord","Access — dashboard"),"Fourni (rapport OCP, valeurs masquées)"),
   ("cite-08-access-collaborateurs.png",("Access — collaborateurs","Access — collaborators"),"Fourni (rapport OCP, données floutées)"),
   ("cite-09-access-versements.png",("Access — versements","Access — payments"),"Fourni (rapport OCP, données floutées)"),
   ("cite-10-access-lots.png",("Access — lots","Access — plots"),"Fourni (rapport OCP, données floutées)"),
   ("cite-11-access-fiche.png",("Access — fiche technique","Access — technical sheet"),"Fourni (rapport OCP, données floutées)"),
   ("cite-12-access-cessions.png",("Access — cessions","Access — cessions"),"Fourni (rapport OCP, données floutées)"),
   ("cite-13-mld.png",("Modèle logique (MLD)","Logical model (MLD)"),"Fourni (rapport OCP)"),
   ("cite-14-table-collaborateurs.png",("Table collaborateurs","Collaborators table"),"Fourni (rapport OCP)"),
   ("cite-15-table-lots.png",("Table lots","Plots table"),"Fourni (rapport OCP)"),
   ("cite-16-table-versements.png",("Table versements","Payments table"),"Fourni (rapport OCP)"),
   ("cite-17-table-cessions.png",("Table cessions","Cessions table"),"Fourni (rapport OCP)"),
  ],
  links=[],
 ),
]

def shot_html(fn, title, hint):
    tf, te = title
    return (f'<figure class="shot"><div class="shot-frame"><img src="{SHOTDIR}/{fn}" alt="{e(tf)}" data-l="alt" data-fr="{e(tf)}" data-en="{e(te)}">'
            f'<div class="ph"><svg class="ic"><use href="#i-img"/></svg><b>{T("Capture à ajouter","Screenshot to add")}</b><code>{SHOTDIR}/{fn}</code></div></div>'
            f'<figcaption><b>{T(tf,te)}</b></figcaption></figure>')

DEMO_TXT = {
 "soc": ("Démo — le poste du SOC","Demo — the SOC workstation",
         "Le PC s'allume tout seul : terminal (rejeu de l'exfiltration, API IA), dashboards Kibana, architecture, résultats mesurés et alertes.",
         "The PC powers on by itself: terminal (exfiltration replay, AI API), Kibana dashboards, architecture, measured results and alerts."),
 "pentest": ("Démo — le laboratoire d'audit","Demo — the audit lab",
         "Le PC s'allume tout seul : laboratoire Docker, modules Burp Suite, failles DVWA, vulnérabilités et contre-mesures.",
         "The PC powers on by itself: Docker lab, Burp Suite modules, DVWA flaws, vulnerabilities and countermeasures."),
 "mpls": ("Démo — la maquette réseau","Demo — the network lab",
         "Le PC s'allume tout seul : topologie des 14 routeurs, dorsale OSPF / LDP, VRF et MP-BGP, tests d'isolation et d'extranet, sécurité (MD5, IPsec) et résultats.",
         "The PC powers on by itself: 14-router topology, OSPF / LDP backbone, VRFs and MP-BGP, isolation and extranet tests, security (MD5, IPsec) and results."),
 "cite": ("Démo — le poste de développement","Demo — the development workstation",
         "Le PC s'allume tout seul : application web React, prototype Access, modèle de données et synthèse du projet.",
         "The PC powers on by itself: React web app, Access prototype, data model and project overview."),
}
def demo_html(p):
    d = p.get("demo")
    if not d: return ""
    tf,te,df,de = DEMO_TXT[d]
    return (f'<div class="demo"><div class="demo-head"><div class="sub-h">{T(tf,te)}</div><p>{T(df,de)}</p></div>'
            f'<div class="pc" data-demo="{d}" data-state="off"></div></div>')

def project_html(p):
    kp = ""
    if p["kpis"]:
        kp = '<div class="kpis">' + "".join(f'<div class="kpi"><b>{T(*v)}</b><span>{T(*d)}</span></div>' for v,d in p["kpis"]) + '</div>'
    lis = "".join(f"<li>{T(*b)}</li>" for b in p["bullets"])
    links = ""
    if p["links"]:
        links = '<div class="p-links">' + "".join(f'<a class="btn sm" href="{u}" target="_blank" rel="noopener"><svg class="ic"><use href="#i-{ic}"/></svg>{e(t)}</a>' for t,u,ic in p["links"]) + '</div>'
    shots = "\n".join(shot_html(fn,t,h) for fn,t,h in p["shots"])
    note = f'<div class="todo-note">⚠ {T(*p["note"])}</div>' if p.get("note") else ""
    n = len(p["shots"])
    if not p["shots"]:
        gal = ""
    elif p.get("demo"):
        gal = (f'<details class="gal"><summary>{T("Galerie complète des captures","Full screenshot gallery")} <span class="count">· {n}</span></summary>'
               f'<div class="gallery">\n{shots}\n</div>{note}</details>')
    else:
        gal = f'<div class="gallery-wrap"><div class="sub-h">{T("Captures & livrables","Screenshots & deliverables")}</div><div class="gallery">\n{shots}\n</div>{note}</div>'
    if p["bullets"]:
        cols = f'''<div class="p-cols">
        <div><h4>{T("Réalisations","Highlights")}</h4><ul class="ticks">{lis}</ul></div>
        <div>{kp}<h4>Stack</h4><div class="chips">{chips(p["stack"])}</div>{links}</div>
      </div>'''
    else:
        cols = f'<div class="chips" style="margin-top:6px">{chips(p["stack"])}</div>{links}'
    return f'''    <article class="project rv{" featured" if p["featured"] else ""}" id="p-{p["id"]}" data-cat="{p["cat"]}">
      <div class="p-top"><span class="badge">{T(*p["badge"])}</span><span class="p-meta">{T(*p["meta"])}</span></div>
      <h3>{T(*p["title"])}</h3>
      <p class="p-desc">{T(*p["desc"])}</p>
      {cols}
      {demo_html(p)}
      {gal}
    </article>'''

def projects_html(): return "\n".join(project_html(p) for p in PROJECTS)

# ---------------------------------------------------------------- EXPÉRIENCE
EXP = [
 (("Ingénieur Cybersécurité — Stage PFE","Cybersecurity Engineer — Final-year internship"),("SOFRECOM Maroc (Groupe Orange), Rabat","SOFRECOM Morocco (Orange Group), Rabat"),("Fév. – Août 2026","Feb – Aug 2026"),
  ("Conception et déploiement d'un SOC intelligent basé sur l'intelligence artificielle","Design and deployment of an AI-based intelligent SOC"),
  [("Plateforme SOC conteneurisée : Wazuh 4.7, Elasticsearch 8.11, Logstash, Kibana, Suricata 7, Zeek.","Containerized SOC platform: Wazuh 4.7, Elasticsearch 8.11, Logstash, Kibana, Suricata 7, Zeek."),
   ("Détection ML (Random Forest 95,3 % en validation croisée sur données synthétiques, Isolation Forest) exposée via FastAPI ; synthèse LLM locale.","ML detection (Random Forest 95.3% in cross-validation on synthetic data, Isolation Forest) exposed through FastAPI; local LLM summaries."),
   ("Réponse automatisée (Active Response + UFW) : blocage de l'IP en 58 s, MTTD réduit de 51,7 % ; dashboards Kibana et documentation complète.","Automated response (Active Response + UFW): IP blocked in 58 s, MTTD reduced by 51.7%; Kibana dashboards and complete documentation.")]),
 (("Stage Sécurité Applicative","Application Security Internship"),("SOFRECOM Maroc, Rabat","SOFRECOM Morocco, Rabat"),("1ᵉʳ juil. – 31 août 2025","Jul 1 – Aug 31, 2025"),None,
  [("Laboratoire Docker isolé (Laravel + MySQL, DVWA) pour étudier et exploiter les failles du Top 10 OWASP : SQLi, XSS, LFI, upload, RCE, CSRF.","Isolated Docker lab (Laravel + MySQL, DVWA) to study and exploit OWASP Top 10 flaws: SQLi, XSS, LFI, upload, RCE, CSRF."),
   ("Tests d'intrusion avec Burp Suite (Proxy, Repeater, Intruder, Sequencer) ; contre-mesures et démarche manuel + automatisé documentées.","Penetration testing with Burp Suite (Proxy, Repeater, Intruder, Sequencer); countermeasures and a combined manual + automated approach documented.")]),
 (("Stage Développement","Development Internship"),("Groupe OCP, Khouribga","OCP Group, Khouribga"),("2024 · 1 mois","2024 · 1 month"),
  ("Projet « Cité Verte »","“Cité Verte” project"),
  [("Prototype Microsoft Access, puis application web Laravel (API REST) + React + MySQL pour la gestion des collaborateurs et des lots.","Microsoft Access prototype, then a Laravel (REST API) + React + MySQL web application to manage collaborators and plots."),
   ("Modélisation des données (MLD), suivi des versements, cessions et génération de la fiche technique pour contrat de vente.","Data modelling (logical model), payment and cession tracking, and generation of the technical sheet for the sales contract.")]),
 (("Stage Réseaux","Networking Internship"),("Groupe OCP, Khouribga","OCP Group, Khouribga"),("2023 · 1 mois","2023 · 1 month"),None,
  [("Observation de l'infrastructure réseau d'un site industriel et participation à la supervision et à la maintenance du réseau local.","Observation of an industrial site's network infrastructure and contribution to monitoring and maintenance of the local network.")]),
]
def exp_html():
    out=[]
    for t,org,when,sub,bl in EXP:
        s = f'<p style="color:var(--muted);font-size:.93rem;margin-top:6px"><em>{T(*sub)}</em></p>' if sub else ""
        out.append(f'''      <div class="tl-item rv"><div class="tl-top"><div><h3>{T(*t)}</h3><div class="org">{T(*org)}</div></div><span class="when">{T(*when)}</span></div>{s}<ul class="ticks">{"".join(f"<li>{T(*b)}</li>" for b in bl)}</ul></div>''')
    return "\n".join(out)

# ---------------------------------------------------------------- CERTIFICATIONS
CERTS = [
 ("cert-iso27001.png",("ISO/IEC 27001:2022 Information Security Associate™",)*2,("Certification professionnelle accréditée.","Accredited professional certification."),("Obtenue","Obtained"),False),
 ("cert-oci.png",("Oracle Cloud Infrastructure 2025 Certified Architect Associate",)*2,("Oracle.","Oracle."),("Obtenue","Obtained"),False),
 ("cert-cisco.png",("Cisco Networking Academy (2025)",)*2,("Networking Basics · Networking Devices and Initial Configuration · Introduction to Cybersecurity · Endpoint Security · Network Defense · Cyber Threat Management.",)*2,("Obtenue","Obtained"),False),
 ("cert-security-plus.png",("CompTIA Security+ (SY0-701)",)*2,("Certification en cours de préparation.","Certification in preparation."),("En préparation · 2026","In preparation · 2026"),True),
]
def certs_html():
    out=[]
    for fn,t,d,st,wip in CERTS:
        out.append(f'''      <div class="cert"><div class="badge-img"><img src="assets/certs/{fn}" alt="Badge {e(t[0])}" onerror="this.parentElement.remove()"></div><h3>{e(t[0])}</h3><p>{T(*d)}</p><span class="state{" wip" if wip else ""}">{T(*st)}</span></div>''')
    return "\n".join(out)

# ---------------------------------------------------------------- BUILD
tpl = open(os.path.join(HERE,"template.html"),encoding="utf-8").read()
# [[fr::en]] -> spans bilingues (contenu HTML déjà sûr, écrit à la main)
tpl = re.sub(r'\[\[(.+?)::(.+?)\]\]', lambda m: f'<span class="fr">{m.group(1)}</span><span class="en">{m.group(2)}</span>', tpl, flags=re.S)
# ---- Captures : seulement l'essentiel (galerie + boutons "capture réelle" de la démo)
ESS = {
 "soc": {"soc-01-kibana-overview.png","soc-03-kibana-ia.png","soc-04-kibana-mitre.png","soc-06-kibana-active-response.png",
         "soc-08-email-alert.png","soc-12-architecture.png","soc-15-sequence.png"},
 "pentest": {"pentest-01-dvwa-sqli.png","pentest-02-xss-stored.png","pentest-03-lfi.png","pentest-06-burp-proxy.png","pentest-08-burp-intruder.png"},
 "cite": {"cite-01-react-accueil.png","cite-02-react-collaborateurs.png","cite-06-react-versements.png",
          "cite-07-access-dashboard.png","cite-11-access-fiche.png","cite-13-mld.png"},
}
for _p in PROJECTS:
    if _p["id"] in ESS:
        _p["shots"] = [x for x in _p["shots"] if x[0] in ESS[_p["id"]]]
tpl = (tpl.replace("%%SKILLS%%",skills_html()).replace("%%PROJECTS%%",projects_html())
          .replace("%%EXPERIENCE%%",exp_html()).replace("%%CERTS%%",certs_html()))
UI_MODS = [("mpls","demo_mpls"),("soc","ui_soc"),("soc","ui_soc_arch"),("pentest","ui_pentest"),("cite","ui_cite")]
for _d,_m in UI_MODS:
    if not os.path.exists(os.path.join(HERE,_m+".py")): continue
    __import__(_m).apply(demos.DEMOS[_d])
for _d,_keep in ESS.items():
    for _a in demos.DEMOS[_d]["apps"]:
        for _t in _a["tabs"]:
            if _t.get("shot") and _t["shot"].split("/")[-1] not in _keep:
                del _t["shot"]; _t.pop("cap", None)
demo_json = json.dumps({"ui":demos.conv(demos.UI),"demos":demos.conv(demos.DEMOS)}, ensure_ascii=False, separators=(",",":")).replace("</","<\\/")
tpl = tpl.replace("%%DEMODATA%%", demo_json)
_css = ""
for _d,_m in UI_MODS:
    _p = os.path.join(HERE, f"{_m}.css")
    if os.path.exists(_p): _css += open(_p, encoding="utf-8").read() + "\n"
tpl = tpl.replace("%%DEMOCSS%%", _css)
os.makedirs(OUT,exist_ok=True)
open(os.path.join(OUT,"index.html"),"w",encoding="utf-8").write(tpl)

# ---------------------------------------------------------------- GUIDE CAPTURES (md)
total = sum(len(p["shots"]) for p in PROJECTS)
g=[]
g.append("# Guide des captures d'écran\n")
provided = sum(1 for p in PROJECTS for sh_ in p["shots"] if sh_[2].startswith("Fourni"))
g.append(f"Le portfolio contient **{total} emplacements** de captures, dont **{provided} déjà fournies** (extraites de tes 3 rapports, ✅). Les cases ☐ restent à faire : MPLS, laboratoire d'infrastructure, et 2 captures optionnelles du SOC. Un emplacement vide affiche « Capture à ajouter » (« Screenshot to add » en anglais).\n")
g.append("Les PC animés de démonstration (SOC, audit, Cité Verte) utilisent ces mêmes fichiers : remplacer une image met la démo à jour automatiquement. Les données personnelles des employés OCP ont été **floutées** dans les captures fournies.\n")
g.append("**Principe : tu n'as rien à modifier dans le code.** Enregistre simplement ton image dans `assets/screenshots/` avec **exactement** le nom indiqué ci-dessous : elle apparaît automatiquement à la place du cadre vide, en français comme en anglais.\n")
g.append("## Règles générales\n")
g.append("- **Format** : PNG (captures de texte/terminal) ou JPG/WebP — mais garde l'**extension indiquée** dans le nom de fichier.")
g.append("- **Ratio** : l'aperçu est en 16:10, recadré en haut de l'image ; vise ~1600×1000 px. L'image complète s'ouvre au clic (lightbox).")
g.append("- **Poids** : < 400 Ko par image idéalement (outil : squoosh.app ou tinypng.com).")
g.append("- **Langue des captures** : les outils (Kibana, Wazuh…) étant en anglais, une même image sert pour les deux langues du site.")
g.append("- **Mode** : mode sombre pour Kibana/Wazuh/terminal = cohérent avec le thème du site.")
g.append("- **Lisibilité** : zoom navigateur à 110–125 %, police de terminal ≥ 14 pt, pas de barre de favoris ni d'onglets perso.")
g.append("- **Confidentialité (important)** : floute ou remplace adresses IP publiques, noms de domaine/hostnames internes, tokens, mots de passe, clés API, noms d'employés. Rien de SOFRECOM / Groupe Orange / OCP identifiable sans autorisation — vérifie ta convention de stage / ton NDA.")
g.append("- **Avant de publier** : passe `HIDE_EMPTY_SHOTS = true` dans le `<script>` de `index.html` pour masquer automatiquement les emplacements restés vides.\n")
for p in PROJECTS:
    g.append(f"## {p['title'][0]}\n")
    if p.get("note"): g.append(f"> ⚠ {p['note'][0]}\n")
    g.append("| État | Fichier (dans `assets/screenshots/`) | Titre affiché (FR / EN) | Source / à capturer |")
    g.append("|---|---|---|---|")
    for fn,t,h in p["shots"]:
        g.append(f"| {'✅' if h.startswith('Fourni') else '☐'} | `{fn}` | {t[0]} / {t[1]} | {h} |")
    g.append("")
g.append("## Autres images (optionnelles)\n")
g.append("| ☐ | Fichier | Emplacement |")
g.append("|---|---|---|")
g.append("| ☐ | `assets/photo.jpg` | Photo de profil, section « À propos » (portrait 4:5, ≥ 800 px de large). Sinon les initiales « AE » s'affichent. |")
for fn,t,*_ in CERTS:
    g.append(f"| ☐ | `assets/certs/{fn}` | Badge / logo de la certification « {t[0]} » (format ~3:1, fond transparent idéal). Sinon la carte s'affiche sans badge. |")
g.append("| ☐ | `assets/og.png` | Image d'aperçu quand le lien est partagé (LinkedIn, WhatsApp) — 1200×630 px, puis décommenter la balise `og:image` dans `index.html`. |")
g.append("| ☐ | `assets/CV_Anas_El_Kadiri.pdf` | Déjà inclus (CV actuel, **sans numéro de téléphone**). Remplace-le à chaque mise à jour du CV en gardant le même nom. |")
g.append("")
open(os.path.join(OUT,"GUIDE_CAPTURES.md"),"w",encoding="utf-8").write("\n".join(g))
print("built", total, "shots")
