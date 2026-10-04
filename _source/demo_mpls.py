# -*- coding: utf-8 -*-
"""Démo « PC » du projet MPLS L3VPN (données du rapport). Écrans en HTML/CSS ; terminaux rejoués."""
import html
from demos import C, O, TERM, DOC

def e(s): return html.escape(s, quote=True)
ESSENTIAL = {"mpls-01-topologie-gns3.png","mpls-08-bgp-vpnv4-table.png","mpls-09-route-vrfa.png","mpls-24-extranet-a1-c3.png",
             "mpls-26-isolation-a1-c1.png","mpls-35-traceroute-labels.png","mpls-16-wireshark-clair.png","mpls-17-wireshark-esp.png"}
DROP = {"Interfaces PE","show ip vrf","CE R6 (RIP)","Limite de routes"}
def apply(demo):
    for a in demo["apps"]:
        a["tabs"] = [t for t in a["tabs"] if (t["label"][0] not in DROP)]
        for t in a["tabs"]:
            if t.get("shot") and t["shot"].split("/")[-1] not in ESSENTIAL:
                del t["shot"]; t.pop("cap", None)

CL = {"A": "#38bdf8", "B": "#c084fc", "C": "#4ade80"}

# ------------------------------------------------------------------ terminaux
def R(p, cmd): return C(cmd, p + "#")
def ping(p, dst, src, ok, rtt=None, mark=None):
    mark = mark or ("!!!!!" if ok else ".....")
    out = ("Type escape sequence to abort.\nSending 5, 100-byte ICMP Echos to %s, timeout is 2 seconds:\n"
           "Packet sent with a source address of %s\n%s\n") % (dst, src, mark)
    out += ("Success rate is 100 percent (5/5), round-trip min/avg/max = %s ms" % rtt) if ok else "Success rate is 0 percent (0/5)"
    return [R(p, "ping %s source FastEthernet0/0" % dst), O(out, "ok" if ok else "er")]

IFB = ("Interface                  IP-Address      OK? Method Status                Protocol\n"
       "FastEthernet0/0            unassigned      YES NVRAM  administratively down down\n"
       "Serial1/0                  10.1.14.1       YES NVRAM  up                    up\n"
       "Serial1/1                  100.1.16.1      YES NVRAM  up                    up\n"
       "Serial1/2                  100.1.17.1      YES NVRAM  up                    up\n"
       "Serial1/3                  100.1.18.1      YES NVRAM  up                    up\n"
       "Serial1/4                  unassigned      YES NVRAM  administratively down down\n"
       "Serial1/5                  unassigned      YES NVRAM  administratively down down\n"
       "Serial1/6                  unassigned      YES NVRAM  administratively down down\n"
       "Serial1/7                  unassigned      YES NVRAM  administratively down down\n"
       "Loopback0                  1.1.1.1         YES NVRAM  up                    up")
OSPFN = ("Neighbor ID     Pri   State           Dead Time   Address         Interface\n"
         "10.1.45.2         0   FULL/  -        00:00:29    10.1.45.2       Serial1/2\n"
         "2.2.2.2           0   FULL/  -        00:00:32    10.1.24.1       Serial1/1\n"
         "1.1.1.1           0   FULL/  -        00:00:32    10.1.14.1       Serial1/0")
LDPN = ("    Peer LDP Ident: 10.1.45.1:0; Local LDP Ident 1.1.1.1:0\n"
        "        TCP connection: 10.1.45.1.29042 - 1.1.1.1.646\n"
        "        State: Oper; Msgs sent/rcvd: 119/121; Downstream\n"
        "        Up time: 01:35:59\n"
        "        LDP discovery sources:\n"
        "          Serial1/0, Src IP addr: 10.1.14.2\n"
        "        Addresses bound to peer LDP Ident:\n"
        "          10.1.14.2       10.1.24.2       10.1.45.1")
LFIB = ("Local  Outgoing    Prefix            Bytes tag  Outgoing   Next Hop\n"
        "tag    tag or VC   or Tunnel Id      switched   interface\n"
        "16     Pop tag     1.1.1.1/32        12366      Se1/0      point2point\n"
        "17     Pop tag     2.2.2.2/32        4524       Se1/1      point2point\n"
        "18     Pop tag     10.1.25.0/30      0          Se1/2      point2point\n"
        "       Pop tag     10.1.25.0/30      0          Se1/1      point2point\n"
        "19     Pop tag     10.1.35.0/30      0          Se1/2      point2point\n"
        "20     18          3.3.3.3/32        4919       Se1/2      point2point")
VRFS = ("  Name                             Default RD          Interfaces\n"
        "  VRFA                             1:10                Se1/1\n"
        "  VRFB                             1:20                Se1/2\n"
        "  VRFC                             1:30                Se1/3")
BGPSUM = ("BGP router identifier 1.1.1.1, local AS number 1\n"
          "BGP table version is 39, main routing table version 39\n"
          "20 network entries using 2740 bytes of memory\n"
          "20 path entries using 1360 bytes of memory\n"
          "BGP activity 20/0 prefixes, 20/0 paths, scan interval 15 secs\n\n"
          "Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd\n"
          "2.2.2.2         4     1      21      21       39    0    0 00:08:37        6\n"
          "3.3.3.3         4     1      23      21       39    0    0 00:08:33        6")
