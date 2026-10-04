# -*- coding: utf-8 -*-
"""Démo « Cité Verte » : écrans recréés en HTML/CSS (React, Access, base de données).
Aucune donnée réelle : valeurs masquées (•••) ou placeholders anonymes."""
from demos import DOC

SHOTDIR = "assets/screenshots/"


def tt(lang, fr, en):
    return fr if lang == "fr" else en


def mask(n=6):
    return '<span class="c-mask">%s</span>' % ("•" * n)


def note(lang):
    return '<span class="c-note">%s</span>' % tt(lang, "Données fictives / anonymisées", "Sample / anonymised data")


# ============================================================ logo (texte neutre, pas de reproduction du logo)
def logo(lang, big=False):
    return ('<span class="c-logo%s"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/>'
            '<circle cx="12" cy="12" r="4.2" fill="currentColor"/></svg><b>OCP</b></span>') % (" lg" if big else "")


# ============================================================ WEB (React)
def web_shell(lang, active, title, body, side_title, with_side=True, recs=True):
    nav = [("Collaborateurs", "Collaborators"), ("Lots", "Plots"), ("Versements", "Payments"), ("Cessions", "Cessions")]
    navh = "".join('<span class="c-navl%s">%s</span>' % (" on" if k == active else "", tt(lang, *n)) for k, n in enumerate(nav))
    head = ('<div class="c-whead"><div class="c-brand">%s<small>Strategic Business Unit – Mining<br>Khouribga Integrated Platform<br>Direction Capital Humain</small></div>%s</div>'
            % (logo(lang), navh))
    foot = ('<div class="c-wfoot"><span>© 2024 A.W APPLICATION</span><span class="c-fl"><u>%s</u><u>%s</u><u>%s</u></span></div>'
            % (tt(lang, "À propos de nous", "About us"), tt(lang, "Contactez-nous", "Contact us"), tt(lang, "Politique de confidentialité", "Privacy policy")))
    return '<div class="c-app"><div class="c-wcard">%s%s%s</div></div>' % (head, body, foot)


def web_side(lang, title, active_btn=None):
    btns = [("Afficher Tous", "Show all"), ("Rechercher", "Search"), ("Ajouter", "Add"), ("Modifier", "Edit"), ("Supprimer", "Delete")]
    return '<div class="c-wside"><h2>%s</h2>%s</div>' % (title, "".join('<span class="c-gbtn">%s</span>' % tt(lang, *b) for b in btns))


def web_main(lang, title, inner, records=True):
    return ('<div class="c-wmain"><div class="c-wttl">%s<h3>%s</h3></div>%s</div>'
            % (note(lang) if records else "<span></span>", title, inner))


def web_home(lang):
    body = ('<div class="c-whome"><div class="c-wside"><h2>%s</h2></div>'
            '<div class="c-welcome"><p>%s</p><p>%s</p><p>%s</p></div></div>') % (
        tt(lang, "Traitements", "Processing"),
        *tt(lang, ("BIENVENUE", "DANS LA GESTION", "DES COLLABORATEURS"), ("WELCOME", "TO THE MANAGEMENT", "OF COLLABORATORS")))
    return web_shell(lang, -1, "", body, "")


def web_collabs(lang):
    cards = ""
    for n in "ABC":
        cards += ('<div class="c-ccard"><div class="c-cname">%s %s</div><div class="c-crow"><span class="c-sbtn">%s</span></div>'
                  '<div class="c-sel"><span>%s</span><i></i></div><div class="c-crow"><span class="c-sbtn two">%s</span></div></div>') % (
            tt(lang, "Collaborateur", "Collaborator"), n, tt(lang, "plus ...", "more ..."), tt(lang, "formulaire...", "form..."),
            tt(lang, "contrat de vente", "sales contract"))
    body = '<div class="c-wbody">%s%s</div>' % (web_side(lang, tt(lang, "collaborateur", "collaborator"), 0),
                                              web_main(lang, tt(lang, "Tous les collaborateurs", "All collaborators"), cards))
    return web_shell(lang, 0, "", body, "")


