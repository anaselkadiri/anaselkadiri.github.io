# Portfolio — Anas El Kadiri

Site statique bilingue **FR / EN** (HTML/CSS/JS, aucune dépendance, aucun build) basé sur le CV. Aucun numéro de téléphone n'apparaît sur le site ni dans le CV PDF téléchargeable.

## Langues FR / EN

- Le sélecteur **FR | EN** est en haut à droite de la barre de navigation.
- Langue d'ouverture : celle du navigateur du visiteur (français → FR, sinon EN) ; son choix est mémorisé.
- Les captures, badges et la photo sont communs aux deux langues : un seul fichier suffit.
- Pour modifier un texte, change-le dans les deux balises : `<span class="fr">…</span><span class="en">…</span>`.
- Le bouton « Télécharger le CV » donne le CV en français dans les deux langues. Pour une version anglaise, ajoute un fichier `assets/CV_Anas_El_Kadiri_EN.pdf` et change le lien `href` du bouton (2 occurrences de `CV_Anas_El_Kadiri.pdf` dans `index.html`).

## Contenu du dossier

```
index.html                  ← le portfolio (à ouvrir dans le navigateur)
GUIDE_CAPTURES.md           ← état des captures (✅ fournies / ☐ à faire), noms de fichiers exacts
_source/                    ← générateur du site (Python) : pour modifier textes et démos
assets/
  CV_Anas_El_Kadiri.pdf     ← bouton « Télécharger le CV » (avec QR code)
  CV_Anas_El_Kadiri_sans_QR.pdf ← CV d'origine, base de add_qr.py
  qr-portfolio.png/.svg/.pdf ← QR code seul
  photo.jpg                 ← (à ajouter) photo de profil
  screenshots/              ← captures réelles essentielles extraites des rapports (26 images, données personnelles floutées)
  certs/                    ← (optionnel) badges des certifications
```

## QR code du portfolio (CV)

`assets/CV_Anas_El_Kadiri.pdf` contient déjà un QR code (haut à droite, cliquable) qui pointe vers **https://anaselkadiri.github.io** — adresse provisoire, à remplacer par la vraie. Quand le site est en ligne : `python3 _source/add_qr.py https://ton-adresse` régénère le CV avec le bon QR (à partir de `assets/CV_Anas_El_Kadiri_sans_QR.pdf`) ainsi que `assets/qr-portfolio.png / .svg / .pdf` (QR seul, pour LinkedIn, carte de visite, etc.). Nécessite `pip install pikepdf reportlab pillow`.

## Les démos « PC »

Quatre projets ont un portable animé et leurs captures essentielles : les 3 de l'EXPÉRIENCE PROFESSIONNELLE (SOC / PFE, audit applicatif SOFRECOM, Cité Verte OCP) et le projet technique MPLS L3VPN ; le laboratoire d'infrastructure et le stage réseau OCP 2023 n'ont qu'une courte description : il démarre tout seul quand on arrive dessus (logo, puis curseur qui clique et parcourt terminal, dashboards, architecture, résultats). Les écrans sont **recréés en HTML/CSS** d'après les captures et les rapports ; le bouton « Voir la capture réelle » ouvre la vraie image. Les boutons d'étapes sous le portable permettent de sauter à un écran, « Rejouer » relance la démo, « Plein écran » agrandit (sur mobile, la démo pivote en paysage). Le visiteur peut aussi cliquer lui-même sur la barre latérale et les onglets.

Pour modifier le contenu d'une démo : éditer `_source/demos.py` et `_source/ui_*.py`, puis lancer `python3 _source/build.py .` depuis ce dossier (régénère `index.html` et `GUIDE_CAPTURES.md`).

## Ajouter les captures (sans toucher au code)

1. Ouvre `GUIDE_CAPTURES.md` : chaque capture y a un nom de fichier précis.
2. Enregistre l'image dans `assets/screenshots/` avec ce nom exact.
3. Recharge `index.html` : l'image remplace automatiquement le cadre « Capture à ajouter ». Un clic ouvre l'agrandissement.

Avant la mise en ligne, ouvre `index.html` dans un éditeur, cherche `HIDE_EMPTY_SHOTS` (vers la fin) et mets `true` : les emplacements restés vides seront masqués.

## Personnaliser

- **Liens GitHub** : le projet SOC pointe vers `github.com/anaselkadiri`. Remplace par l'URL exacte du dépôt (chercher `href="https://github.com/anaselkadiri"` dans le bloc `p-soc`). Ajoute des boutons identiques dans les autres projets si tu as des dépôts.
- **Image de partage** (LinkedIn/WhatsApp) : ajoute `assets/og.png` (1200×630) et décommente la ligne `og:image` dans le `<head>`.
- **Mise à jour du CV** : remplace `assets/CV_Anas_El_Kadiri.pdf` en gardant le même nom.
- **Couleurs** : variables `--accent`, `--accent2`, `--bg` au début du `<style>`.

## Mise en ligne gratuite (GitHub Pages)

1. Crée un dépôt `anaselkadiri.github.io` (ou n'importe quel nom) et envoie-y tout le contenu de ce dossier.
2. Settings → Pages → Branch `main` / dossier `/ (root)` → Save.
3. Le site est disponible sur `https://anaselkadiri.github.io`. (Alternatives : Netlify ou Cloudflare Pages en glissant-déposant le dossier.)

## Confidentialité

Les projets SOFRECOM / Groupe Orange / OCP sont des travaux d'entreprise : anonymise les captures (IP, domaines, noms) et vérifie ta convention de stage avant de publier. Pour le pentest, privilégie une cible de démonstration (DVWA, Juice Shop).