BGPALL = ("   Network          Next Hop            Metric LocPrf Weight Path\n"
          "Route Distinguisher: 1:10 (default for vrf VRFA)\n"
          "*> 100.1.16.0/30    0.0.0.0                  0         32768 ?\n"
          "*>i100.1.32.0/30    3.3.3.3                  0    100      0 ?\n"
          "*>i100.1.34.0/30    3.3.3.3                  0    100      0 ?\n"
          "*>i100.1.209.0/30   2.2.2.2                  0    100      0 ?\n"
          "*>i172.31.3.0/24    3.3.3.3            2172416    100      0 ?\n"
          "*> 192.168.1.0      100.1.16.2               1         32768 ?\n"
          "*>i192.168.2.0      2.2.2.2                  1    100      0 ?\n"
          "*>i192.168.3.0      3.3.3.3                  1    100      0 ?\n"
          "Route Distinguisher: 1:20 (default for vrf VRFB)\n"
          "*> 100.1.17.0/30    0.0.0.0                  0         32768 ?\n"
          "*>i100.1.33.0/30    3.3.3.3                  0    100      0 ?\n"
          "*>i100.1.210.0/30   2.2.2.2                  0    100      0 ?\n"
          "*> 172.16.0.0       100.1.17.2         2172416         32768 ?\n"
          "*>i172.17.0.0       2.2.2.2                  0    100      0 ?\n"
          "*>i172.18.0.0       3.3.3.3                  1    100      0 ?\n"
          "Route Distinguisher: 1:30 (default for vrf VRFC)\n"
          "*> 100.1.18.0/30    0.0.0.0                  0         32768 ?\n"
          "*>i100.1.34.0/30    3.3.3.3                  0    100      0 ?\n"
          "*>i100.1.211.0/30   2.2.2.2                  0    100      0 ?\n"
          "*> 172.31.1.0/24    100.1.18.2               0         32768 ?\n"
          "*>i172.31.2.0/24    2.2.2.2                 65    100      0 ?\n"
          "*>i172.31.3.0/24    3.3.3.3            2172416    100      0 ?")
RT_A = ("Routing Table: VRFA\n"
        "Codes: C - connected, S - static, R - RIP, B - BGP, D - EIGRP, O - OSPF   (légende complète dans la capture)\n\n"
        "Gateway of last resort is not set\n\n"
        "     100.0.0.0/30 is subnetted, 4 subnets\n"
        "B       100.1.32.0 [200/0] via 3.3.3.3, 00:09:52\n"
        "B       100.1.34.0 [200/0] via 3.3.3.3, 00:09:52\n"
        "C       100.1.16.0 is directly connected, Serial1/1\n"
        "B       100.1.209.0 [200/0] via 2.2.2.2, 00:09:52\n"
        "     172.31.0.0/24 is subnetted, 1 subnets\n"
        "B       172.31.3.0 [200/2172416] via 3.3.3.3, 00:09:52\n"
        "R    192.168.1.0/24 [120/1] via 100.1.16.2, 00:00:01, Serial1/1\n"
        "B    192.168.2.0/24 [200/1] via 2.2.2.2, 00:09:52\n"
        "B    192.168.3.0/24 [200/1] via 3.3.3.3, 00:09:52")
RT_C = ("Routing Table: VRFC\n"
        "Codes: C - connected, S - static, R - RIP, B - BGP, D - EIGRP, O - OSPF   (légende complète dans la capture)\n\n"
        "Gateway of last resort is not set\n\n"
        "     100.0.0.0/30 is subnetted, 4 subnets\n"
        "C       100.1.34.0 is directly connected, Serial1/3\n"
        "B       100.1.16.0 [200/0] via 1.1.1.1, 00:24:09\n"
        "B       100.1.18.0 [200/0] via 1.1.1.1, 00:24:09\n"
        "B       100.1.211.0 [200/0] via 2.2.2.2, 00:24:09\n"
        "     172.31.0.0/24 is subnetted, 3 subnets\n"
        "D       172.31.3.0 [90/2172416] via 100.1.34.2, 00:24:57, Serial1/3\n"
        "B       172.31.2.0 [200/65] via 2.2.2.2, 00:24:09\n"
        "B       172.31.1.0 [200/0] via 1.1.1.1, 00:24:09\n"
        "B    192.168.1.0/24 [200/1] via 1.1.1.1, 00:24:09")
RT_R6 = ("Gateway of last resort is not set\n\n"
         "     100.0.0.0/30 is subnetted, 4 subnets\n"
         "R       100.1.32.0 [120/1] via 100.1.16.1, 00:00:11, Serial1/0\n"
         "R       100.1.34.0 [120/1] via 100.1.16.1, 00:00:11, Serial1/0\n"
         "C       100.1.16.0 is directly connected, Serial1/0\n"
         "R       100.1.209.0 [120/1] via 100.1.16.1, 00:00:11, Serial1/0\n"
         "     172.31.0.0/24 is subnetted, 1 subnets\n"
         "R       172.31.3.0 [120/1] via 100.1.16.1, 00:00:11, Serial1/0\n"
         "C    192.168.1.0/24 is directly connected, FastEthernet0/0\n"
         "R    192.168.2.0/24 [120/1] via 100.1.16.1, 00:00:11, Serial1/0\n"
         "R    192.168.3.0/24 [120/1] via 100.1.16.1, 00:00:11, Serial1/0")
TRACE = ("Type escape sequence to abort.\nTracing the route to 192.168.3.1\n\n"
         "  1 100.1.16.1 120 msec 60 msec 112 msec\n"
         "  2 10.1.14.2 [MPLS: Labels 20/23 Exp 0] 460 msec 604 msec 680 msec\n"
         "  3 10.1.45.2 [MPLS: Labels 18/23 Exp 0] 540 msec 616 msec 508 msec\n"
         "  4 100.1.32.1 [MPLS: Label 23 Exp 0] 600 msec 396 msec 504 msec\n"
         "  5 100.1.32.2 420 msec 552 msec 480 msec")
ISAKMP = ("dst             src             state          conn-id slot status\n"
          "172.18.0.1      172.16.0.1      QM_IDLE              1    0 ACTIVE")