def field(label, val="", kind="in", wide=False):
    if kind == "sel":
        inner = '<div class="c-in c-sel2"><span>%s</span><i></i></div>' % val
    else:
        inner = '<div class="c-in">%s</div>' % val
    return '<div class="c-fld"><label>%s</label>%s</div>' % (label, inner)


def web_form_fields(lang, edit=False):
    f = [field("Matriculecollab:", "0"), field("Sce:"), field("NomPrenom:")]
    cat = tt(lang, "Categorie:", "Category:")
    if edit:
        f.append(field(cat))
    else:
        f.append(field(cat, tt(lang, "Categorie ...", "Category ..."), "sel"))
    f += [field(tt(lang, "Telephone:", "Phone:"), ""), field("Cin:"), field("Mleconjointocp:", "0"), field("Nomprenomconjointocp:"), field("Observations:")]
    return '<div class="c-form">%s</div>' % "".join(f)


def web_add(lang):
    inner = ('<div class="c-fbox">%s<div class="c-frow"><span class="c-sbtn">%s</span></div></div>') % (web_form_fields(lang), tt(lang, "Ajouter", "Add"))
    body = '<div class="c-wbody">%s%s</div>' % (web_side(lang, tt(lang, "collaborateur", "collaborator")),
                                              web_main(lang, tt(lang, "Ajouter un collaborateur", "Add a collaborator"), inner, records=False))
    return web_shell(lang, 0, "", body, "")


def web_edit(lang):
    inner = ('<div class="c-search"><label>matriculecollab :</label><div class="c-in wide"></div><span class="c-sbtn bold">%s</span></div><hr class="c-hr">'
             '<div class="c-fbox">%s</div>') % (tt(lang, "Modifier", "Edit"), web_form_fields(lang, edit=True))
    body = '<div class="c-wbody">%s%s</div>' % (web_side(lang, tt(lang, "collaborateur", "collaborator")),
                                              web_main(lang, tt(lang, "Modifier un collaborateur", "Edit a collaborator"), inner, records=False))
    return web_shell(lang, 0, "", body, "")


def web_list(lang, side, title, items, label):
    cards = "".join('<div class="c-ccard flat"><ul><li>%s</li></ul><div class="c-crow"><span class="c-sbtn">%s</span></div></div>' % (i, tt(lang, "plus ...", "more ..."))
                    for i in items)
    return web_shell(lang, 0, "", '<div class="c-wbody">%s%s</div>' % (web_side(lang, side), web_main(lang, title, cards)), "")


def web_lots(lang):
    return web_list(lang, tt(lang, "lots", "plots"), tt(lang, "Tous les lots", "All plots"), ["001", "002"], "")


def web_vers(lang):
    return web_list(lang, tt(lang, "versements", "payments"), tt(lang, "Tous les versements", "All payments"), ["1", "2"], "")


# ============================================================ ACCESS
ICONS = {
    "home": '<svg viewBox="0 0 24 24"><path d="M12 2 1 12h3v10h6v-6h4v6h6V12h3z"/></svg>',
    "user": '<svg viewBox="0 0 24 24"><circle cx="12" cy="7" r="5"/><path d="M3 23c0-6 4-9 9-9s9 3 9 9z"/></svg>',
    "pay": '<svg viewBox="0 0 24 24"><path d="M12 1 1 11h3v11h16V11h3z"/><text x="12" y="19" text-anchor="middle" font-size="12" font-weight="800" fill="#55a64a">$</text></svg>',
    "lots": '<svg viewBox="0 0 24 24"><path d="M2 22 8 8l4-2 10 3-4 13zM9 22l3-9M14 21l2-8"/></svg>',
    "form": '<svg viewBox="0 0 24 24"><path d="M2 2h20v20H2z"/><path d="M5 7h3M10 7h9M5 12h3M10 12h9M5 17h3M10 17h9" stroke="#55a64a" stroke-width="2"/></svg>',
    "cess": '<svg viewBox="0 0 24 24"><rect x="2" y="2" width="11" height="11"/><path d="M4 15v6h7M15 10h7v12H12" fill="none" stroke="#111" stroke-width="2"/></svg>',
}


