# Guide des captures d'écran

Le portfolio contient **26 emplacements** de captures, dont **26 déjà fournies** (extraites de tes 3 rapports, ✅). Les cases ☐ restent à faire : MPLS, laboratoire d'infrastructure, et 2 captures optionnelles du SOC. Un emplacement vide affiche « Capture à ajouter » (« Screenshot to add » en anglais).

Les PC animés de démonstration (SOC, audit, Cité Verte) utilisent ces mêmes fichiers : remplacer une image met la démo à jour automatiquement. Les données personnelles des employés OCP ont été **floutées** dans les captures fournies.

**Principe : tu n'as rien à modifier dans le code.** Enregistre simplement ton image dans `assets/screenshots/` avec **exactement** le nom indiqué ci-dessous : elle apparaît automatiquement à la place du cadre vide, en français comme en anglais.

## Règles générales

- **Format** : PNG (captures de texte/terminal) ou JPG/WebP — mais garde l'**extension indiquée** dans le nom de fichier.
- **Ratio** : l'aperçu est en 16:10, recadré en haut de l'image ; vise ~1600×1000 px. L'image complète s'ouvre au clic (lightbox).
- **Poids** : < 400 Ko par image idéalement (outil : squoosh.app ou tinypng.com).
- **Langue des captures** : les outils (Kibana, Wazuh…) étant en anglais, une même image sert pour les deux langues du site.
- **Mode** : mode sombre pour Kibana/Wazuh/terminal = cohérent avec le thème du site.
- **Lisibilité** : zoom navigateur à 110–125 %, police de terminal ≥ 14 pt, pas de barre de favoris ni d'onglets perso.
- **Confidentialité (important)** : floute ou remplace adresses IP publiques, noms de domaine/hostnames internes, tokens, mots de passe, clés API, noms d'employés. Rien de SOFRECOM / Groupe Orange / OCP identifiable sans autorisation — vérifie ta convention de stage / ton NDA.
- **Avant de publier** : passe `HIDE_EMPTY_SHOTS = true` dans le `<script>` de `index.html` pour masquer automatiquement les emplacements restés vides.

## SOC intelligent basé sur l'intelligence artificielle

| État | Fichier (dans `assets/screenshots/`) | Titre affiché (FR / EN) | Source / à capturer |
|---|---|---|---|
| ✅ | `soc-01-kibana-overview.png` | Kibana — vue d'ensemble / Kibana — overview | Fourni (rapport PFE) |
| ✅ | `soc-03-kibana-ia.png` | Kibana — module IA / Kibana — AI module | Fourni (rapport PFE) |
| ✅ | `soc-04-kibana-mitre.png` | Kibana — MITRE ATT&CK / Kibana — MITRE ATT&CK | Fourni (rapport PFE) |
| ✅ | `soc-06-kibana-active-response.png` | Active Response / Active Response | Fourni (rapport PFE) |
| ✅ | `soc-08-email-alert.png` | E-mail d'alerte critique / Critical alert email | Fourni (rapport PFE) |
| ✅ | `soc-12-architecture.png` | Architecture globale / Global architecture | Fourni (rapport PFE) |
| ✅ | `soc-15-sequence.png` | Diagramme de séquence / Sequence diagram | Fourni (rapport PFE) |

## Réseau opérateur MPLS L3VPN multi-clients, extranet et sécurisation

| État | Fichier (dans `assets/screenshots/`) | Titre affiché (FR / EN) | Source / à capturer |
|---|---|---|---|
| ✅ | `mpls-01-topologie-gns3.png` | Topologie sous GNS3 / GNS3 topology | Fourni (rapport MPLS) |
| ✅ | `mpls-08-bgp-vpnv4-table.png` | Table BGP VPNv4 de R1 / R1 VPNv4 BGP table | Fourni (rapport MPLS) |
| ✅ | `mpls-09-route-vrfa.png` | Table de la VRFA (extranet vers C3) / VRFA table (extranet to C3) | Fourni (rapport MPLS) |
| ✅ | `mpls-24-extranet-a1-c3.png` | Extranet : A1 joint C3 / Extranet: A1 reaches C3 | Fourni (rapport MPLS) |
| ✅ | `mpls-26-isolation-a1-c1.png` | Isolation : A1 ne joint pas C1 / Isolation: A1 cannot reach C1 | Fourni (rapport MPLS) |
| ✅ | `mpls-35-traceroute-labels.png` | Traceroute : labels MPLS dans le cœur / Traceroute: MPLS labels in the core | Fourni (rapport MPLS) |
| ✅ | `mpls-16-wireshark-clair.png` | Wireshark : client A, paquet lisible / Wireshark: customer A, readable packet | Fourni (rapport MPLS) |
| ✅ | `mpls-17-wireshark-esp.png` | Wireshark : client B, ESP chiffré / Wireshark: customer B, encrypted ESP | Fourni (rapport MPLS) |