IPSEC = ("interface: Serial1/0\n"
         "    Crypto map tag: CMAP-PFA, local addr 172.16.0.1\n\n"
         "   local  ident (addr/mask/prot/port): (172.16.0.0/255.255.0.0/0/0)\n"
         "   remote ident (addr/mask/prot/port): (172.18.0.0/255.255.0.0/0/0)\n"
         "   current_peer 172.18.0.1 port 500\n"
         "     PERMIT, flags={origin_is_acl,}\n"
         "    #pkts encaps: 8, #pkts encrypt: 8, #pkts digest: 8\n"
         "    #pkts decaps: 8, #pkts decrypt: 8, #pkts verify: 8\n"
         "    #pkts compressed: 0, #pkts decompressed: 0\n"
         "    #send errors 2, #recv errors 0\n\n"
         "     local crypto endpt.: 172.16.0.1, remote crypto endpt.: 172.18.0.1\n"
         "     path mtu 1500, ip mtu 1500, ip mtu idb Serial1/0\n"
         "     inbound esp sas:\n"
         "       transform: esp-256-aes esp-sha-hmac")

def cap(fr, en): return (fr, en)

# ------------------------------------------------------------------ HTML : topologie
def topo(i):
    t = lambda fr, en: (fr, en)[i]
    pe = {"R1": (230, 250), "R2": (450, 150), "R3": (670, 250)}
    p = {"R4": (370, 300), "R5": (530, 300)}
    ce = [("R6", "A1", "A", (90, 130), "R1", "RIPv2"), ("R7", "B1", "B", (60, 250), "R1", "EIGRP 20"), ("R8", "C1", "C", (100, 375), "R1", t("Statique", "Static")),
          ("R9", "A2", "A", (300, 50), "R2", "RIPv2"), ("R10", "B2", "B", (450, 45), "R2", t("Statique", "Static")), ("R11", "C2", "C", (600, 50), "R2", "OSPF 3"),
          ("R12", "A3", "A", (810, 130), "R3", "RIPv2"), ("R13", "B3", "B", (840, 250), "R3", "RIPv2"), ("R14", "C3", "C", (800, 375), "R3", "EIGRP 30")]
    s = ['<svg class="m-svg" viewBox="0 0 900 470" role="img" aria-label="%s">' % e(t("Topologie MPLS L3VPN : 3 PE, 2 P, 9 CE", "MPLS L3VPN topology: 3 PE, 2 P, 9 CE"))]
    s.append('<ellipse cx="450" cy="255" rx="285" ry="125" class="m-core"/><text x="450" y="352" class="m-ct" text-anchor="middle">%s</text>' % e(t("Cœur opérateur · OSPF 1 · MPLS / LDP · AS 1", "Provider core · OSPF 1 · MPLS / LDP · AS 1")))
    for a, b in [("R1", "R4"), ("R2", "R4"), ("R4", "R5"), ("R2", "R5"), ("R3", "R5")]:
        A = {**pe, **p}[a]; B = {**pe, **p}[b]
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="m-lk"/>' % (*A, *B))
    for n, site, c, (x, y), pen, proto in ce:
        X, Y = pe[pen]
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" class="m-pe"/>' % (x, y, X, Y, CL[c]))
        s.append('<text x="%d" y="%d" class="m-pl" text-anchor="middle">%s</text>' % ((x + X) / 2, (y + Y) / 2 - 4, e(proto)))
    # extranet + ipsec + paquet
    s.append('<path d="M90 130 L230 250 L370 300 L530 300 L670 250 L800 375" class="m-ext"/>')
    s.append('<path d="M60 270 Q450 520 840 270" class="m-ipsec"/>')
    s.append('<text x="450" y="446" class="m-it" text-anchor="middle">%s</text>' % e(t("Tunnel IPsec ESP · B1 ↔ B3", "IPsec ESP tunnel · B1 ↔ B3")))
    for n, (x, y) in pe.items():
        s.append('<rect x="%d" y="%d" width="50" height="34" rx="8" class="m-pe-b"/><text x="%d" y="%d" class="m-n" text-anchor="middle">%s</text><text x="%d" y="%d" class="m-s" text-anchor="middle">PE</text>' % (x - 25, y - 17, x, y + 4, n, x, y + 30))
    for n, (x, y) in p.items():
        s.append('<circle cx="%d" cy="%d" r="19" class="m-p-b"/><text x="%d" y="%d" class="m-n" text-anchor="middle">%s</text><text x="%d" y="%d" class="m-s" text-anchor="middle">P</text>' % (x, y, x, y + 4, n, x, y + 34))
    for n, site, c, (x, y), pen, proto in ce:
        s.append('<circle cx="%d" cy="%d" r="19" fill="#0b101c" stroke="%s" stroke-width="2.5"/><text x="%d" y="%d" class="m-n" text-anchor="middle">%s</text><text x="%d" y="%d" class="m-site" fill="%s" text-anchor="middle">%s</text>' % (x, y, CL[c], x, y + 4, n, x, y - 26 if y < 300 else y + 36, CL[c], site))
    s.append('<g><circle r="6" class="m-pkt"><animateMotion dur="4.2s" repeatCount="indefinite" path="M90 130 L230 250 L370 300 L530 300 L670 250 L810 130"/></circle></g>')
    s.append('</svg>')
    leg = ('<div class="m-leg"><span><i style="background:%s"></i>%s</span><span><i style="background:%s"></i>%s</span><span><i style="background:%s"></i>%s</span>'
           '<span><i class="m-dash x"></i>%s</span><span><i class="m-dash v"></i>%s</span><span><i class="m-dot"></i>%s</span></div>') % (
        CL["A"], t("Client A", "Customer A"), CL["B"], t("Client B", "Customer B"), CL["C"], t("Client C", "Customer C"),
        t("Extranet A1 ↔ C3 (RT 1:400)", "Extranet A1 ↔ C3 (RT 1:400)"), t("IPsec B1 ↔ B3", "IPsec B1 ↔ B3"), t("Paquet A1 → A3 (labels LDP / VPN)", "A1 → A3 packet (LDP / VPN labels)"))
    note = '<p class="fine">%s</p>' % t(
        "14 routeurs Cisco 7200 sous GNS3 : 3 PE (R1–R3), 2 P (R4–R5), 9 CE (R6–R14). Le routeur P ne connaît aucune route client : il commute uniquement sur le label externe.",
        "14 Cisco 7200 routers in GNS3: 3 PE (R1–R3), 2 P (R4–R5), 9 CE (R6–R14). The P routers know no customer route: they switch on the outer label only.")
    return '<div class="doc m-doc">%s%s%s</div>' % (s and "".join(s), leg, note)