def acc_shell(lang, active, inner, stamp=True):
    items = [("home", "Tableau de bord", "Dashboard"), ("user", "Collaborateurs", "Collaborators"), ("pay", "Versement", "Payment"),
             ("lots", "Lots", "Plots"), ("form", "Formulaire", "Form"), ("cess", "Cession", "Cession")]
    nav = "".join('<span class="c-ni%s">%s<b>%s</b></span>' % (" on" if k == active else "", ICONS[ic], tt(lang, fr, en)) for k, (ic, fr, en) in enumerate(items))
    return ('<div class="c-acc"><aside class="c-side">%s<em>2024 APP BY A.W</em></aside>'
            '<div class="c-amain"><div class="c-atop">%s<span class="c-date">29/09/2024 20:36:44</span></div><div class="c-abody">%s</div></div></div>') % (
        nav, logo(lang, True), inner)


def gbtn(kind):
    g = {"plus": '<path d="M12 6v12M6 12h12" stroke="#fff" stroke-width="3"/>', "refresh": '<path d="M18 12a6 6 0 1 1-2-4.5M18 4v4h-4" fill="none" stroke="#fff" stroke-width="2.4"/>',
         "search": '<circle cx="10.5" cy="10.5" r="4.5" fill="none" stroke="#fff" stroke-width="2.4"/><path d="m14 14 5 5" stroke="#fff" stroke-width="3"/>',
         "print": '<path d="M7 9V4h10v5M7 17H4v-7h16v7h-3M7 14h10v6H7z" fill="none" stroke="#fff" stroke-width="2"/>'}[kind]
    return '<span class="c-ib"><svg viewBox="0 0 24 24">%s</svg></span>' % g


def acc_form(lang, title, labels, icons, boxclass="", val_first=None, tall=False, checkbox_row=None, select_row=None):
    rows = ""
    for k, lab in enumerate(labels):
        v = mask(8)
        if val_first is not None and k == 0:
            v = val_first
        if checkbox_row is not None and k == checkbox_row:
            v = '<i class="c-cb"></i>'
        if select_row is not None and k == select_row:
            v = '<i class="c-dd"></i>'
        rows += '<div class="c-ar"><span class="c-lb">%s</span><span class="c-vb">%s</span></div>' % (lab, v)
    return ('<div class="c-gbox %s"><div class="c-gh"><b>%s</b><span class="c-ibs">%s</span></div><div class="c-gb">%s</div>'
            '<div class="c-gf"><span class="c-abtn">%s</span><span class="c-abtn">%s</span></div></div>') % (
        boxclass, title, "".join(gbtn(i) for i in icons), rows, tt(lang, "Enregistrer", "Save"), tt(lang, "Supprimer", "Delete"))


def acc_list(lang, title, cols, rows=7, rowhead=None):
    th = "".join("<th>%s</th>" % c for c in cols)
    tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % (rowhead(r) if (rowhead and k == 0) else mask(5)) for k in range(len(cols))) for r in range(rows))
    return ('<div class="c-glist"><div class="c-gt">%s</div><table class="c-ds"><thead><tr>%s</tr></thead><tbody>%s</tbody></table><div class="c-lnote">%s</div></div>') % (title, th, tr, note(lang))