## Laboratoire d'infrastructure d'entreprise

| État | Fichier (dans `assets/screenshots/`) | Titre affiché (FR / EN) | Source / à capturer |
|---|---|---|---|

## Audit de sécurité applicative (OWASP Top 10)

> ⚠ Travail réalisé sur un laboratoire de démonstration isolé : aucune donnée ni application interne n'est exposée.

| État | Fichier (dans `assets/screenshots/`) | Titre affiché (FR / EN) | Source / à capturer |
|---|---|---|---|
| ✅ | `pentest-01-dvwa-sqli.png` | SQL Injection (DVWA) / SQL Injection (DVWA) | Fourni (rapport de stage) |
| ✅ | `pentest-02-xss-stored.png` | XSS stockée / Stored XSS | Fourni (rapport de stage, IP/e-mail floutés) |
| ✅ | `pentest-03-lfi.png` | File Inclusion / File Inclusion | Fourni (rapport de stage) |
| ✅ | `pentest-06-burp-proxy.png` | Burp — Proxy / Burp — Proxy | Fourni (rapport de stage) |
| ✅ | `pentest-08-burp-intruder.png` | Burp — Intruder / Burp — Intruder | Fourni (rapport de stage) |

## « Cité Verte » — gestion des collaborateurs et des lots

| État | Fichier (dans `assets/screenshots/`) | Titre affiché (FR / EN) | Source / à capturer |
|---|---|---|---|
| ✅ | `cite-01-react-accueil.png` | Application web — accueil / Web app — home | Fourni (rapport OCP) |
| ✅ | `cite-02-react-collaborateurs.png` | Collaborateurs (noms floutés) / Collaborators (names blurred) | Fourni (rapport OCP) |
| ✅ | `cite-06-react-versements.png` | Gestion des versements / Payment management | Fourni (rapport OCP) |
| ✅ | `cite-07-access-dashboard.png` | Access — tableau de bord / Access — dashboard | Fourni (rapport OCP, valeurs masquées) |
| ✅ | `cite-11-access-fiche.png` | Access — fiche technique / Access — technical sheet | Fourni (rapport OCP, données floutées) |
| ✅ | `cite-13-mld.png` | Modèle logique (MLD) / Logical model (MLD) | Fourni (rapport OCP) |

## Autres images (optionnelles)

| ☐ | Fichier | Emplacement |
|---|---|---|
| ☐ | `assets/photo.jpg` | Photo de profil, section « À propos » (portrait 4:5, ≥ 800 px de large). Sinon les initiales « AE » s'affichent. |
| ☐ | `assets/certs/cert-iso27001.png` | Badge / logo de la certification « ISO/IEC 27001:2022 Information Security Associate™ » (format ~3:1, fond transparent idéal). Sinon la carte s'affiche sans badge. |
| ☐ | `assets/certs/cert-oci.png` | Badge / logo de la certification « Oracle Cloud Infrastructure 2025 Certified Architect Associate » (format ~3:1, fond transparent idéal). Sinon la carte s'affiche sans badge. |
| ☐ | `assets/certs/cert-cisco.png` | Badge / logo de la certification « Cisco Networking Academy (2025) » (format ~3:1, fond transparent idéal). Sinon la carte s'affiche sans badge. |
| ☐ | `assets/certs/cert-security-plus.png` | Badge / logo de la certification « CompTIA Security+ (SY0-701) » (format ~3:1, fond transparent idéal). Sinon la carte s'affiche sans badge. |
| ☐ | `assets/og.png` | Image d'aperçu quand le lien est partagé (LinkedIn, WhatsApp) — 1200×630 px, puis décommenter la balise `og:image` dans `index.html`. |
| ☐ | `assets/CV_Anas_El_Kadiri.pdf` | Déjà inclus (CV actuel, **sans numéro de téléphone**). Remplace-le à chaque mise à jour du CV en gardant le même nom. |