def table(head, rows, cls=""):
    h = "".join("<th>%s</th>" % e(x) for x in head)
    b = "".join("<tr>%s</tr>" % "".join("<td%s>%s</td>" % (' class="m"' if j == 0 else "", c) for j, c in enumerate(r)) for r in rows)
    return '<table class="tb %s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (cls, h, b)

def addr(i):
    t = lambda fr, en: (fr, en)[i]
    links = [("R1 – R4", "10.1.14.0/30", ".1", ".2"), ("R2 – R4", "10.1.24.0/30", ".1", ".2"), ("R4 – R5", "10.1.45.0/30", ".1", ".2"),
             ("R2 – R5", "10.1.25.0/30", ".1", ".2"), ("R3 – R5", "10.1.35.0/30", ".1", ".2")]
    sites = [("A1", "R6", "R1", "100.1.16.0/30", "192.168.1.0/24", "RIPv2"), ("B1", "R7", "R1", "100.1.17.0/30", "172.16.0.0/16", "EIGRP 20"),
             ("C1", "R8", "R1", "100.1.18.0/30", "172.31.1.0/24", t("Statique", "Static")), ("A2", "R9", "R2", "100.1.209.0/30", "192.168.2.0/24", "RIPv2"),
             ("B2", "R10", "R2", "100.1.210.0/30", "172.17.0.0/16", t("Statique", "Static")), ("C2", "R11", "R2", "100.1.211.0/30", "172.31.2.0/24", "OSPF 3"),
             ("A3", "R12", "R3", "100.1.32.0/30", "192.168.3.0/24", "RIPv2"), ("B3", "R13", "R3", "100.1.33.0/30", "172.18.0.0/16", "RIPv2"),
             ("C3", "R14", "R3", "100.1.34.0/30", "172.31.3.0/24", "EIGRP 30")]
    return ('<div class="doc"><h5>%s</h5>%s<p class="fine">%s</p><h5 style="margin-top:20px">%s</h5>%s</div>') % (
        t("Dorsale opérateur (séries /30)", "Provider backbone (/30 serial links)"),
        table([t("Liaison", "Link"), t("Réseau", "Network"), t("Extrémité 1", "End 1"), t("Extrémité 2", "End 2")], links),
        t("Bouclages : R1 1.1.1.1 · R2 2.2.2.2 · R3 3.3.3.3 (sessions BGP et LSP).", "Loopbacks: R1 1.1.1.1 · R2 2.2.2.2 · R3 3.3.3.3 (BGP sessions and LSPs)."),
        t("Sites clients et routage PE–CE", "Customer sites and PE–CE routing"),
        table([t("Site", "Site"), "CE", "PE", t("Liaison PE–CE", "PE–CE link"), "LAN", t("Routage", "Routing")], sites))

def vrfrt(i):
    t = lambda fr, en: (fr, en)[i]
    rows = [("VRFA", "1:10", "1:100", t("1:400 sur R1 uniquement (site A1)", "1:400 on R1 only (site A1)")),
            ("VRFB", "1:20", "1:200", "—"),
            ("VRFC", "1:30", "1:300", t("1:400 sur R3 uniquement (site C3)", "1:400 on R3 only (site C3)"))]
    return ('<div class="doc"><h5>%s</h5>%s<ul style="margin-top:16px"><li>%s</li><li>%s</li><li>%s</li></ul></div>') % (
        t("VRF, Route Distinguishers et Route Targets", "VRFs, Route Distinguishers and Route Targets"),
        table(["VRF", "RD", t("RT de base", "Base RT"), t("RT d'extranet", "Extranet RT")], rows),
        t("Le RD rend chaque préfixe unique (VPNv4) ; le RT décide quelles VRF importent quelles routes.", "The RD makes every prefix unique (VPNv4); the RT decides which VRF imports which routes."),
        t("Le RT de base relie les trois sites d'un même client.", "The base RT links the three sites of a given customer."),
        t("Le RT 1:400, exporté et importé uniquement par la VRFA de R1 et la VRFC de R3, ouvre un extranet A1 ↔ C3 et rien d'autre.", "RT 1:400, exported and imported only by R1's VRFA and R3's VRFC, opens an A1 ↔ C3 extranet and nothing else."))

def matrix(i):
    t = lambda fr, en: (fr, en)[i]
    S9 = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
    ok = lambda a, b: (a[0] == b[0] and a != b) or {a, b} == {"A1", "C3"}
    head = "<th></th>" + "".join('<th class="c%s">%s</th>' % (s[0], s) for s in S9)
    rows = ""
    for a in S9:
        rows += '<tr><th class="c%s">%s</th>' % (a[0], a)
        for b in S9:
            rows += '<td class="dg">•</td>' if a == b else ('<td class="y%s">✓</td>' % (" x" if {a, b} == {"A1", "C3"} else "") if ok(a, b) else '<td class="n">—</td>')
        rows += "</tr>"
    return ('<div class="doc"><h5>%s</h5><table class="m-mx"><thead><tr>%s</tr></thead><tbody>%s</tbody></table><p class="fine">%s</p></div>') % (
        t("Matrice des flux attendus (✓ autorisé · — interdit)", "Expected flow matrix (✓ allowed · — denied)"), head, rows,
        t("L'extranet est volontairement restreint : A1 voit C3, mais A2 et A3 ne le voient pas, et C1 comme C2 ne voient aucun site du client A.",
          "The extranet is deliberately narrow: A1 sees C3, but A2 and A3 do not, and neither C1 nor C2 sees any customer-A site."))