def acc_dash(lang):
    kp = [(tt(lang, "Nombres Des Agents OCP", "Number Of OCP Agents"), "users"), (tt(lang, "Somme Des Avances", "Sum Of Advances"), "bag"),
          (tt(lang, "Nombre Des Lots", "Number Of Plots"), "plot")]
    ico = {"users": '<svg viewBox="0 0 24 24"><circle cx="7" cy="8" r="3.2"/><circle cx="17" cy="8" r="3.2"/><circle cx="12" cy="13" r="3.4"/><path d="M1 21c0-4 3-6 6-6M23 21c0-4-3-6-6-6M6 22c0-4 3-6 6-6s6 2 6 6z"/></svg>',
           "bag": '<svg viewBox="0 0 24 24"><path d="M9 2h6l-2 4c4 1 7 5 7 10 0 4-3 6-8 6s-8-2-8-6c0-5 3-9 7-10z"/><text x="12" y="18" text-anchor="middle" font-size="9" font-weight="800" fill="#fff">$</text></svg>',
           "plot": '<svg viewBox="0 0 24 24"><path d="M3 14 9 5l12 3-3 11zM10 6l6 13"/></svg>'}
    cards = "".join('<div class="c-kpi"><div class="c-kh">%s</div><div class="c-kb"><span class="c-mask">•••••</span>%s</div></div>' % (t, ico[i]) for t, i in kp)
    months = ["févr/24", "mars/24", "avr/24", "mai/24", "juin/24", "juil/24", "août/24"] if lang == "fr" else ["Feb/24", "Mar/24", "Apr/24", "May/24", "Jun/24", "Jul/24", "Aug/24"]
    hs = [8, 60, 88, 50, 70, 40, 3]
    bars = "".join('<div class="c-bar"><i style="height:%d%%"></i><span>%s</span></div>' % (h, m) for h, m in zip(hs, months))
    ticks = "".join("<span>%d</span>" % v for v in (250, 200, 150, 100, 50, 0))
    chart1 = ('<div class="c-chart"><h4>%s</h4><div class="c-leg"><i class="g"></i>%s</div><div class="c-bars"><div class="c-yax">%s</div><div class="c-plot">%s</div></div></div>') % (
        tt(lang, "L'Avance", "Advances"), tt(lang, "Avances (échantillon)", "Advances (sample)"), ticks, bars)
    chart2 = ('<div class="c-chart"><h4>%s</h4><div class="c-leg"><i class="b"></i>Commercial<i class="o"></i>%s</div><div class="c-pie"></div></div>') % (
        tt(lang, "Type des lots", "Plot types"), tt(lang, "Résidentiel", "Residential"))
    inner = '<div class="c-kpis">%s</div><div class="c-charts">%s%s</div>%s' % (cards, chart1, chart2, note(lang))
    return acc_shell(lang, 0, inner)


def acc_collabs(lang):
    labels = ["MatriculeCollab", "Sce", tt(lang, "Nom et Prenom", "Full name"), tt(lang, "Categorie", "Category"), tt(lang, "Num telephone", "Phone no."), "CIN",
              "Mle conjoint OCP", tt(lang, "Nom prenom Conjoint OCP", "Spouse name (OCP)"), tt(lang, "Observation", "Notes")]
    inner = '<div class="c-split">%s%s</div>' % (
        acc_form(lang, tt(lang, "Gestion des Collaborateurs", "Collaborator management"), labels, ["plus", "refresh", "search"]),
        acc_list(lang, tt(lang, "Liste des Collaborateurs", "Collaborator list"), ["MatriculeCollab", "Sce", tt(lang, "Nom et Prenom", "Full name")], 8,
                 lambda r: "Employé %03d" % (r + 1) if lang == "fr" else "Employee %03d" % (r + 1)))
    return acc_shell(lang, 1, inner)


def acc_vers(lang):
    labels = ["MatriculeCollab", "Num_Recu_Avance", "avance", "Date_Avance", "1er_Versement", "NumRecu_1er_Versement", "Date_1er_Versement", "2eme_Versement",
              "Date_2eme_Versement", "NumRecu_3eme_Versement", "Date_3eme_Versement", "4eme_Versement", "NumRecu_4eme_Versement", "Date_4eme_Versement"]
    inner = '<div class="c-split">%s%s</div>' % (
        acc_form(lang, tt(lang, "Gestion des Versements", "Payment management"), labels, ["plus", "search", "refresh"], "dense"),
        acc_list(lang, tt(lang, "Liste des Versements", "Payment list"), ["MatriculeCollab", "Num_Recu_Avance", "avance"], 8,
                 lambda r: "Employé %03d" % (r + 1) if lang == "fr" else "Employee %03d" % (r + 1)))
    return acc_shell(lang, 2, inner)