# ------------------------------------------------------------------ HTML : config
def code(txt): return '<pre class="m-code">%s</pre>' % e(txt)
def cfg_vpn(i):
    t = lambda fr, en: (fr, en)[i]
    vrf = ("ip vrf VRFA\n  rd 1:10\n  route-target export 1:100\n  route-target export 1:400\n  route-target import 1:100\n  route-target import 1:400\n!\n"
           "interface Serial1/1\n  ip vrf forwarding VRFA\n  ip address 100.1.16.1 255.255.255.252")
    bgp = ("router bgp 1\n neighbor 2.2.2.2 remote-as 1\n neighbor 2.2.2.2 update-source Loopback0\n neighbor 3.3.3.3 remote-as 1\n neighbor 3.3.3.3 update-source Loopback0\n !\n"
           " address-family vpnv4\n  neighbor 2.2.2.2 activate\n  neighbor 2.2.2.2 send-community extended\n  neighbor 3.3.3.3 activate\n  neighbor 3.3.3.3 send-community extended")
    mpls = "mpls label protocol ldp\n!\ninterface Serial1/0\n  mpls ip      ! %s" % t("uniquement sur la dorsale", "backbone only")
    return ('<div class="doc two"><div><h5>%s</h5>%s<h5>%s</h5>%s</div><div><h5>%s</h5>%s<p class="fine">%s</p></div></div>') % (
        t("VRF sur le PE R1 (extrait)", "VRF on PE R1 (excerpt)"), code(vrf), t("MPLS / LDP", "MPLS / LDP"), code(mpls),
        t("MP-BGP entre PE (iBGP, AS 1)", "MP-BGP between PEs (iBGP, AS 1)"), code(bgp),
        t("Maillage iBGP complet entre bouclages ; sans « send-community extended », les RT ne seraient pas transmis.", "Full iBGP mesh between loopbacks; without “send-community extended” the RTs would not be advertised."))

def cfg_pece(i):
    t = lambda fr, en: (fr, en)[i]
    rip = "! PE R1\nrouter rip\n  address-family ipv4 vrf VRFA\n   redistribute bgp 1 metric 1\n   network 100.0.0.0\n   no auto-summary\n   version 2\n!\nrouter bgp 1\n  address-family ipv4 vrf VRFA\n   redistribute connected\n   redistribute rip"
    eig = "! PE R3\nrouter eigrp 1\n  address-family ipv4 vrf VRFC\n   redistribute bgp 1 metric 1500 200 250 1 1500\n   network 100.0.0.0\n   autonomous-system 30\n!\nrouter bgp 1\n  address-family ipv4 vrf VRFC\n   redistribute eigrp 30"
    osp = "! PE R2\nrouter ospf 3 vrf VRFC\n  redistribute bgp 1 metric 1500 subnets\n  network 100.1.211.0 0.0.0.3 area 0\n!\nrouter bgp 1\n  address-family ipv4 vrf VRFC\n   redistribute ospf 3 vrf VRFC"
    sta = "! PE R1\nip route vrf VRFC 172.31.1.0 255.255.255.0 100.1.18.2\nrouter bgp 1\n address-family ipv4 vrf VRFC\n  redistribute connected\n  redistribute static\n! CE R8\nip route 0.0.0.0 0.0.0.0 100.1.18.1"
    return ('<div class="doc"><div class="m-grid2"><div><h5>RIPv2 · A1, A2, A3, B3</h5>%s</div><div><h5>EIGRP · B1, C3</h5>%s</div>'
            '<div><h5>OSPF · C2</h5>%s</div><div><h5>%s · C1, B2</h5>%s</div></div>'
            '<p class="fine">%s</p></div>') % (code(rip), code(eig), code(osp), t("Routage statique", "Static routing"), code(sta),
            t("Même principe dans les 4 cas : le protocole est instancié dans la VRF, ses routes sont redistribuées dans BGP, et les routes BGP des autres sites reviennent vers le CE.",
              "Same principle in all 4 cases: the protocol runs inside the VRF, its routes are redistributed into BGP, and the other sites' BGP routes come back to the CE."))

# ------------------------------------------------------------------ HTML : Wireshark
def wshark(i, kind):
    t = lambda fr, en: (fr, en)[i]
    if kind == "A":
        tree = ('<div class="m-w"><div class="r">▸ Cisco HDLC</div>'
                '<div class="r">▸ MultiProtocol Label Switching Header, <b>Label: 18</b>, Exp: 0, S: 0, TTL: 253</div>'
                '<div class="r">▾ MultiProtocol Label Switching Header, <b>Label: 23</b>, Exp: 0, S: 1, TTL: 254</div>'
                '<div class="r in">MPLS Label: 23 · Bottom Of Label Stack: 1 · TTL: 254</div>'
                '<div class="r">▸ Internet Protocol Version 4, Src: <b>192.168.1.1</b>, Dst: <b>192.168.3.1</b></div>'
                '<div class="r">▾ Internet Control Message Protocol</div>'
                '<div class="r in">Type: Echo (ping) request (8) · Code: 0 · Checksum: 0x36b6 [correct]</div>'
                '<div class="r in">Identifier (BE): 8 · Sequence Number (BE): 0</div>'
                '<div class="r in ok">Data (72 bytes): abcdabcdabcdabcd…</div></div>')
        info = "No.: 354 · Source: 192.168.1.1 · Destination: 192.168.3.1 · Info: Echo (ping) request"
        tag = t("Client A — sans IPsec : contenu lisible", "Customer A — no IPsec: readable payload")
    else:
        tree = ('<div class="m-w"><div class="r">▸ Cisco HDLC</div>'
                '<div class="r">▸ MultiProtocol Label Switching Header, <b>Label: 18</b>, Exp: 0, S: 0, TTL: 253</div>'
                '<div class="r">▸ MultiProtocol Label Switching Header, <b>Label: 25</b>, Exp: 0, S: 1, TTL: 254</div>'
                '<div class="r">▸ Internet Protocol Version 4, Src: <b>172.16.0.1</b>, Dst: <b>172.18.0.1</b></div>'
                '<div class="r">▾ Encapsulating Security Payload</div>'
                '<div class="r in">ESP SPI: 0xfe77437d (4269228925)</div>'
                '<div class="r in">ESP Sequence: 1</div>'
                '<div class="m-enc">%s</div></div>') % e(t("contenu chiffré — illisible", "encrypted payload — unreadable"))
        info = "No.: 561 · Source: 172.16.0.1 · Destination: 172.18.0.1 · Protocol: ESP · Length: 180 · Info: ESP (SPI=0xfe77437d)"
        tag = t("Client B — IPsec : paquet ESP chiffré", "Customer B — IPsec: encrypted ESP packet")
    note = t("Capture sur le lien R4–R5 du cœur. Double label MPLS : transport LDP (18) puis label VPN (%s). Le label de transport est le même pour les deux clients (même PE de sortie, R3).",
             "Capture on the R4–R5 core link. Double MPLS label: LDP transport (18) then VPN label (%s). The transport label is identical for both customers (same egress PE, R3).") % ("23" if kind == "A" else "25")
    return '<div class="doc"><div class="m-wh"><span class="m-tag %s">%s</span><span>Wireshark</span></div>%s<div class="m-wi">%s</div><p class="fine">%s</p></div>' % (kind, e(tag), tree, e(info), note)