def acc_lots(lang):
    labels = ["NLOT", "superficie m2", "Forme", "Titre Foncier", "Surface apres Bornage", "Nombre de Facades", "Type", "Plus Valeur sur Facades",
              "Valeur sur facades com…", "Principal", "Prix Cession", "MatriculeCollab", "Acquereur", "Adresse"]
    labels = [l for l in labels]
    inner = '<div class="c-split">%s%s</div>' % (
        acc_form(lang, tt(lang, "Gestion des Lots", "Plot management"), labels, ["print", "plus", "refresh", "search"], "dense", val_first='<span class="c-mask">1</span>'),
        acc_list(lang, tt(lang, "Liste des Lots", "Plot list"), ["NLOT", "superficie m2", "Forme"], 8, lambda r: "L-%03d" % (r + 1)))
    return acc_shell(lang, 3, inner)


def acc_cess(lang):
    labels = ["Id cession", tt(lang, "Contrat de vente", "Sales contract"), tt(lang, "Date signature par OIK/H", "Signature date by OIK/H"),
              tt(lang, "Date contrat (notaire)", "Contract date (notary)"), tt(lang, "NOTAIRE", "NOTARY"), "MatriculeCollab"]
    form = ('<div class="c-gbox"><div class="c-gh"><b>%s</b><span class="c-ibs">%s</span></div><div class="c-gb">%s</div>'
            '<div class="c-gf"><span class="c-abtn">%s</span><span class="c-abtn">%s</span></div></div>') % (
        tt(lang, "Gestion des Cessions", "Cession management"), "".join(gbtn(i) for i in ["plus", "refresh", "search"]),
        "".join('<div class="c-ar"><span class="c-lb">%s</span><span class="c-vb">%s</span></div>' % (l, v) for l, v in zip(
            labels, ['<span class="r">0</span>', '<i class="c-cb"></i>', "", "", '<i class="c-dd"></i>', ""])),
        tt(lang, "Enregistrer", "Save"), tt(lang, "Supprimer", "Delete"))
    cols = ["MatriculeCollab", tt(lang, "Contrat de vente", "Sales contract"), tt(lang, "Date signature par OIK/H", "Signature date by OIK/H"),
            tt(lang, "Date contrat (notaire)", "Contract date (notary)")]
    lst = ('<div class="c-glist"><div class="c-gt">%s</div><table class="c-ds c-empty"><thead><tr>%s</tr></thead><tbody><tr><td></td><td></td><td></td><td></td></tr>'
           '<tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr></tbody></table></div>') % (
        tt(lang, "Liste des Cessions", "Cession list"), "".join("<th>%s</th>" % c for c in cols))
    return acc_shell(lang, 5, '<div class="c-split">%s%s</div>' % (form, lst))


def acc_fiche(lang):
    inner = ('<div class="c-sheet"><div class="c-sh1"><div class="c-sbrand">%s<b>Strategic Business Unit – Mining<br>Khouribga Integrated Platform<br>Direction Capital Humain</b></div>'
             '<div class="c-sid"><span>MatriculeCollab</span><span class="c-vb">%s</span>%s</div></div>'
             '<h2>%s</h2><h5>%s</h5>'
             '<div class="c-sl"><span>%s</span><span>%s</span></div><div class="c-sl"><span>%s</span><span><u>:</u> %s</span></div>'
             '<div class="c-sl"><span>%s</span><span><u>:</u> %s</span></div></div>%s') % (
        logo(lang, True), mask(7), gbtn("print"), tt(lang, "Fiche Technique", "Technical Sheet"), tt(lang, "Pour contrat de vente", "For sales contract"),
        tt(lang, "Adresse", "Address"), mask(8), tt(lang, "Acquereur", "Buyer"), mask(14), tt(lang, "Prix Cession", "Cession price"), mask(7), note(lang))
    return acc_shell(lang, 4, inner)