# ------------------------------------------------------------------ HTML : résultats
def results(i):
    t = lambda fr, en: (fr, en)[i]
    ok = t("Succès", "Success"); ko = t("Échec", "Failure")
    T = [("VPN A", "A1", "A3", 1), ("VPN A", "A1", "A2", 1), ("VPN B", "B1", "B3", 1), ("VPN B", "B1", "B2", 1), ("VPN C", "C1", "C2", 1), ("VPN C", "C1", "C3", 1),
         (t("Extranet", "Extranet"), "A1", "C3", 1), (t("Extranet (retour)", "Extranet (return)"), "C3", "A1", 1),
         (t("Isolation", "Isolation"), "A1", "C1", 0), (t("Isolation", "Isolation"), "A1", "B3", 0), (t("Isolation", "Isolation"), "A3", "C3", 0), (t("Isolation", "Isolation"), "A3", "B1", 0),
         (t("Isolation", "Isolation"), "B1", "A1", 0), (t("Isolation", "Isolation"), "B1", "C3", 0), (t("Isolation", "Isolation"), "C1", "A1", 0),
         (t("Isolation", "Isolation"), "C1", "B1", 0), (t("Isolation", "Isolation"), "C3", "B1", 0)]
    rows = [(n, "%s → %s" % (a, b), ok if r else ko, "100 %" if r else "0 %", '<span class="pill g">✔ %s</span>' % t("conforme", "as expected")) for n, a, b, r in T]
    return ('<div class="doc"><div class="big"><b>17 / 17</b><span>%s</span></div>%s<p class="fine">%s</p></div>') % (
        t("tests conformes à la matrice des flux", "tests matching the flow matrix"),
        table([t("Test", "Test"), t("Flux", "Flow"), t("Attendu", "Expected"), t("Obtenu", "Obtained"), ""], rows),
        t("Temps de réponse de 300 à 600 ms : ils viennent de l'émulation de 14 routeurs sur une seule machine, pas de l'architecture. Tests rejoués après sécurisation (MD5, limites de routes, IPsec) : aucune régression.",
          "Response times of 300–600 ms come from emulating 14 routers on a single machine, not from the architecture. Tests replayed after hardening (MD5, route limits, IPsec): no regression."))

def bilan(i):
    t = lambda fr, en: (fr, en)[i]
    obj = [(t("Cœur MPLS fonctionnel (OSPF + LDP)", "Working MPLS core (OSPF + LDP)"), "4.2 – 4.4"), (t("Un VPN par client (VRF + MP-BGP)", "One VPN per customer (VRF + MP-BGP)"), "4.5 – 4.7"),
           (t("4 modes de routage PE–CE", "4 PE–CE routing modes"), "4.8 – 4.10"), (t("Extranet A1 ↔ C3", "A1 ↔ C3 extranet"), "6.4"), (t("Isolation entre clients", "Customer isolation"), "6.6"),
           (t("Authentification MD5 de la dorsale", "MD5 authentication of the backbone"), "5.1 – 5.2"), (t("Limite de routes par VRF", "Route limit per VRF"), "5.3"), (t("Chiffrement IPsec B1 ↔ B3", "IPsec encryption B1 ↔ B3"), "5.4 – 5.7")]
    lim = [t("Chiffrement partiel (B1–B3 seulement)", "Partial encryption (B1–B3 only)"), t("MD5 : algorithme ancien, secrets statiques", "MD5: legacy algorithm, static secrets"),
           t("Clé IPsec prépartagée (labo)", "Pre-shared IPsec key (lab)"), t("Un seul PE par site : redondance partielle", "One PE per site: partial redundancy"),
           t("Maillage iBGP : pas d'échelle (route reflectors)", "iBGP full mesh: does not scale (route reflectors)"), t("Environnement émulé", "Emulated environment")]
    nxt = [t("IPsec généralisé + certificats", "IPsec everywhere + certificates"), t("SHA / TCP-AO", "SHA / TCP-AO"), t("Route reflectors", "Route reflectors"), "BFD · MPLS-TE · QoS", t("Supervision SNMP / NetFlow", "SNMP / NetFlow monitoring"), "6VPE"]
    return ('<div class="doc two"><div><h5>%s</h5>%s</div><div><h5>%s</h5><div class="pills">%s</div><h5>%s</h5><div class="pills">%s</div></div></div>') % (
        t("Objectifs atteints (8 / 8)", "Objectives achieved (8 / 8)"),
        table([t("Objectif", "Objective"), t("Preuve (§ rapport)", "Evidence (report §)")], [(a, '<span class="pill g">✔</span> %s' % b) for a, b in obj]),
        t("Limites assumées", "Acknowledged limits"), "".join("<span>%s</span>" % x for x in lim),
        t("Perspectives", "Next steps"), "".join("<span>%s</span>" % x for x in nxt))