# ============================================================ DATABASE
def mld(lang):
    P, F, I = "PK", "FK", "IDX"
    ents = {
        "cess": ("cessions", 10, 130, 215, [("idcessions", "bigint(20) unsigned", P), ("contratdevente", "tinyint(1)", ""), ("datesignatureparOIK/H", "date", ""),
                                            ("datecontratnotaire", "date", ""), ("notaire", "varchar(255)", ""), ("matriculecollab", "varchar(255)", F),
                                            ("created_at", "timestamp", ""), ("updated_at", "timestamp", "")]),
        "coll": ("collaborateurs", 290, 10, 250, [("matriculecollab", "varchar(255)", P), ("sce", "varchar(255)", ""), ("nomPrenom", "varchar(255)", ""),
                                                  ("categorie", "varchar(255)", ""), ("telephone", "varchar(255)", ""), ("cin", "varchar(255)", ""),
                                                  ("mleconjointocp", "bigint(20)", ""), ("nomprenomconjointocp", "varchar(255)", ""), ("observations", "varchar(255)", ""),
                                                  ("created_at", "timestamp", ""), ("updated_at", "timestamp", "")]),
        "lots": ("lots", 290, 232, 250, [("numLot", "varchar(191)", P), ("superficiem2", "int(11)", ""), ("forme", "varchar(255)", ""), ("titrefoncier", "varchar(255)", ""),
                                         ("surfaceapresbornage", "varchar(255)", ""), ("nombredefacades", "varchar(255)", ""), ("type", "varchar(255)", ""),
                                         ("plusvaluessurfacades", "decimal(10,2)", ""), ("plusvaluessurfacadescommercial", "decimal(10,2)", ""), ("principal", "decimal(10,2)", ""),
                                         ("prixCession", "decimal(10,2)", ""), ("matriculecollab", "varchar(255)", F), ("nomPrenom", "varchar(255)", I),
                                         ("created_at", "timestamp", ""), ("updated_at", "timestamp", "")]),
        "vers": ("versements", 590, 10, 250, [("idversements", "int(20)", P), ("avance", "int(20)", ""), ("numrecuavance", "date", ""), ("dateavance", "date", ""),
                                              ("1erversement", "decimal(8,2)", ""), ("numrecu1erversement", "bigint(20)", ""), ("date1erversement", "date", ""),
                                              ("2emeversement", "decimal(8,2)", ""), ("numrecu2emeversement", "bigint(20)", ""), ("date2emeversement", "date", ""),
                                              ("3emeversement", "decimal(8,2)", ""), ("numrecu3emeversement", "bigint(20)", ""), ("date3emeversement", "date", ""),
                                              ("4emeversement", "decimal(8,2)", ""), ("numrecu4emeversement", "bigint(20)", ""), ("date4emeversement", "date", ""),
                                              ("comptant", "decimal(8,2)", ""), ("num_recu_comptant", "bigint(20)", ""), ("date_comptant", "date", ""),
                                              ("montant_pret", "decimal(8,2)", ""), ("date_pret", "date", ""), ("num_cheque_pret", "varchar(255)", ""),
                                              ("banque_pret", "varchar(255)", ""), ("matriculecollab", "varchar(255)", F), ("created_at", "timestamp", ""), ("updated_at", "timestamp", "")]),
    }
    html = ""
    pos = {}
    for key, (name, x, y, w, cols) in ents.items():
        rows = ""
        for k, (c, t, kk) in enumerate(cols):
            cls = {"PK": "pk", "FK": "fk", "IDX": "ix"}.get(kk, "")
            rows += '<div class="c-er %s"><i>%s</i><b>%s</b><span>%s</span></div>' % (cls, kk, c, t)
            if c == "matriculecollab":
                pos[key] = (x, y + 22 + k * 16 + 8, w)
        html += '<div class="c-ent" style="left:%dpx;top:%dpx;width:%dpx"><div class="c-eh"><small>ocp</small> %s</div>%s</div>' % (x, y, w, name, rows)
    cx, cy, cw = pos["coll"]
    sx, sy, sw = pos["cess"]
    lx, ly, lw = pos["lots"]
    vx, vy, vw = pos["vers"]
    # lignes de relation : PK collaborateurs -> FK des trois autres tables
    svg = ('<svg class="c-rel" viewBox="0 0 850 510" aria-hidden="true">'
           '<path d="M%d %d H258 V%d H%d" /><path d="M%d %d H570 V%d H%d" /><path d="M570 %d V%d H%d" />'
           '<circle cx="%d" cy="%d" r="4"/><circle cx="%d" cy="%d" r="4"/><circle cx="%d" cy="%d" r="4"/>'
           '<circle cx="%d" cy="%d" r="4" class="o"/></svg>') % (
        cx, cy, sy, sx + sw, cx + cw, cy, vy, vx, cy, ly, lx + lw,
        sx + sw, sy, lx + lw, ly, vx, vy, cx, cy)
    leg = ('<div class="c-mleg"><span><i class="pk">PK</i> %s</span><span><i class="fk">FK</i> %s</span><span><i class="ix">IDX</i> %s</span><span><s></s> %s</span></div>') % (
        tt(lang, "clé primaire", "primary key"), tt(lang, "clé étrangère", "foreign key"), tt(lang, "index", "index"), tt(lang, "relation 1–1 via matriculecollab", "1–1 relation via matriculecollab"))
    return '<div class="c-db"><div class="c-canvas">%s%s</div>%s</div>' % (svg, html, leg)


def dict_table(lang, tname, cols, extra=None):
    body = ""
    for k, (c, t, kk, fr, en) in enumerate(cols, 1):
        key = {"PK": '<span class="c-k pk">PK</span>', "FK": '<span class="c-k fk">FK</span>', "IDX": '<span class="c-k ix">IDX</span>'}.get(kk, "")
        body += '<tr><td class="n">%d</td><td class="nm">%s</td><td class="ty">%s</td><td>%s</td><td class="ds">%s</td></tr>' % (k, c, t, key, tt(lang, fr, en))
    ex = '<p class="c-dnote">%s</p>' % tt(lang, *extra) if extra else ""
    return ('<div class="c-dict"><div class="c-dh"><b>ocp.%s</b><span>%d %s</span></div><table class="c-dt"><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th><th>Description</th></tr></thead>'
            '<tbody>%s</tbody></table>%s</div>') % (tname, len(cols), tt(lang, "colonnes", "columns"), tt(lang, "Colonne", "Column"), "Type", tt(lang, "Clé", "Key"), body, ex)


D_COLL = [
    ("matriculecollab", "varchar(255)", "PK", "Matricule du collaborateur", "Collaborator ID number"),
    ("sce", "varchar(255)", "", "Service", "Department"),
    ("nomPrenom", "varchar(255)", "", "Nom et prénom", "Full name"),
    ("categorie", "varchar(255)", "", "Catégorie professionnelle", "Job category"),
    ("telephone", "varchar(255)", "", "Numéro de téléphone", "Phone number"),
    ("cin", "varchar(255)", "", "Carte d'identité nationale", "National ID card"),
    ("mleconjointocp", "bigint(20)", "", "Matricule du conjoint (OCP)", "Spouse ID number (OCP)"),
    ("nomprenomconjointocp", "varchar(255)", "", "Nom et prénom du conjoint (OCP)", "Spouse full name (OCP)"),
]
D_LOTS = [
    ("numLot", "varchar(191)", "PK", "Numéro du lot", "Plot number"),
    ("superficiem2", "int(11)", "", "Superficie en m²", "Area in m²"),
    ("forme", "varchar(255)", "", "Forme du terrain", "Plot shape"),
    ("titrefoncier", "varchar(255)", "", "Titre foncier", "Land title"),
    ("surfaceapresbornage", "varchar(255)", "", "Surface après bornage", "Area after boundary marking"),
    ("nombredefacades", "varchar(255)", "", "Nombre de façades", "Number of frontages"),
    ("type", "varchar(255)", "", "Type de lot (commercial / résidentiel)", "Plot type (commercial / residential)"),
    ("plusvaluessurfacades", "decimal(10,2)", "", "Plus-value sur façades", "Frontage surcharge"),
    ("plusvaluessurfacadescommercial", "decimal(10,2)", "", "Plus-value sur façades commerciales", "Commercial frontage surcharge"),
    ("principal", "decimal(10,2)", "", "Montant principal", "Principal amount"),
    ("prixCession", "decimal(10,2)", "", "Prix de cession", "Cession price"),
    ("matriculecollab", "varchar(255)", "FK", "Collaborateur attributaire (→ collaborateurs)", "Allocated collaborator (→ collaborateurs)"),
    ("nomPrenom", "varchar(255)", "IDX", "Nom et prénom (index)", "Full name (index)"),
]
D_VERS = [
    ("idversements", "int(20)", "PK", "Identifiant du versement", "Payment identifier"),
    ("avance", "int(20)", "", "Avance", "Advance"),
    ("numrecuavance", "date", "", "N° de reçu de l'avance", "Advance receipt no."),
    ("dateavance", "date", "", "Date de l'avance", "Advance date"),
    ("1erversement", "decimal(8,2)", "", "1er versement", "1st payment"),
    ("numrecu1erversement", "bigint(20)", "", "N° de reçu du 1er versement", "1st payment receipt no."),
    ("date1erversement", "date", "", "Date du 1er versement", "1st payment date"),
    ("2emeversement", "decimal(8,2)", "", "2ème versement", "2nd payment"),
    ("numrecu2emeversement", "bigint(20)", "", "N° de reçu du 2ème versement", "2nd payment receipt no."),
    ("date2emeversement", "date", "", "Date du 2ème versement", "2nd payment date"),
    ("3emeversement", "decimal(8,2)", "", "3ème versement", "3rd payment"),
    ("numrecu3emeversement", "bigint(20)", "", "N° de reçu du 3ème versement", "3rd payment receipt no."),
    ("date3emeversement", "date", "", "Date du 3ème versement", "3rd payment date"),
    ("4emeversement", "decimal(8,2)", "", "4ème versement", "4th payment"),
    ("numrecu4emeversement", "bigint(20)", "", "N° de reçu du 4ème versement", "4th payment receipt no."),
    ("date4emeversement", "date", "", "Date du 4ème versement", "4th payment date"),
    ("comptant", "decimal(8,2)", "", "Paiement comptant", "Cash payment"),
    ("num_recu_comptant", "bigint(20)", "", "N° de reçu du comptant", "Cash payment receipt no."),
    ("date_comptant", "date", "", "Date du comptant", "Cash payment date"),
    ("montant_pret", "decimal(8,2)", "", "Montant du prêt", "Loan amount"),
    ("date_pret", "date", "", "Date du prêt", "Loan date"),
    ("num_cheque_pret", "varchar(255)", "", "N° de chèque du prêt", "Loan cheque no."),
    ("banque_pret", "varchar(255)", "", "Banque du prêt", "Loan bank"),
    ("matriculecollab", "varchar(255)", "FK", "Collaborateur concerné (→ collaborateurs)", "Related collaborator (→ collaborateurs)"),
]
D_CESS = [
    ("idcessions", "bigint(20)", "PK", "Identifiant de la cession", "Cession identifier"),
    ("contratdevente", "tinyint(1)", "", "Contrat de vente (oui / non)", "Sales contract (yes / no)"),
    ("datesignatureparOIK/H", "date", "", "Date de signature par OIK/H", "Signature date by OIK/H"),
    ("datecontratnotaire", "date", "", "Date du contrat chez le notaire", "Contract date at the notary"),
    ("notaire", "varchar(255)", "", "Notaire", "Notary"),
    ("matriculecollab", "varchar(255)", "FK", "Collaborateur concerné (→ collaborateurs)", "Related collaborator (→ collaborateurs)"),
]


def apply(demo):
    def rep(app_id, builders):
        app = next(a for a in demo["apps"] if a["id"] == app_id)
        new = []
        for tab, b in zip(app["tabs"], builders):
            if tab.get("type") != "img":
                new.append(tab)
                continue
            new.append(DOC(tab["label"], b("fr"), b("en"), shot=tab["src"].replace(SHOTDIR, ""), cap=tab["cap"]))
        app["tabs"] = new

    rep("web", [web_home, web_collabs, web_add, web_edit, web_lots, web_vers])
    rep("access", [acc_dash, acc_collabs, acc_vers, acc_lots, acc_cess, acc_fiche])
    n_coll = ("Laravel ajoute aussi observations, created_at et updated_at (voir le modèle logique).", "Laravel also adds observations, created_at and updated_at (see the logical model).")
    rep("db", [mld,
               lambda l: dict_table(l, "collaborateurs", D_COLL, n_coll),
               lambda l: dict_table(l, "lots", D_LOTS),
               lambda l: dict_table(l, "versements", D_VERS),
               lambda l: dict_table(l, "cessions", D_CESS)])