# ------------------------------------------------------------------ assemblage
def D(label, f, shot=None, cp=None): return DOC(label, f(0), f(1), shot, cp)

MPLS = dict(
    host="mpls-lab", logo="MPLS", sub="GNS3 · Cisco 7200 · 14 routeurs", accent="#38bdf8",
    wall="radial-gradient(ellipse at 15% 10%,#0b3550 0,transparent 55%),radial-gradient(ellipse at 90% 95%,#2a1b5c 0,transparent 55%),#0a1020",
    boot=[],
    apps=[
        dict(id="topo", icon="i-net", name=("Topologie", "Topology"), chrome="plain", title=("GNS3 — PFA-Project", "GNS3 — PFA-Project"), tabs=[
            DOC(("Topologie", "Topology"), topo(0), topo(1), "mpls-01-topologie-gns3.png", ("Topologie complète sous GNS3 (capture du rapport).", "Full topology in GNS3 (report screenshot).")),
            DOC(("Adressage", "Addressing"), addr(0), addr(1)),
            DOC(("VRF · RD · RT", "VRF · RD · RT"), vrfrt(0), vrfrt(1)),
            DOC(("Matrice des flux", "Flow matrix"), matrix(0), matrix(1)),
        ]),
        dict(id="core", icon="i-term", name=("Dorsale", "Backbone"), chrome="term", title="R4 / R1 — console", tabs=[
            TERM(("Interfaces PE", "PE interfaces"), [R("R1", "show ip interface brief"), O(IFB)], "mpls-02-interfaces-pe-r1.png", ("État des interfaces du PE R1.", "Interface state of PE R1.")),
            TERM(("OSPF", "OSPF"), [R("R4", "show ip ospf neighbor"), O(OSPFN, "ok")], "mpls-03-ospf-voisins-r4.png", ("Voisinages OSPF à l'état FULL sur le routeur P R4.", "OSPF neighbors in FULL state on P router R4.")),
            TERM(("LDP", "LDP"), [R("R1", "show mpls ldp neighbor"), O(LDPN, "ok")], "mpls-04-ldp-session.png", ("Session LDP opérationnelle entre R1 et R4.", "LDP session operational between R1 and R4.")),
            TERM(("LFIB (R4)", "LFIB (R4)"), [R("R4", "show mpls forwarding-table"), O(LFIB), O(("# R4 commute les labels des bouclages des PE sans connaître aucune route client.", "# R4 switches the PE loopback labels without knowing any customer route."), "dim")],
                 "mpls-05-lfib-r4.png", ("Table de commutation de labels de R4.", "Label forwarding table of R4.")),
        ]),
        dict(id="vpn", icon="i-layers", name=("VPN & BGP", "VPN & BGP"), chrome="plain", title=("Services VPN — PE R1", "VPN services — PE R1"), tabs=[
            D(("Config VRF + BGP", "VRF + BGP config"), cfg_vpn),
            D(("Routage PE–CE", "PE–CE routing"), cfg_pece),
            TERM(("show ip vrf", "show ip vrf"), [R("R1", "show ip vrf"), O(VRFS)], "mpls-06-vrf-r1.png", ("Une VRF par client, rattachée à une interface vers le CE.", "One VRF per customer, bound to an interface towards the CE.")),
            TERM(("Sessions MP-BGP", "MP-BGP sessions"), [R("R1", "show ip bgp vpnv4 all summary"), O(BGPSUM, "ok")], "mpls-07-bgp-vpnv4-summary.png", ("Sessions établies avec R2 et R3 : 6 préfixes reçus de chaque PE.", "Sessions up with R2 and R3: 6 prefixes received from each PE.")),
            TERM(("Table VPNv4", "VPNv4 table"), [R("R1", "show ip bgp vpnv4 all"), O(BGPALL)], "mpls-08-bgp-vpnv4-table.png", ("Table BGP VPNv4 de R1 pour les trois VRF (RD 1:10, 1:20, 1:30).", "R1 VPNv4 BGP table for the three VRFs (RD 1:10, 1:20, 1:30).")),
        ]),
        dict(id="rt", icon="i-db", name=("Routes", "Routes"), chrome="term", title="R1 / R3 / R6 — console", tabs=[
            TERM(("VRFA sur R1", "VRFA on R1"), [R("R1", "show ip route vrf VRFA"), O(RT_A), O(("# C3 (172.31.3.0/24) apparaît dans la VRFA de R1 grâce au RT 1:400.", "# C3 (172.31.3.0/24) shows up in R1's VRFA thanks to RT 1:400."), "dim")],
                 "mpls-09-route-vrfa.png", ("Table de la VRFA sur R1 : sites A2, A3 et, par l'extranet, C3.", "VRFA table on R1: sites A2, A3 and, through the extranet, C3.")),
            TERM(("VRFC sur R3", "VRFC on R3"), [R("R3", "show ip route vrf VRFC"), O(RT_C), O(("# Le réseau de A1 (192.168.1.0/24) apparaît dans la VRFC de R3.", "# A1's network (192.168.1.0/24) shows up in R3's VRFC."), "dim")],
                 "mpls-10-route-vrfc.png", ("Table de la VRFC sur R3 : sites C1, C2 et, par l'extranet, A1.", "VRFC table on R3: sites C1, C2 and, through the extranet, A1.")),
            TERM(("CE R6 (RIP)", "CE R6 (RIP)"), [R("R6", "show ip route"), O(RT_R6)], "mpls-11-route-ce-r6.png", ("Routes apprises en RIP par le CE R6 (site A1).", "Routes learnt through RIP by CE R6 (site A1).")),
        ]),
        dict(id="tests", icon="i-chart", name=("Tests", "Tests"), chrome="term", title="CE — console", tabs=[
            TERM(("Connectivité VPN", "VPN connectivity"),
                 ping("R6", "192.168.3.1", "192.168.1.1", 1, "408/561/756") + ping("R7", "172.18.0.1", "172.16.0.1", 1, "412/472/528") + ping("R8", "172.31.3.1", "172.31.1.1", 1, "460/520/552"),
                 "mpls-18-ping-a1-a3.png", ("A1 → A3, B1 → B3, C1 → C3 : 100 % de réussite (autres tests dans la galerie).", "A1 → A3, B1 → B3, C1 → C3: 100% success (other tests in the gallery).")),
            TERM(("Extranet A1 ↔ C3", "A1 ↔ C3 extranet"),
                 ping("R6", "172.31.3.1", "192.168.1.1", 1, "472/577/664") + ping("R14", "192.168.1.1", "172.31.3.1", 1, "372/501/612") + ping("R12", "172.31.3.1", "192.168.3.1", 0),
                 "mpls-24-extranet-a1-c3.png", ("A1 et C3 se joignent ; A3 ne joint pas C3 (extranet restreint à A1).", "A1 and C3 reach each other; A3 cannot reach C3 (extranet limited to A1).")),
            TERM(("Isolation", "Isolation"),
                 ping("R6", "172.31.1.1", "192.168.1.1", 0) + ping("R7", "192.168.1.1", "172.16.0.1", 0, mark="UUUUU") + ping("R8", "172.16.0.1", "172.31.1.1", 0, mark="UUUUU") + ping("R14", "172.16.0.1", "172.31.3.1", 0),
                 "mpls-26-isolation-a1-c1.png", ("Échecs attendus : aucun client ne voit les sites d'un autre (U = unreachable).", "Expected failures: no customer sees another customer's sites (U = unreachable).")),
            TERM(("Chemin MPLS", "MPLS path"), [R("R6", "traceroute 192.168.3.1 source FastEthernet0/0"), O(TRACE),
                 O(("# R1 impose le label VPN (23) puis le label LDP (20) ; R5 retire le label externe (PHP) ; R3 lit le label VPN et remet le paquet IP à R12.",
                    "# R1 pushes the VPN label (23) then the LDP label (20); R5 pops the outer label (PHP); R3 reads the VPN label and hands the IP packet to R12."), "dim")],
                 "mpls-35-traceroute-labels.png", ("Traceroute A1 → A3 : labels MPLS visibles dans le cœur.", "A1 → A3 traceroute: MPLS labels visible in the core.")),
        ]),
        dict(id="sec", icon="i-shield", name=("Sécurité", "Security"), chrome="term", title=("Sécurisation de la dorsale", "Backbone hardening"), tabs=[
            TERM(("MD5 (OSPF/LDP/BGP)", "MD5 (OSPF/LDP/BGP)"), [
                O(("# Authentification MD5 des 5 routeurs de la dorsale — secrets de laboratoire non affichés", "# MD5 authentication on the 5 backbone routers — lab secrets not shown"), "dim"),
                R("R1", "show ip ospf interface Serial1/0 | include authentication"), O("  Message digest authentication enabled", "ok"),
                R("R1", "show running-config | include neighbor .* password"),
                O("mpls ldp neighbor 10.1.45.1 password 7 ••••••••••••••••••••\n neighbor 2.2.2.2 password 7 ••••••••••••••••••••\n neighbor 3.3.3.3 password 7 ••••••••••••••••••••"),
                O(("# service password-encryption : les secrets sont stockés chiffrés (type 7) ; sessions rétablies : OSPF FULL, LDP Oper, BGP 6 préfixes par PE.", "# service password-encryption: secrets are stored encrypted (type 7); sessions re-established: OSPF FULL, LDP Oper, BGP 6 prefixes per PE."), "dim")],
                "mpls-12-md5-ospf.png", ("Authentification par condensat activée sur Serial1/0 de R1.", "Digest authentication enabled on R1 Serial1/0.")),
            TERM(("Limite de routes", "Route limit"), [R("R1", "show running-config | include maximum"), O(" maximum routes 100 80\n maximum routes 100 80\n maximum routes 100 80"),
                O(("# 100 routes max par VRF, alerte à 80 % : un client ne peut pas saturer le PE.", "# 100 routes max per VRF, warning at 80%: a customer cannot saturate the PE."), "dim")],
                "mpls-13-max-routes.png", ("Limites de routes configurées sur les trois VRF de R1.", "Route limits configured on the three VRFs of R1.")),
            TERM(("IPsec B1 ↔ B3", "IPsec B1 ↔ B3"), [
                O(("# AES-256 / SHA, clé prépartagée (non affichée), mode tunnel — trafic protégé 172.16.0.0/16 ↔ 172.18.0.0/16", "# AES-256 / SHA, pre-shared key (not shown), tunnel mode — protected traffic 172.16.0.0/16 ↔ 172.18.0.0/16"), "dim"),
                R("R7", "show crypto isakmp sa"), O(ISAKMP, "ok"), R("R7", "show crypto ipsec sa"), O(IPSEC)],
                "mpls-15-ipsec-sa.png", ("Compteurs IPsec sur R7 : paquets chiffrés et déchiffrés sans erreur.", "IPsec counters on R7: packets encrypted and decrypted with no error.")),
            DOC(("Wireshark : client A", "Wireshark: customer A"), wshark(0, "A"), wshark(1, "A"), "mpls-16-wireshark-clair.png", ("Lien R4–R5, client A (sans IPsec) : paquet ICMP lisible.", "R4–R5 link, customer A (no IPsec): readable ICMP packet.")),
            DOC(("Wireshark : client B", "Wireshark: customer B"), wshark(0, "B"), wshark(1, "B"), "mpls-17-wireshark-esp.png", ("Lien R4–R5, client B (IPsec) : paquet ESP au contenu chiffré.", "R4–R5 link, customer B (IPsec): ESP packet with encrypted payload.")),
        ]),
        dict(id="res", icon="i-doc", name=("Résultats", "Results"), chrome="plain", title=("Résultats & bilan", "Results & outcome"), tabs=[
            D(("17 tests", "17 tests"), results), D(("Bilan & limites", "Outcome & limits"), bilan),
        ]),
    ])
