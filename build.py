#!/usr/bin/env python3
"""Educore site generator. Renders every page into ./site from shared layout + content.
Run:  python3 build.py
"""
import json, os, re, html
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "site"
SRC = ROOT.parent / ".edu-src"
IMG = "assets/img/"
import time
ASSET_V = int(time.time())

# ---------------------------------------------------------------- icons
P = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "chev": '<path d="m6 9 6 6 6-6"/>',
 "chevr": '<path d="m9 6 6 6-6 6"/>',
 "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
 "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
 "users": '<path d="M16 20v-1.5A3.5 3.5 0 0 0 12.5 15h-5A3.5 3.5 0 0 0 4 18.5V20"/><circle cx="10" cy="8" r="3.5"/><path d="M20 20v-1.5a3.5 3.5 0 0 0-2.5-3.35M15.5 4.6a3.5 3.5 0 0 1 0 6.8"/>',
 "staff": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
 "school": '<path d="M3 10 12 5l9 5-9 5z"/><path d="M7 12.5V17c0 1 2.2 3 5 3s5-2 5-3v-4.5M21 10v6"/>',
 "baby": '<circle cx="12" cy="8" r="4"/><path d="M5 21a7 7 0 0 1 14 0"/><path d="M10 8h.01M14 8h.01"/>',
 "building": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1M10 21v-3h4v3"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/>',
 "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 "funnel": '<path d="M3 4h18l-7 8.5V19l-4 2v-8.5z"/>',
 "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
 "id": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.5"/><path d="M5.5 16.5a3.5 3.5 0 0 1 7 0M15 10h3M15 14h3"/>',
 "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>',
 "chart": '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 6-6"/>',
 "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M12 12v2"/>',
 "wallet": '<rect x="3" y="6" width="18" height="14" rx="2"/><path d="M16 13h.01M3 10h18M6 6V4h12v2"/>',
 "tools": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
 "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
 "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>',
 "form": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
 "team": '<circle cx="12" cy="7" r="3"/><circle cx="5" cy="10" r="2"/><circle cx="19" cy="10" r="2"/><path d="M7 21v-2a5 5 0 0 1 10 0v2M2 20v-1a3 3 0 0 1 3-3M22 20v-1a3 3 0 0 0-3-3"/>',
 "grad": '<path d="M22 10 12 5 2 10l10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
 "qr": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3M21 14v.01M14 21h3M21 17v4h-4"/>',
 "award": '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 8 5-3 5 3-1.5-8"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
 "lang": '<path d="M4 5h8M8 3v2M6 5c0 4 3 7 6 8M10 5c0 3-3 7-6 8"/><path d="m13 21 4-9 4 9M14.5 18h5"/>',
 "headset": '<path d="M3 14v-2a9 9 0 0 1 18 0v2"/><rect x="2" y="14" width="5" height="6" rx="2"/><rect x="17" y="14" width="5" height="6" rx="2"/>',
 "puzzle": '<path d="M10 3h4v3a2 2 0 1 0 4 0V3h3v7h-3a2 2 0 1 0 0 4h3v7h-7v-3a2 2 0 1 0-4 0v3H3v-7h3a2 2 0 1 0 0-4H3V3z"/>',
 "bell": '<path d="M6 8a6 6 0 1 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>',
 "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
 "bus": '<rect x="4" y="3" width="16" height="15" rx="3"/><path d="M4 11h16M8 21v-3M16 21v-3M8 15h.01M16 15h.01"/>',
 "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 "map": '<path d="M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 "tel": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 "cloud": '<path d="M17.5 19a4.5 4.5 0 1 0-1-8.9A6 6 0 0 0 5 11.5 4 4 0 0 0 6 19z"/>',
 "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "trend": '<path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
 "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
 "db": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
 "pulse": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/><path d="M3.5 12h4l1.5-3 2.5 6 2-4.5 1 1.5h6"/>',
 "box": '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
 "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 12.4a1.5 1.5 0 0 0 1.5 1.1h8.6a1.5 1.5 0 0 0 1.5-1.1L21 7H6"/>',
 "flow": '<rect x="3" y="3" width="6" height="6" rx="1.5"/><rect x="15" y="15" width="6" height="6" rx="1.5"/><path d="M6 9v4a2 2 0 0 0 2 2h7"/><path d="m12 12 3 3-3 3"/>',
 "flask": '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/>',
}
def ic(name, cls=""):
    return f'<svg{(" class=%s" % cls) if cls else ""} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>'

SOCIAL = {
 "linkedin": ("https://www.linkedin.com/company/ieducore/", '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.6 8.65 21 11.3 21 14.6V21h-4v-5.6c0-1.35-.03-3.08-1.88-3.08-1.88 0-2.17 1.47-2.17 2.98V21H9z"/></svg>'),
 "instagram": ("https://www.instagram.com/educoresystemstechnologies", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/></svg>'),
 "facebook": ("https://www.facebook.com/educoreme", '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 8V6c0-.9.6-1 1-1h2.5V1.1L14.1 1C10.3 1 9.5 3.8 9.5 5.6V8H7v4h2.5v11h4.5V12h3.2l.4-4z"/></svg>'),
 "youtube": ("https://www.youtube.com/@educoresystemstechnologies8012", '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1c.4-1.6.5-3.2.5-4.8s-.1-3.2-.5-4.8zM9.75 15.02V8.98L15.5 12z"/></svg>'),
}
WA = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm8.4-18.2A11.8 11.8 0 0 0 1.7 17.8L0 24l6.3-1.7A11.8 11.8 0 0 0 24 12a11.7 11.7 0 0 0-3.6-8.4z"/></svg>'

# ---------------------------------------------------------------- layout
NAV = [
  ("index", "Home", None),
  ("about", "About", None),
  ("services", "Services", [
     ("early-years", "Early Years", "Curriculum compass for nurseries & ECE", "baby"),
     ("school", "School", "All-in-one school management system", "school"),
     ("education-groups", "Education Institution", "Multi-school control for groups", "building"),
  ]),
  ("features", "Features", None),
  ("modules", "Modules", [
     ("modules-education", "Education", "LMS, Early Years, IB, Attendance, Appointment, Analysis, Library, Digital Library, Timetable, ECA", "book"),
     ("modules-operations", "Operations", "SIS, CRM, Admission, Workflow, Transport, Dismissal, Menu, Withdrawal, Report Center", "gear"),
     ("modules-hr", "HR", "HRM, Recruitment, Payroll, Evaluation, AdminEvaluation, Teams", "team"),
     ("modules-erp", "ERP", "Billing, Finance, Assets, Inventory, Payments, Budgets, Marketplace, External Operations", "db"),
     ("modules-communication", "Communication", "Communicator, Alumni, Chat Monitor, EducoreParent, EducoreTeacher", "chat"),
     ("modules-wellbeing", "Well-being", "Health, SEN, Concerns, SEP", "pulse"),
  ]),
  ("certificates", "Certifications", None),
  ("contact-us", "Contact", None),
]
SERVICE_KEYS = {"services", "early-years", "school", "education-groups"}
MODULE_KEYS = {"modules", "mobile-app", "modules-education", "modules-operations", "modules-hr", "modules-erp", "modules-communication", "modules-wellbeing"}

def href(k): return "index.html" if k == "index" else f"{k}.html"

def header(active):
    items = []
    for key, label, sub in NAV:
        is_active = key == active or (key == "services" and active in SERVICE_KEYS) or (key == "modules" and active in MODULE_KEYS)
        a = ' active' if is_active else ''
        if sub:
            links = "".join(f'<a href="{href(k)}"><span class="ic">{ic(i)}</span><span><b>{t}</b><small>{d}</small></span></a>' for k, t, d, i in sub)
            if key == "modules":
                links += f'<a href="modules.html"><span class="ic">{ic("layers")}</span><span><b>All Modules</b><small>Explore the full Educore suite</small></span></a>'
            wide = " wide" if len(sub) > 4 else ""
            items.append(f'<li class="has-drop"><button type="button" class="nav-link{a}" aria-expanded="false" aria-haspopup="true">{label}{ic("chev")}</button><div class="drop{wide}">{links}</div></li>')
        else:
            items.append(f'<li><a class="nav-link{a}" href="{href(key)}">{label}</a></li>')
    signin = f'''<li class="has-drop"><button type="button" class="nav-link" aria-expanded="false" aria-haspopup="true">Sign In{ic("chev")}</button><div class="drop right">
      <a href="https://academic.educore.io/"><span class="ic">{ic("school")}</span><span><b>School Sign-in</b><small>Staff & administrators</small></span></a>
      <a href="https://parent.educore.io/"><span class="ic">{ic("users")}</span><span><b>Parent / Student Sign-in</b><small>Families & learners</small></span></a></div></li>'''
    mob = []
    for key, label, sub in NAV:
        if sub:
            extra = '<a href="modules.html">All Modules</a>' if key == "modules" else ""
            mob.append(f'<button type="button" class="m-toggle" aria-expanded="false">{label}{ic("chev")}</button><div class="sub">' + "".join(f'<a href="{href(k)}">{t}</a>' for k, t, _, _ in sub) + extra + '</div>')
        else:
            mob.append(f'<a href="{href(key)}">{label}</a>')
    mob.append(f'<button type="button" class="m-toggle" aria-expanded="false">Sign In{ic("chev")}</button><div class="sub"><a href="https://academic.educore.io/">School Sign-in</a><a href="https://parent.educore.io/">Parent / Student Sign-in</a></div>')
    return f'''<div class="progress"></div>
<header class="header"><div class="container"><div class="bar">
  <a class="logo" href="index.html" aria-label="Educore home"><img src="{IMG}logo.png" alt="Educore, Systems and Technologies" width="295" height="102"></a>
  <ul class="nav">{"".join(items)}{signin}</ul>
  <div class="header-cta"><a class="btn btn-sm" href="get-started.html" data-magnetic>Get a Quote {ic("arrow")}</a>
  <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button></div>
</div></div></header>
<nav class="mobile-menu">{"".join(mob)}<a class="btn" href="get-started.html">Get a Quote {ic("arrow")}</a></nav>'''

X_ICON = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.75 3h3.07l-6.7 7.66L22 21h-6.17l-4.83-6.32L5.47 21H2.4l7.17-8.2L2 3h6.33l4.37 5.77zm-1.08 16.2h1.7L7.4 4.73H5.58z"/></svg>'
MAP_URL = "https://www.google.com/maps/search/?api=1&query=Educore+Systems+and+Technologies+Dubai+Silicon+Oasis"

def footer():
    soc = [("facebook", SOCIAL["facebook"][0], SOCIAL["facebook"][1]), ("linkedin", SOCIAL["linkedin"][0], SOCIAL["linkedin"][1]),
           ("X", "#", X_ICON), ("youtube", SOCIAL["youtube"][0], SOCIAL["youtube"][1]), ("instagram", SOCIAL["instagram"][0], SOCIAL["instagram"][1])]
    soc = "".join(f'<a href="{u}"{"" if u == "#" else " target=_blank rel=noopener"} aria-label="{n}">{i}</a>' for n, u, i in soc)
    links = [("index", "Home"), ("about", "About Us"), ("services", "Services"), ("features", "Features"), ("modules", "Modules"), ("terms", "Terms of Service"), ("privacy", "Privacy & Policy")]
    lis = "".join(f'<li><a href="{href(k)}">{ic("chevr")}{t}</a></li>' for k, t in links)
    return f'''<footer class="footer">
<div class="container"><div class="top">
  <div class="f-about">
   <a class="f-logo" href="index.html"><img src="{IMG}footer-logo.png" alt="Educore Systems and Technologies"></a>
   <p>Educore is an educational management system that serves as a core system for nurseries, early learning centers, primary schools and early intervention centers. Flexible enough to cater for any setting, easy to use and backed up by a great team of professionals who fully understand the childcare industry.</p>
   <div class="socials">{soc}</div>
  </div>
  <div class="f-links"><h4>Useful Links</h4><ul>{lis}</ul></div>
  <div class="f-card">
   <a class="f-map" href="{MAP_URL}" target="_blank" rel="noopener" aria-label="Open Educore office in Google Maps"><img src="{IMG}map.png" alt="Map showing Educore Systems and Technologies, Dubai Silicon Oasis" loading="lazy"></a>
   <div class="ci">{ic("map")}<span>Office 703, Wing B,<br>DSO Headquarters Building,<br>Dubai Silicon Oasis, Dubai, United Arab Emirates.</span></div>
   <div class="ci">{ic("tel")}<span>Phone: <a href="tel:+971504051555">+971 50 405 1555</a></span></div>
   <div class="ci">{ic("mail")}<a href="mailto:info@ieducore.com">info@ieducore.com</a></div>
   <a class="btn f-btn" href="contact-us.html">Contact Us</a>
  </div>
 </div>
 <div class="bottom"><span>© <span id="yr">2026</span> Educore Systems and Technologies FZE. All rights reserved.</span></div>
</div></footer>
<div class="fab"><button class="top" aria-label="Back to top">{ic("up")}</button><a class="wa" href="https://wa.me/971504051555" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WA}</a></div>
<div class="toast" role="status">{ic("check")}<span></span></div>
<script>document.getElementById('yr').textContent=new Date().getFullYear()</script>'''

def page(key, title, desc, body):
    full = "Educore, 360° School Management System" if key == "index" else f"{title} · Educore"
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#0B2240">
<meta property="og:title" content="{full}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{IMG}logo.png">
<link rel="icon" href="{IMG}favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={ASSET_V}">
</head><body>
{header(key)}
<main>
{body}
</main>
{footer()}
<script src="assets/js/main.js?v={ASSET_V}" defer></script>
</body></html>'''

# ---------------------------------------------------------------- components
MESH = ''

def crumbs(trail):
    parts = [f'<a href="index.html">Home</a>']
    for k, t in trail:
        parts.append(ic("chevr"))
        parts.append(f'<a href="{href(k)}">{t}</a>' if k else f'<span>{t}</span>')
    return f'<div class="crumbs" data-reveal>{"".join(parts)}</div>'

def phero(trail, eyebrow, title, lead, img=None, actions=True, pills=None, center=False):
    pr = f'<div class="pill-row" data-stagger>{"".join(f"<span class=pill>{p}</span>" for p in pills)}</div>' if pills else ""
    acts = (f'<div class="hero-actions" data-reveal style="--d:.3s"><a class="btn" href="get-started.html" data-magnetic>Get a Quote {ic("arrow")}</a>'
            f'<a class="btn btn-ghost" href="registration.html">Setup School</a></div>') if actions else ""
    art = f'<div class="art" data-reveal="zoom" style="--d:.2s"><img src="{IMG}{img}" alt=""></div>' if img else ""
    return f'''<section class="phero{' center' if center or not img else ''}"><div class="container"><div class="phero-grid">
<div>{crumbs(trail)}
<h1 data-reveal>{title}</h1><p class="lead" data-reveal style="--d:.15s">{lead}</p>{pr}{acts}</div>{art}
</div></div></section>'''

def checks(items, two=False):
    return f'<ul class="checks{" two" if two else ""}" data-stagger>{"".join(f"<li>{i}</li>" for i in items)}</ul>'

def defs(items):
    return '<div class="defs" data-stagger>' + "".join(
        f'<div class="def"><span class="n">{i+1:02d}</span><div><b>{t}</b><p>{d}</p></div></div>' for i, (t, d) in enumerate(items)) + '</div>'

ORIG = {
 "Nurturing ECE education": "Nurturing ECE Education with Educore’s Holistic Curriculum Support",
 "Track & report": "Track Student Progress and Generate Gap Analysis Report Showing Student Attainments",
 "Multi-curriculum management": "Multi-Curriculum Management",
 "Streamline & enhance": "Streamline and Enhance Your School Operations with Educore",
 "Control dashboard": "Active Execution Revolution",
 "Single sign-on": "Protected Access Powerhouse",
 "Educore HR": "Educore HR: A Human Touch with Digital Efficiency",
 "EducoreEY": "EducoreEY: Crafting a Brighter Future for Early Learners",
 "Educore Mobile Apps": "Educore Mobile Apps: Empowering Teachers and Parents",
 "Educore Performance Analysis": "Educore Performance Analysis: Decode the Matrix of Student Grades",
 "From data to decisions": "Grade Analysis",
 "About Educore System": "About Educore System",
}

def split(img, kicker, title, desc="", body="", rev=False, badges=None, soft=False, cta=None):
    fb = ""
    if badges:
        fb = "".join(f'<div class="float-badge fb{i+1}"><span class="d">{ic(b[0])}</span>{b[1]}</div>' for i, b in enumerate(badges))
    c = f'<a class="link-arrow" href="{cta[0]}">{cta[1]} {ic("arrow")}</a>' if cta else ""
    return f'''<section class="section{' section-soft' if soft else ''}"><div class="container"><div class="split{' rev' if rev else ''}">
<div class="media" data-reveal="{'right' if rev else 'left'}"><div class="frame"><img src="{IMG}{img}" alt="{html.escape(title)}" loading="lazy"></div>{fb}</div>
<div><h2 data-reveal>{ORIG.get(kicker, kicker)}</h2>{f'<p class="desc" data-reveal>{desc}</p>' if desc else ''}{body}{c}</div>
</div></div></section>'''

def head(eyebrow, title, sub="", left=False, dark=False):
    return f'<div class="section-head{" left" if left else ""}"><h2 data-reveal>{title}</h2>{f"<p data-reveal>{sub}</p>" if sub else ""}</div>'

def cta(title="Join the Educore Revolution!", text="Simplify, enhance, and transform your school management today with Educore’s all-encompassing platform."):
    return f'''<section class="section" style="padding-top:0"><div class="container"><div class="cta" data-reveal="zoom">
<h2>{title}</h2><p>{text}</p>
<div class="acts"><a class="btn btn-light" href="get-started.html" data-magnetic>Get a Quote {ic("arrow")}</a><a class="btn btn-outline-light" href="contact-us.html">Talk to our team</a></div>
</div></div></section>'''

def card(icon, title, text, link=None, num=None, extra_cls=""):
    icn = f'<img src="{IMG}{icon}" alt="">' if icon.endswith((".png", ".jpg")) else ic(icon)
    l = f'<a class="link-arrow" href="{link}">Read more {ic("arrow")}</a>' if link else ""
    n = ""
    return f'<div class="card spot gborder {extra_cls}">{n}<div class="ic">{icn}</div><h3>{title}</h3><p>{text}</p>{l}</div>'

# ---------------------------------------------------------------- pages
pages = {}

# ===== VIDEOS: Educore's own YouTube videos (played on click, privacy-enhanced embed)
VIDEOS = {  # key: (YouTube id, title, duration)
 "home": ("5IMLWCYQXzY", "Advance Your School Management with Educore's 360° Holistic System", "1:23"),
 "montessori": ("niKLfuWlclY", "Empower Young Minds with Educore's Montessori Curriculum", "1:08"),
 "lms": ("9FjHfAEq3-c", "Smart Assessment Solutions with Educore", "2:14"),
 "ey": ("Wrn8m0IKcmA", "Educore Observation Module Helps ECE Centers Meet Regulatory Compliance", "1:17"),
 "attendance": ("WIhpYhLL-N4", "Transform Your School's Attendance Management with Educore", "0:52"),
 "analysis": ("B1oxD5FP8V0", "Academic Analytics in Educore", "1:25"),
 "crm": ("iZXNZlNv6Fs", "Revamp Your School's Registration Process with EducoreCRM", "1:33"),
 "admission": ("_gOgjRaV-C8", "Increase Admissions with the Educore Registration Workflow", "1:53"),
 "payments": ("wTkPcW77qng", "A New Era of School Payments with Educore", "1:43"),
 "communicator": ("fDWs-0I8bU0", "Seamless School Communication with the Educore Communication Console", "2:18"),
 "parent": ("kcSSWLqaJ3k", "Re-Enrollment Made Easy with EducoreParent", "0:44"),
 "teacher": ("rIlO68ynWSs", "Observations with the EducoreTeacher App", "1:34"),
 "health": ("L1hv5zz8iuQ", "Educore's Health Feature", "1:45"),
}
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.6-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>'
def video(key):
    yid, title, dur = VIDEOS[key]
    t = html.escape(title)
    return (f'<div class="vid" data-yt="{yid}" data-title="{t}">'
            f'<img src="{IMG}yt-{yid}.jpg" alt="" loading="lazy">'
            f'<button type="button" class="vid-play" aria-label="Play video: {t}">{PLAY}</button>'
            f'<span class="vid-meta">{PLAY}Watch video · {dur}</span></div>')

# ===== MODULES: six functional areas, each module listed once under its main purpose
# (id, name, short description, icon, details list or None, image or None, link or None)
AREAS = [
 dict(key="education", name="Education", color="#00A9E6", icon="book", img="academic-module.png",
  lead="Everything teachers and academic leaders use every day: learning, early years, attendance, appointments, results, library, timetables and extracurricular activities.",
  mods=[
   ("lms", "EducoreLMS", "Curriculum, lessons, assignments and assessments.", "book",
    ["Curriculum management", "Courses, lessons and lesson plans", "Assignments and homework", "Online exams and assessments with a question bank", "Academic reports and report cards", "Gap analysis and cohort analysis"], "learning-management-system.png", "school.html"),
   ("ey", "EducoreEY", "Early years observations, learning objectives, journals and reports.", "baby",
    ["Curriculum and learning areas (EYFS, Montessori and more)", "Define objectives and set attainments", "Record observations in real time", "Generate gap analysis", "Learning journals and academic reports for parents"], "observations.png", "early-years.html"),
   ("ib", "EducoreIB", "International Baccalaureate (IB) curriculum support.", "globe", None, None, None),
   ("attendance", "EducoreAttendance", "Student attendance, absences, lateness and reports.", "check", None, None, None),
   ("appointment", "EducoreAppointment", "Appointment scheduling and coordination.", "calendar", None, None, None),
   ("analysis", "EducoreAnalysis", "Academic performance analysis and reports.", "chart",
    ["Dashboards that bring your data to life", "Trend analysis across grades, subjects and cohorts", "Predictive insights to support student success"], "educore-performance-module.png", None),
   ("library", "EducoreLibrary", "Book lending and returns.", "book", None, None, None),
   ("digitallibrary", "EducoreDigitalLibrary", "Digital resources organised by categories, sub-categories and activities.", "layers", None, None, None),
   ("timetable", "EducoreTimetable", "Class, teacher and room timetable scheduling.", "calendar",
    ["Weekly subject planners for each class", "Assign lessons to specific periods", "Match teachers and rooms to each course", "Timetables available in the Educore mobile app"], "timetable-mangement.png", None),
   ("eca", "EducoreECA", "Extracurricular activities, clubs and participation.", "award", None, None, None),
  ]),
 dict(key="operations", name="Operations", color="#6A3FD0", icon="gear", img="school-operations.png",
  lead="The daily running of the school: student records, enquiries and admissions, approvals, transport, dismissal, menus, withdrawals and reports.",
  mods=[
   ("sis", "EducoreSIS", "Student information, classes, registrations and school records.", "id",
    ["School setup: campuses, grade levels, classrooms and schedules", "Fee groups", "Parents’ and children’s profiles with contacts and relationships", "Registrations to classes and grade levels", "Classes management: teachers, class sizes and progress", "Admin reports on attendance, performance and finance", "Light employee profiling"], "basic-modules.png", None),
   ("crm", "EducoreCRM", "Leads, enquiries, referrals and follow-ups.", "funnel",
    ["Inquiries from Facebook, Instagram, Snapchat, X and LinkedIn", "Educore Forms for online and offline inquiries", "Walk-in registrations", "Landing pages linked to your website", "Referrals and follow-ups"], "educore-crm-module.png", None),
   ("admission", "EducoreAdmission", "Applications, admission tasks, documents and enrolment.", "form",
    ["Collect inquiries", "Follow up through the CRM", "Register students online", "Convert leads into registrations"], "educore-admission-workflow.png", None),
   ("workflow", "EducoreWorkflow", "Staff requests, routing, approvals and status tracking.", "flow",
    ["Staff requests routed to the responsible department", "Approval processes on autopilot", "Live request status", "Online forms in more than 16 languages"], "educore-workflow-module.png", None),
   ("transport", "EducoreTransport", "Transport routes, bus assignments and transport updates.", "bus",
    ["Bus routes and schedules", "Live bus tracking for parents in EducoreParent", "Boarding and drop-off notifications", "Trip notifications when a student will not ride", "Driver and assistant trip and student lists"], "educore-transport-module.png", None),
   ("dismissal", "EducoreDismissal", "Student pick-up/drop-off coordination and dismissal records.", "users",
    ["Designated pick-up and drop-off points and times", "Timely notifications for parents and staff", "QR verification at pick-up", "Dismissal records"], "educore-pick-drop-module.png", None),
   ("menu", "EducoreMenu", "School menu planning and publishing.", "form", None, None, None),
   ("withdrawal", "EducoreWithdrawal", "Student withdrawal requests, approvals and setup.", "arrow", None, None, None),
   ("reportcenter", "EducoreReportCenter", "HR, admin, attendance, financial, VAT, accounting and academic reports in one place.", "chart", None, None, None),
  ]),
 dict(key="hr", name="HR", color="#B43BEF", icon="team", img="HRM-module.png",
  lead="Your staff from hiring to payroll: records, recruitment, payroll, evaluation and the staff team app.",
  mods=[
   ("hrm", "EducoreHRM", "Employee profiles, attendance, HR records and reports.", "id",
    ["Staff profiles, contracts and personal records", "Staff attendance by QR code, biometric or mobile app", "Track progression and promotions", "HR reports"], None, None),
   ("recruitment", "EducoreRecruitment", "Publish vacancies and receive applicant submissions.", "users", None, None, None),
   ("payroll", "EducorePayroll", "Payroll periods, leave, deductions, loans and end-of-service calculations.", "card",
    ["Earnings, allowances, deductions and leave", "Print pay slips", "End-of-service calculations", "Saudi GOSI calculation for KSA schools", "Payroll synced with attendance"], None, None),
   ("evaluation", "EducoreEvaluation", "Staff evaluations and performance reports.", "award",
    ["Build evaluation KPIs", "Record staff evaluations", "Track employee growth over time", "Evaluation charts for meetings"], None, None),
   ("adminevaluation", "EducoreAdminEvaluation", "Evaluation of administrative staff with KPIs and employee tracking.", "target", None, None, None),
   ("teams", "EducoreTeams", "Staff communication and leave requests.", "team",
    ["Messages and updates between teams", "Leave requests", "Documents and notifications linked to HR and payroll"], "educore-module-mobile-app.png", "mobile-app.html"),
  ]),
 dict(key="erp", name="ERP", color="#E0249A", icon="db", img="educore-finance-module.png",
  lead="The school’s resources and money: billing with ZATCA e-invoicing, accounts, assets, inventory, payments, budgets, the school marketplace and external sales.",
  mods=[
   ("billing", "EducoreBilling", "Invoices, receipts, balances and statements.", "form",
    ["Invoices and automated receipts", "Custom payment schedules and automated reminders", "Balances and statements", "Pending, collected and outstanding fee reports", "Export to accounting software in Excel formats"], "educore-billing-module.png", None),
   ("finance", "EducoreFinance", "Expenses, accounts, journals, bank records and VAT reports.", "wallet",
    ["Expenses", "Accounts and journals", "Bank records", "VAT reports", "Audit trails for compliance"], None, None),
   ("assets", "EducoreAssets", "Asset management and tracking.", "layers", None, None, None),
   ("inventory", "EducoreInventory", "Inventory and stock records.", "box", None, None, None),
   ("payments", "EducorePayments", "Payment processing and integration.", "card",
    ["Integration with major payment gateways", "Parents pay in the EducoreParent app", "Secure, instantly processed transactions"], None, None),
   ("budgets", "EducoreBudgets", "Budgets and approval hierarchies.", "target", None, None, None),
   ("marketplace", "EducoreMarketplace", "School products/services, purchases and related payments.", "cart", None, None, None),
   ("externaloperations", "EducoreExternalOperations", "Clients, invoices, receipts and cash sales for external customers.", "briefcase", None, None, None),
  ]),
 dict(key="communication", name="Communication", color="#00A9E6", icon="chat", img="module-EducoreCommunicator.png",
  lead="Keeping your community connected: announcements and updates, alumni, chat oversight, and the parent and teacher apps.",
  mods=[
   ("communicator", "EducoreCommunicator", "Announcements, notifications, newsletters, events, polls, surveys and media.", "bell",
    ["Notifications and event reminders", "Daily reports with photos", "Newsletters and banners", "Polls and surveys", "Incident reports", "Media sharing, chat, diaries and agendas"], None, None),
   ("alumni", "EducoreAlumni", "Stay connected with alumni: notifications, events, polls, surveys, registration, banners and discount vouchers.", "grad", None, None, None),
   ("chatmonitor", "EducoreChatMonitor", "School oversight of chats between teachers, parents and students.", "eye", None, None, None),
   ("parent", "EducoreParent", "Parent-facing school updates and supported school services.", "users",
    ["Daily reports, activities and notifications", "Attendance and live bus tracking", "Online fee payment"], "feature-1.png", "mobile-app.html"),
   ("teacher", "EducoreTeacher", "Teacher access to classroom tools, resources and communication.", "grad",
    ["Assignments and schedules", "Observations", "Online assessments"], "feature-2.png", "mobile-app.html"),
  ]),
 dict(key="wellbeing", name="Well-being", color="#5DAE3B", icon="pulse", img="feature-3.png",
  lead="Caring for every student: health, special educational needs, concerns and positive behaviour.",
  mods=[
   ("health", "EducoreHealth", "Student health profiles, allergies, illnesses and incident records.", "heart",
    ["Vaccination records and compliance", "Allergies and chronic illnesses", "Health logs for students, staff and visitors", "Incident reports sent to the parent’s app"], "feature-3.png", None),
   ("sen", "EducoreSEN", "Special educational needs, conditions, progress and academic assessments.", "puzzle", None, None, None),
   ("concerns", "EducoreConcerns", "Parent and student concerns, logs and resolutions.", "shield", None, None, None),
   ("sep", "EducoreSEP", "Behaviour points, awards and redemption.", "star", None, None, None),
  ]),
]
# Feature lists merged from the Educore General Proposal (slides 8–16) and the live portal (academic.educore.io)
PROPOSAL_FEATURES = {
 "lms": ["Projects", "Curriculum management", "Courses and lesson management", "Lesson plans and weekly plans", "Exams and assessments", "Assignments and homework", "Grade weighting", "Academic reports and report cards"],
 "ey": ["Assessment coverage and term comparative report", "Learning goals tracker", "Curriculum, learning areas and aspects of learning (EYFS, Montessori and more)", "Define objectives and set attainments", "Record observations", "Generate gap analysis", "Learning journals", "Academic reports"],
 "analysis": ["Grade books and teacher report", "Tracking forms", "Assessment program and marks percentage", "Grades and analytics", "Academic reports", "Rubrics", "Gap analysis and cohort analysis", "3-year comparative analysis by class and by student", "Same-year term performance"],
 "library": ["Books management", "Book lending", "Return notifications"],
 "eca": ["Build your extracurricular activities", "Set up fees and schedules", "Student registration", "Compliant invoices"],
 "crm": ["KYC and school tours (booked and taken)", "No-enrollment reasons", "Manage leads", "Referrals and enquiry sources", "Social media inquiries: Facebook, Instagram, Snapchat, X and LinkedIn", "Email templates and email automation", "Mass mailing", "Walk-ins and Educore Forms"],
 "admission": ["Admission Q&A and admission form attachments", "Manage admission applications", "Add tasks to each application", "Track required data and documents", "Register students online and convert leads into registrations"],
 "workflow": ["Staff groups", "Request types: HR, inventory and more", "Build approval workflows", "Tracking dashboard for request status"],
 "transport": ["Bus list report", "Manage buses", "Assign staff, trips and students", "GPS tracking of buses (requires tracking hardware)", "Parents notified on boarding and drop-off", "Live bus tracking in EducoreParent"],
 "dismissal": ["Parents send pick-up/drop-off requests", "The gate is notified automatically", "Monitor requests live", "Dismissal records"],
 "hrm": ["User rights", "Class assignment", "Employees on holidays", "Attendance policies", "Full employee profiles", "Employee attendance", "EducoreAttendance staff app: check in by QR code or proximity card, linked to HR and payroll", "HR reports and HR demographics", "Employee notifications"],
 "adminevaluation": ["Build evaluation KPIs", "Record staff evaluations", "Generate employee track"],
 "recruitment": ["Online application portal connected to Educore", "Vacancies by role, grade and subject", "Filter applicants by required criteria", "Recruitment tasks and email communication"],
 "payroll": ["Cut-off periods", "Leaves and absences", "Allowances, deductions and loans", "End-of-service calculations", "WPS SIF report", "Saudi GOSI calculation for KSA schools", "Pay slips"],
 "evaluation": ["Build evaluation KPIs", "Record staff evaluations", "Generate employee track", "Generate evaluation charts"],
 "teams": ["Communicate with staff and messaging", "Leave requests and tracking", "Personalized QR code for attendance (requires EducorePayroll)"],
 "billing": ["Registration proforma, registration invoices and services billing", "Batch registration and change class", "ZATCA e-invoicing for KSA (Zakat, Tax and Customs Authority)", "Services and term fee structure", "Registration invoices and services billing", "Receipts", "Balance reports", "Statement of accounts"],
 "finance": ["Purchases", "Journal vouchers", "Suppliers, expenses and payments", "Receipts and banks", "VAT reports", "Trial balance, balance sheet and income statement", "Chart of accounts and cost centres"],
 "assets": ["Asset definitions", "Depreciation schemes", "Automatic depreciation journal vouchers", "Track depreciation"],
 "inventory": ["Define your warehouses", "Track item movement", "Item transfers", "Item consumption and costs"],
 "payments": ["Integration with the payment gateway provided by the school", "Parents pay in the EducoreParent app", "Secure, instantly processed transactions"],
 "budgets": ["Up to 3 years of trial balance", "Set the yearly expense budget", "Allocate expense transactions against the budget", "Approval hierarchies"],
 "marketplace": ["Define your services and items", "Integrated with the EducoreParent app and portal", "Parents buy online and pay through the payment gateway", "Automated invoices and receipts"],
 "communicator": ["Exam and homework posts", "Notifications, events and chat", "Images and videos", "Newsletters, banners and notes", "Online classes and shared resources", "Polls and surveys", "School policies, diary and agenda"],
 "health": ["Incident reports", "Illnesses and allergies", "Student vaccination records", "Health logs for students, staff and visitors", "EducoreHealth mobile app"],
 "sen": ["Set SEN student tiers", "Build a general objective plan", "Personalized plan per student", "Generate reports"],
 "concerns": ["Parents write concerns or complaints", "Engage the right staff", "Resolve privately through internal discussion", "Resolve with the parent through EducoreParent"],
 "digitallibrary": ["Digital library list", "Categories and sub-categories", "Activities"],
 "withdrawal": ["Withdrawal requests view", "Withdrawal manager", "Withdrawal setup"],
 "reportcenter": ["HR reports", "Admin reports", "Attendance reports", "Financial, VAT and accounting reports", "Academic reports"],
 "externaloperations": ["Clients", "Invoices", "Receipts", "Cash sales"],
 "alumni": ["Notifications, events and banners for alumni", "Polls and surveys", "Alumni registration", "Discount vouchers"],
 "chatmonitor": ["See every teacher–parent and teacher–student conversation", "Search conversations", "Message counts and last activity"],
 "menu": ["Menu items", "Allergies list", "Meal calendar: breakfast, AM snack, lunch and PM snack"],
 "sep": ["SEP status, priorities and actions taken", "Define awards, trophies, warnings and behaviours", "Record awards or incidents per student", "Generate analysis", "Resolve incidents"],
}
for _a in AREAS:
    _a["mods"] = [(m[0], m[1], m[2], m[3], PROPOSAL_FEATURES.get(m[0], m[4]), m[5], m[6]) for m in _a["mods"]]

# Extra features seen in the portal walkthrough (2 Nov 2026)
PORTAL_EXTRA = {
 "sis": ["Registration periods", "Student promotion and fast track", "Assign elective subjects", "Merge classes", "Roles", "Alumni students and media download"],
 "billing": ["Services and service bundles", "Fee structure, discounts and term fee policies"],
 "finance": ["Petty cash, direct and cash expenses", "Multi-payments and multi-expenses", "Cheque replacement and bank reconciliation", "Purchase orders, tax purchases and tax debit notes"],
 "payroll": ["Monthly payroll", "Early tuition repayments"],
 "communicator": ["Parent comments", "Results, activities and finance posts", "Media approval", "Engagement statistics", "Consolidated communication across schools"],
 "ey": ["Monthly observations", "Curriculum builder", "Create and assign activities"],
 "lms": ["Exam groups and types"],
 "timetable": ["Period types and automatic timetable generation"],
}
for _a in AREAS:
    _a["mods"] = [(m[0], m[1], m[2], m[3], (list(m[4] or []) + [f for f in PORTAL_EXTRA.get(m[0], []) if f not in (m[4] or [])]) or None, m[5], m[6]) for m in _a["mods"]]

def area_href(a): return f"modules-{a['key']}.html"

def area_nav(active):
    return '<div class="subnav"><div class="container"><div class="inner">' + "".join(
        f'<a class="{"on" if a["key"] == active else ""}" href="{area_href(a)}">{a["name"]}</a>' for a in AREAS) + '</div></div></div>'

def mod_list(a, link_to_page=False):
    """Compact list of an area's modules: name + one-line purpose (like the overview chart)."""
    rows = ""
    for mid, n, d, i, *_ in a["mods"]:
        target = f'{area_href(a)}#{mid}' if link_to_page else f'#{mid}'
        rows += f'<a class="ml" href="{target}"><span class="ml-ic">{ic(i)}</span><span><b>{n}</b><small>{d}</small></span></a>'
    return f'<div class="mlist">{rows}</div>'

def area_page(a):
    secs = ""
    n = 0
    for mid, name, d, i, details, img, link in a["mods"]:
        more = f'<a class="link-arrow" href="{link}">Learn more {ic("arrow")}</a>' if link else ""
        has_video = mid in VIDEOS
        if (details and img) or has_video:
            media = f'<div class="media" data-reveal="{"right" if n % 2 else "left"}">' + (video(mid) if has_video else f'<div class="frame"><img src="{IMG}{img}" alt="{name}" loading="lazy"></div>') + '</div>'
            secs += f'<section class="section{" section-soft" if n % 2 else ""}" id="{mid}" style="scroll-margin-top:150px"><div class="container"><div class="split{" rev" if n % 2 else ""}">' \
                    f'{media}<div><h2 data-reveal>{name}</h2><p class="desc" data-reveal>{d}</p>{checks(details) if details else ""}{more}</div></div></div></section>'
            n += 1
    # modules without an image: one clean grid
    rest = [(mid, name, d, i, details, link) for mid, name, d, i, details, img, link in a["mods"] if not ((details and img) or mid in VIDEOS)]
    if rest:
        cards = ""
        for mid, name, d, i, details, link in rest:
            body = checks(details) if details else ""
            more = f'<a class="link-arrow" href="{link}">Learn more {ic("arrow")}</a>' if link else ""
            cards += f'<div class="card spot gborder area-card" id="{mid}" style="scroll-margin-top:150px"><div class="ic">{ic(i)}</div><h3>{name}</h3><p>{d}</p>{body}{more}</div>'
        secs += f'<section class="section{" section-soft" if n % 2 else ""}"><div class="container">{head("", "More " + a["name"] + " modules" if n else a["name"] + " modules")}<div class="grid g2" data-stagger>{cards}</div></div></section>'
    return f'''{phero([("modules","Modules"),(None,a["name"])], "", a["name"], a["lead"], a["img"])}
{area_nav(a["key"])}
<section class="section" style="padding-bottom:40px"><div class="container" style="--area:{a["color"]}">
 {head("", "Modules in " + a["name"], "Each module below is part of the " + a["name"] + " area. Select one to jump to it.")}
 {mod_list(a)}
</div></section>
{secs}
{cta()}'''

# ===== HOME
APPS = [
  ("EducoreParent", "users", "Instant access to everything about their child, daily reports, activities, notifications, fee payments and attendance."),
  ("EducoreTeacher", "grad", "Create and share assignments and schedules, record observations and run tailored online assessments."),
  ("EducoreHealth", "heart", "Connected to the Health Module: declaration forms and health logs for students, employees and visitors."),
  ("EducoreForms", "form", "Used by school receptions to capture visitor data for follow-up and tracking, and to power admissions."),
  ("EducoreTeam", "team", "Staff notifications linked to HR & Payroll, with documents and leave records always at hand."),
  ("EducoreStudent", "book", "Distance learning made easy: lesson plans, homework, curricula, sessional exams and performance."),
  ("EducoreAttendance", "qr", "Mark daily staff attendance by proximity card or QR code, linked directly to HR & Payroll."),
  ("EducoreAppraisal", "award", "Design appraisal questionnaires, set benchmarks, run periodic staff appraisals and generate reports."),
]
FAQ = [
  ("How secure is your data with Educore?", "Our Security Center includes cPHulk Brute Force Protection, Host Access Control, ModSecurity and a Security Adviser including ImunifyAV, plus Shell Fork Bomb Protection. Our security framework complies with GDPR, with perpetual security and DDoS protection. To detect and block attacks on our technical infrastructure, we process identification, connection or localization data under our legitimate interest in protective measures; this data is processed by Cloudflare Inc. under a data processing agreement (Art. 28 GDPR). Educore is also ISO 27001:2022 certified."),
  ("How are we different from other daycare platforms?", "We are a childcare management software dedicated to providing better education and overall upbringing to your children. Managing a full-fledged school is not other platforms’ forte. With Educore, parents can raise concerns, pay fees, receive assessment reports for their kids and much more."),
  ("Does Educore provide training sessions to clients?", "Our apps are built with intuitiveness at their core, even older guardians use them seamlessly. We also provide training and support during onboarding, along with additional material for further help."),
  ("Does Educore work across all platforms?", "Yes. Educore runs on Web, iOS and Android across tablets, computers, laptops and smartphones, so you can access it anytime, anywhere, at a price that works for you."),
  ("Can payments & transactions be made online?", "EducoreParent has an integrated payment system supporting all major payment portals. School owners can raise invoices, accept payments and generate automated, branded receipts in the app."),
  ("What do I need to get started with Educore?", "All you need is an internet connection and a tablet or mobile phone for each room. We take care of the rest, we onboard all your data or migrate it from your existing system within a day."),
]
TESTI = [
  ("Amina Rayees", "We are extremely satisfied with the Educore Management Portal. We find it very convenient and easy to use, highly effective for parent communication while maintaining confidentiality. Educore is always prompt with services and innovative, constantly updating."),
  ("Ana Mary", "We started with the basic package and within 6 months were using the majority of Educore modules. It has really supported our drive for effective management across locations. For nurseries looking for a fully integrated system, Educore really does provide it all."),
  ("Amina Rayees", "Our clinics are also managed using Educore, with children’s details and complete medical history available to nurses. Accident reports go straight to the parent’s app, and the CRM lets us track every parent’s registration journey."),
  ("Ahmed Kiyam", "Educore saved us an incredible amount of research and documentation. Parents are happy, and the support we receive is responsive to our evolving needs. We reviewed many solutions on the market and Educore stood out as the very best."),
  ("Sandra Joseph", "Convenient, easy to use and highly effective for parent communication. We use it for record keeping, communication and documenting, and we constantly get feedback from happy parents. The app also encourages parental involvement."),
]
CERTS = [("certificate1.png", "ISO 9001:2015", "Quality management"), ("certificate2.png", "ISO 27001:2022", "Information security"),
         ("certificate3.png", "Oracle Cloud", "OCI partner"), ("certificate4.png", "MySQL HeatWave", "Official partner"), ("certificate5.png", "HIK Vision", "Security solutions")]
TOOLS = ["Build Evaluation KPI", "Generate Employee Track", "Transportation", "Online Payment Gateway", "Record Staff Evaluation", "Generate Evaluation Chart", "Automated Timetables", "Bus Tracking"]


def app_btn_fn(r):
    return "".join(f'<button class="app-btn" type="button"><span class="ic">{ic(icn)}</span><span><b>{t}</b><small>{d}</small></span></button>' for t, icn, d in r)
def phones_fn():
    return "".join(f'<img src="{IMG}feature-{i+1}.png" alt="{APPS[i][0]} app screen" loading="lazy">' for i in range(8))
def apps_block():
    return f'''<div class="apps" data-reveal>
  <div class="app-list">{app_btn_fn(APPS[:4])}</div>
  <div class="phone">{phones_fn()}</div>
  <div class="app-list">{app_btn_fn(APPS[4:])}</div>
 </div>'''


def home():
    slides = [("banner-slider-1.png", "Holistic System"), ("digital-transformation.jpg", "Digital Transformation"), ("banner-slider-3.png", "Digital Partner"),
              ("multi-curriculum.jpg", "Multi Curriculum Support"), ("banner-slider-5.png", "Empowered Communication")]
    # Hero clips: real classroom footage from Pexels (free licence), one per topic button
    clips = ["8342238", "7999596", "8342240", "5200348", "5897650"]
    vids = "".join(f'<video muted playsinline loop preload="{"auto" if n == 0 else "none"}" poster="assets/video/class-{c}.jpg" aria-label="{slides[n][1]}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"><source src="assets/video/class-{c}.mp4" type="video/mp4"></video>' for n, c in enumerate(clips))
    tabs = "".join(f'<button type="button">{t}</button>' for _, t in slides)
    rot = "".join(f"<span>{w}</span>" for w in ["schools", "nurseries", "education groups", "teachers", "parents"])
    certs = "".join(f'<div class="logo-pill"><img src="{IMG}{i}" alt="{t}"><span><b>{t}</b><small>{s}</small></span></div>' for i, t, s in CERTS) * 2
    mods = "".join(f'<a class="card spot gborder area-tile" href="{area_href(a)}" style="--area:{a["color"]}"><div class="ic">{ic(a["icon"])}</div><h3>{a["name"]}</h3><p>{", ".join(m[1] for m in a["mods"])}</p><span class="link-arrow">Explore {a["name"]} {ic("arrow")}</span></a>' for a in AREAS)
    app_btn = lambda r: "".join(f'<button class="app-btn" type="button"><span class="ic">{ic(icn)}</span><span><b>{t}</b><small>{d}</small></span></button>' for t, icn, d in r)
    phones = "".join(f'<img src="{IMG}feature-{i+1}.png" alt="{APPS[i][0]} app screen" loading="lazy">' for i in range(8))
    faq = "".join(f'<details{" open" if n == 0 else ""}><summary>{q}<span class="pm"></span></summary><div class="ans">{a}</div></details>' for n, (q, a) in enumerate(FAQ))
    tools = "".join(f'<span class="tag-pill"><i></i>{t}</span>' for t in TOOLS) * 2
    tcards = "".join(f'<div class="tcard"><p>“{q}”</p><div class="who"><span class="av">{n[0]}</span><span><b>{n}</b><small>Educore client</small></span></div></div>' for n, q in TESTI) * 2
    locs = "".join(f'<span class="loc{" hq" if c == "Dubai, UAE" else ""}"><span class="pin"></span>{c}{" · HQ" if c == "Dubai, UAE" else ""}</span>' for c in ["Toronto, Canada", "London, UK", "Milan, Italy", "Istanbul, Turkey", "Dubai, UAE"])
    return f'''
<section class="hero"><div class="container"><div class="hero-grid">
 <div>
  <h1 data-reveal>Educore is a 360-degree Holistic Experience</h1>
  <p class="lead" data-reveal style="--d:.2s">Educore is a holistic system that serves the entire education system with a digitally empowered platform.</p>
  <div class="hero-actions" data-reveal style="--d:.3s"><a class="btn" href="get-started.html" data-magnetic>Get a Price {ic("arrow")}</a><a class="btn btn-ghost" href="registration.html">Setup School</a></div>
 </div>
 <div data-reveal="zoom" style="--d:.15s">
  <div class="stage">
   <div class="ring"></div><div class="ring r2"></div>
   <div class="disc" style="overflow:hidden"><div data-slides="hero" style="position:absolute;inset:0">{vids}</div></div>
   <div class="orbit"><span class="dot"></span><span class="dot"></span></div>
   <div class="chip c1"><span class="ic" style="background:linear-gradient(135deg,#B43BEF,#7b5cff)">{ic("star")}</span><span><b data-count="137">0</b><small>Clients</small></span></div>
   <div class="chip c2"><span class="ic" style="background:linear-gradient(135deg,#007AFF,#00C0FE)">{ic("users")}</span><span><b data-count="81337">0</b><small>Students & Parents</small></span></div>
   <div class="chip c3"><span class="ic" style="background:linear-gradient(135deg,#00C0FE,#00a3d6)">{ic("staff")}</span><span><b data-count="6119">0</b><small>Total Staff</small></span></div>
  </div>
  <div class="slide-tabs" data-slide-tabs="hero" style="justify-content:center">{tabs}</div>
 </div>
</div></div></section>

<section style="padding:10px 0 40px"><div class="container">
 <h3 style="text-align:center;margin-bottom:24px" data-reveal>Trusted Certifications & Partnerships</h3>
 <div class="marquee" data-reveal><div class="marquee-track">{certs}</div></div>
</div></section>

<section class="section"><div class="container">
 {head("", "Educore Exclusive Modules", "Six functional areas, with each module grouped by its main purpose. Start with what you need and add more as you grow.")}
 <div class="grid g3" data-stagger>{mods}</div>
 <div style="text-align:center;margin-top:44px" data-reveal><a class="btn btn-ghost" href="modules.html">Explore all modules {ic("arrow")}</a></div>
</div></section>

<section class="section section-soft"><div class="container">
 {head("", "Watch Educore in Action", "See how Educore brings every part of school management together in one holistic system.")}
 <div class="vid-wide" data-reveal="zoom">{video("home")}</div>
</div></section>

<section class="section"><div class="container">
 {head("", 'We Serve In Extensive Traits', "Educore is a holistic system that serves the entire education system with a digitally empowered platform.")}
 <div class="grid g3" data-stagger>
  <a class="plat-orig" href="early-years.html"><img src="{IMG}platform-1.png" alt="Early Years" loading="lazy"></a>
  <a class="plat-orig" href="school.html"><img src="{IMG}platform-2.png" alt="School" loading="lazy"></a>
  <a class="plat-orig" href="education-groups.html"><img src="{IMG}platform-3.png" alt="Education Institution" loading="lazy"></a>
 </div>
</div></section>

{split("aboutDB.png", "About Educore System", 'A holistic system for the entire education journey', "Educore serves the entire education system with a digitally empowered platform, academic, administrative and financial.",
  checks(["All-in-one holistic system", "Highly adaptable", "Localized to local authority laws", "Multi-lingual", "Distinguished first-line support", "Modular system"], two=True),
  badges=[("shield", "ISO 27001 secured"), ("globe", "Multi-lingual")], cta=("about.html", "Explore more"))}

<section class="section section-soft"><div class="container">
 <div class="scroller">
  <div class="sticky"><div class="section-head left" style="margin-bottom:28px"><h2>Educore Core Features</h2><p>Core features and innovative solutions designed to cover all school operations.</p></div>
   <div class="screen">{"".join(f'<img src="{IMG}{i}" alt="" loading="lazy">' for i in ["student-profiles.png","school-operations.png","online-assessment.png","module-EducoreCommunicator.png","educore-finance.png","performance-analytics.png"])}</div></div>
  <div class="steps">
   {"".join(f'<div class="step"><h3>{t}</h3><p>{d}</p></div>' for n,(t,d) in enumerate([
     ("Comprehensive Student Information System","Detailed student profiles with personal information, academic history, attendance and health records, plus a parent portal."),
     ("Highly adaptable","Configure campuses, grade levels, curricula and workflows to match the way your institution actually works."),
     ("Efficient administration tools","Automated scheduling, admission management, gradebooks and curriculum management in a few clicks."),
     ("Enhanced communication features","Direct messaging between teachers, students and parents, with school-wide announcements."),
     ("Integrated financial management","Tuition fees, payment tracking, invoices and expense tracking, with online payment gateways."),
     ("Dashboards and reports","Live dashboards and analytics that turn every data point into a decision."),
   ]))}
   <a class="link-arrow" href="features.html" style="margin:14px 0 0 8px">See all features {ic("arrow")}</a>
  </div>
 </div>
</div></section>

<section class="section"><div class="container">
 {head("", "Exclusive Mobile Family", "Apps for parents, teachers, students, staff and school receptions, all connected to the same system.")}
 <div style="text-align:center;margin:-30px 0 40px" data-reveal><a class="link-arrow" href="mobile-app.html">Explore the apps {ic("arrow")}</a></div>
 <div class="apps" data-reveal>
  <div class="app-list">{app_btn(APPS[:4])}</div>
  <div class="phone">{phones}</div>
  <div class="app-list">{app_btn(APPS[4:])}</div>
 </div>
</div></section>

<section class="section dark on-dark">{MESH}<div class="container">
 {head("", "Get the extra milestone with Educore Tools")}
 <div class="marquee"><div class="marquee-track" style="animation-duration:35s">{tools.replace('tag-pill','tag-pill" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.12);color:#fff')}</div></div>
 <div style="height:16px"></div>
 <div class="marquee rev"><div class="marquee-track" style="animation-duration:45s">{tools.replace('tag-pill','tag-pill" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.12);color:#fff')}</div></div>
 <div style="text-align:center;margin:60px 0 26px"><h3 data-reveal>Serving schools across the globe</h3></div>
 <div class="locs" data-stagger>{locs}</div>
</div></section>

<section class="section"><div class="container">
 {head("", "Look What Our Customers Say!")}
</div>
 <div class="marquee" data-reveal><div class="marquee-track slow">{tcards}</div></div>
</section>

<section class="section section-soft"><div class="container">
 {head("", "Frequently Asked Questions")}
 <div class="faq" data-stagger>{faq}</div>
</div></section>

<section class="section" style="padding-bottom:40px"><div class="container">
 <div class="stats" data-stagger>
  <div class="stat"><div class="num"><span data-count="137">0</span><em>+</em></div><p>Clients worldwide</p></div>
  <div class="stat"><div class="num"><span data-count="81337">0</span><em>+</em></div><p>Students & parents</p></div>
  <div class="stat"><div class="num"><span data-count="6119">0</span><em>+</em></div><p>Staff on Educore</p></div>
  <div class="stat"><div class="num"><span data-count="8">0</span></div><p>Mobile apps</p></div>
 </div>
</div></section>
{cta()}
'''
pages["index"] = ("Home", "Educore is a 360° holistic school management system: CRM & admissions, SIS, LMS, HRM, finance, communication and mobile apps for schools, nurseries and education groups.", home())

# ===== ABOUT
pages["about"] = ("About", "About Educore, a holistic, cloud-based school management system covering academic, administrative and financial operations.", f'''
{phero([(None,"About")], "", 'About Educore System', "Educore is a holistic system that serves the entire education system with a digitally empowered platform.", "about-page-hero.png", pills=["SaaS", "Cloud-based ERP", "Multi-lingual", "Localized"])}
<section class="section" style="padding-top:20px"><div class="container"><div class="stats" data-stagger>
 <div class="stat"><div class="num"><span data-count="137">0</span><em>+</em></div><p>Clients</p></div>
 <div class="stat"><div class="num"><span data-count="81337">0</span><em>+</em></div><p>Students & parents</p></div>
 <div class="stat"><div class="num"><span data-count="6119">0</span><em>+</em></div><p>Total staff</p></div>
 <div class="stat"><div class="num"><span data-count="5">0</span><em> cities</em></div><p>Global presence</p></div>
</div></div></section>
<section class="section section-soft"><div class="container">
 {head("", "What We Do", "A holistic and coherent system for education that covers all the operations of an educational establishment, academic, administrative or financial.")}
 <div class="bento" data-stagger>
  <div class="card spot span-4 feature"><div class="ic">{ic("layers")}</div><h3>Full workflow coverage</h3><p>We cover the full workflow of your processes: School CRM & Admissions, School Management, Learning Management (LMS), HRM and ERP.</p></div>
  <div class="card spot span-2"><div class="ic">{ic("cloud")}</div><h3>Software as a Service</h3><p>Educore is served on SaaS, always up to date, always available.</p></div>
  <div class="card spot span-2"><div class="ic">{ic("bolt" if False else "spark")}</div><h3>Fast, accurate data</h3><p>Quick, accurate allocation and maintenance of student and enquiry information boosts administration capability.</p></div>
  <div class="card spot span-2"><div class="ic">{ic("chat")}</div><h3>Engaging communication</h3><p>An effective communication app that lifts the engagement of parents and students.</p></div>
  <div class="card spot span-2"><div class="ic">{ic("calendar")}</div><h3>One platform</h3><p>Digitally plan, manage and monitor daily activities on a single platform.</p></div>
  <div class="card spot span-6"><div class="ic">{ic("puzzle")}</div><h3>Integrates with what you use</h3><p>Educore integrates with 3rd-party systems chosen by schools, payment gateways, people access control, bus tracking and more.</p></div>
 </div>
</div></section>
{split("mission-vission.png", "Our Mission", 'Transforming school management with innovative technology', "Our mission is to make educational administration straightforward and effective. We empower schools with a comprehensive, cloud-based ERP designed to manage every aspect of school life, from academic tracking to administrative functions.",
 checks(["Automates daily tasks", "Enhances enrollment processes", "Provides insightful analytics", "Frees educators to focus on nurturing students"]), badges=[("target","Mission-driven"),("trend","Always improving")])}
<section class="section dark on-dark">{MESH}<div class="container" style="max-width:900px;text-align:center">
 <h2 data-split>Our Vision</h2>
 <p data-reveal style="font-size:1.08rem">We aim to be the top choice for school management systems globally, setting a new standard in educational technology. Our vision is a vibrant ecosystem where schools thrive on advanced, intuitive tools, and by continuously advancing our solutions, we strive to lead the evolution of education management in a rapidly changing world.</p>
</div></section>
<section class="section"><div class="container">
 {head("", "Our USP’s")}
 <div class="grid g3" data-stagger>
  {card("layers","All-in-one holistic system","Every operation of an educational establishment, covered end to end.")}
  {card("puzzle","Highly adaptable & modular","Start with what you need and switch on more modules as you grow.")}
  {card("shield","Localized for local authorities","Configured to comply with the laws and regulations where you operate.")}
  {card("lang","Multi-lingual","Serve families and staff in the languages they speak.")}
  {card("headset","Professional first-line support","A distinguished team that understands schools and childcare.")}
  {card("award","Certified quality & security","ISO 9001:2015 and ISO 27001:2022 certified.")}
 </div>
</div></section>
{cta()}''')

# ===== SERVICES
SVCS = [
 ("Build Evaluation KPI", "educore-genius-service-1.png", ["Set up and run KPIs designed around your school's objectives.", "Analyze and report how educational methods and staff perform.", "Receive analysis results through customizable KPI dashboards for decision-making."], None),
 ("Record Staff Evaluation", None, ["Structurally register evaluations of staff performance.", "Keep accurate, detailed records of feedback, achievements and improvements.", "Make evaluation processes uniform and transparent across the institution."], None),
 ("Generate Employee Track", None, ["Monitor and observe employee performance and growth over time."], None),
 ("Generate Evaluation Chart", None, ["Show performance metrics by creating visual evaluation charts.", "Use charts in presentations and meetings to show trends and results."], None),
 ("Transportation", None, ["Handle school transportation logistics effectively.", "EducoreTransport keeps parents, schools, students & drivers connected through their daily commute for a safer bus ride."],
   [("Bus Tracking", "Live tracking of your child’s movement in EducoreParent."), ("Trip Notification", "Parents can notify the bus if their child won’t take the trip."), ("Pick & Drop", "Parents are notified before the drop or pick-up."), ("Child Boarding", "Instant on-boarding and off-boarding notifications."), ("Student Information", "Drivers & assistants get complete trip info and pick-and-drop order lists.")]),
 ("Online Payment Gateway", None, ["Safeguard online fee collection and other payments with secure transactions.", "Offer various payment methods for parents and guardians.", "Guarantee accurate financial operations with instant processing and reporting."], None),
 ("Attendance Application for Staff", None, ["Make staff attendance management easier with a user-friendly app.", "Monitor arrival/departure times, leave requests and attendance patterns.", "Increase correctness and effectiveness in attendance reporting."], None),
 ("EducoreTeam Application", None, ["Easy internal communication and cooperation among staff.", "Share updates, files and messages between teams and departments.", "Promote teamwork and productivity with integrated tools."], None),
 ("Personalize Your Mobile Apps", None, ["Tailor mobile apps to your school’s branding & needs.", "Provide personalized experiences for students, parents and staff.", "Increase satisfaction and involvement by customizing your services."], None),
 ("Automated Timetables", None, ["Still scheduling timetables manually? Educore automates class timetables across grades and classes with the Educore School Management System, and keeps everyone updated."], None),
]
def services():
    rows = ""
    for n, (t, _, bullets, subs) in enumerate(SVCS):
        s = ""
        if subs:
            s = '<div class="subs">' + "".join(f"<div><b>{a}</b>{b}</div>" for a, b in subs) + "</div>"
        rows += f'<div class="svc" data-reveal><span class="n">{n+1:02d}</span><div><h3>{t}</h3></div><div>{checks(bullets)}{s}</div></div>'
    return f'''
{phero([(None,"Services")], "", 'Educore Genius Services', "The Complete Toolkit for Modern Education. Plug into Educore and Electrify Your School.", "service-page-hero.png")}
<section class="section"><div class="container">
 {head("", "We Serve In Extensive Traits", "Choose the solution built for your type of institution.")}
 <div class="grid g3" data-stagger>
  <a class="plat-orig" href="early-years.html"><img src="{IMG}platform-1.png" alt="Early Years" loading="lazy"></a>
  <a class="plat-orig" href="school.html"><img src="{IMG}platform-2.png" alt="School" loading="lazy"></a>
  <a class="plat-orig" href="education-groups.html"><img src="{IMG}platform-3.png" alt="Education Institution" loading="lazy"></a>
 </div>
</div></section>
<section class="section section-soft"><div class="container">
 {head("", "Educore Genius Services", "Plug into Educore and electrify your school with these services, available for every type of institution.")}
 {rows}
</div></section>
{cta()}'''
pages["services"] = ("Services", "Educore Genius Services: KPIs, staff evaluation, transportation & bus tracking, online payments, staff attendance, team app, branded apps and automated timetables.", services())

# ===== EARLY YEARS
COMM = [("school-announcement.png","Announcements"),("notifications.png","Notifications"),("event.png","Events"),("note.png","Newsletter"),("media.png","Media"),("note.png","Notes"),
        ("online-class.png","Online Class"),("resources.png","Resources"),("incident-report.png","Incident Report"),("poll.png","Polls"),("survey.png","Surveys"),("agenda.png","Agenda"),
        ("exam.png","Exams"),("homework.png","Homework"),("activity.png","Activity"),("registration.png","Registration"),("parent-controls.png","Parent Controls"),("banners.png","Banners")]
def early():
    tiles = "".join(f'<div class="tile"><img src="{IMG}{i}" alt="" loading="lazy">{t}</div>' for i, t in COMM)
    return f'''
{phero([("services","Services"),(None,"Early Years")], "", 'Endless Possibilities with Educore Comprehensive Curriculum Compass', "Redefine early education with Educore’s dynamic approach to learning frameworks. Fuel young minds with curiosity and creativity through pathways that celebrate individuality and potential.", "early-years-hero.png", pills=["Customized curriculum","Daily engagement","Education","Communication"])}
{split("nurturing-ECE.png", "Nurturing ECE education", 'Holistic curriculum support', "Unlock tailored learning journeys that spark curiosity and ignite potential. From EYFS to Montessori, PYP to Reggio, we’re the compass guiding educators to success.",
  defs([("Curiosity-fueled exploration","Build your curriculum with an adaptable framework designed to spark joy and wonder in every child."),("Empower educators","Intuitive tools to track development, plan engaging activities and personalize learning."),("Guided success","Resources and insights at your fingertips make navigating the early years smoother than ever.")]))}
<section class="section"><div class="container">
 {head("", "Educore Montessori Curriculum", "Empower young minds with Educore’s Montessori curriculum support.")}
 <div class="vid-wide" data-reveal="zoom">{video("montessori")}</div>
</div></section>
<section class="section section-soft"><div class="container">
 {head("", "USP’S")}
 <div class="grid g3" data-stagger>
  <div class="card spot gborder"><div class="ic">{ic("book")}</div><h3>Curriculum Builder</h3>{checks(["Create an engaging curriculum tailored to your nursery","Integrate various educational standards","Develop, customize and manage curricula effortlessly"])}</div>
  <div class="card spot gborder"><div class="ic">{ic("chart")}</div><h3>Progress Analysis</h3>{checks(["Identify learning gaps against milestones","Create targeted strategies to close them","Ensure every child reaches full potential"])}</div>
  <div class="card spot gborder"><div class="ic">{ic("target")}</div><h3>Learning Goals Tracker</h3>{checks(["Monitor attendance, performance and progress in real time","Provide timely support and interventions","Track academic and developmental progress"])}</div>
 </div>
</div></section>
{split("student-progress.png", "Track & report", 'Track progress and generate gap analysis reports', "Educore helps you document and regularly record each student's progress and development.",
  checks(["Improve practices by implementing and tracking the best educational processes","Build your activity and lesson library and maintain daily logs","Observe pupils in action with detailed records of behavior, engagement and progress"]), rev=True)}
{split("multi-curriculum-management.png", "Multi-curriculum management", 'Many programs. One platform.', "Organize and administer multiple educational programs within a single platform.",
  checks(["Manage Montessori, Reggio or custom curricula","Provide personalized experiences for each child","Develop a clear weekday class routine"]), soft=True)}
{split("observations.png", "Observations", 'Capture learning as it happens', "Document and track students’ learning experiences in real time, capturing key strengths and areas for improvement.",
  defs([("Multi-curriculum compatible","Seamlessly integrate with various programs for flexible, adaptable teaching."),("EYFS","Align observations with the Early Years Foundation Stage framework."),("Montessori","Track self-directed activities and developmental milestones."),("Others","Consistent, thorough observation tracking across additional curricula.")]), rev=True)}
<section class="section section-soft"><div class="container">
 {head("", "Generate Learning Journals and Academic Reports")}
 <div class="grid g3" data-stagger>
  {card("form","Personal portfolios","Compile observations, work samples, photos and teacher notes into a portfolio for each child.")}
  {card("chart","Clear reports","Highlight strengths and areas needing attention in easy-to-read formats.")}
  {card("users","Parents in the loop","Give parents a comprehensive view of their child’s learning journey.")}
 </div>
</div></section>
<section class="section"><div class="container">
 {head("", "Transform School Communication with Educore", "Say goodbye to outdated methods and hello to seamless organization, from notifications to parent comments.")}
 <div class="icon-tiles" data-stagger>{tiles}</div>
</div></section>
{cta()}'''
pages["early-years"] = ("Early Years", "Educore Early Years: curriculum builder, progress analysis, observations, learning journals and multi-curriculum support for EYFS, Montessori, PYP and Reggio.", early())

# ===== SCHOOL
def school():
    return f'''
{phero([("services","Services"),(None,"School")], "", 'Educore All-In-One School Management System', "An Absolute Solution for School Administration. Crafted to Perfection for Every Institution's Needs.", "school-hero.png")}
{split("school-operations.png", "Streamline & enhance", 'Your school operations, centralized', "Educore brings together advanced pedagogical modules and a versatile multi-curricular system, transforming school management and faculty practice into one seamless, centralized experience. Save time, cut costs and boost efficiency across your institution.",
  badges=[("clock","Save time"),("trend","Boost efficiency")])}
<section class="section section-soft"><div class="container">
 {head("", "Explore Our Comprehensive Resources", "Foster administrative excellence with pedagogical flexibility and peer interaction on a thoughtfully designed platform.")}
</div></section>
{split("learning-management-system.png", "Learning Management System", 'A vibrant virtual classroom', "Supports synchronous and asynchronous learning with courses and content in various formats.", checks(["Access all teacher-shared resources","Submit assignments online","Foolproof online exam systems","Analyze student performance with ease","Group discussions with teachers"]), soft=True)}
{split("performance-analytics.png", "Performance Analytics", 'Track progress at every level', "A robust multi-user tool that tracks and assesses progress at student and class levels, with grade management and observational recording.", checks(["Implement and use statistical data","Record exam results for students and classes","Analyze demographic figures","Generate daily performance reports"]), rev=True)}
{split("online-assessment.png", "Online Assessment", 'Flexible assessments, your way', "Multiple-choice, matching, fill-in-the-blank, true/false, descriptive and more, with a reusable question bank.", checks(["Manage exam dates and times","Ensure curriculum coverage","Measure standards and competencies","Provide hints and feedback","Assign retakes for selected students"]), soft=True)}
{split("timetable-mangement.png", "Timetable Management", 'Organize the academic year automatically', "Create detailed schedules for courses and instructors, automated and accessible through the Educore mobile app.", checks(["Weekly subject planners for each class","Assign lessons to specific periods","Match instructors to each course","A clear weekday class routine"]), rev=True)}
{split("lesson-planing.png", "Lesson Planning", 'Plan lessons that deliver', "Curriculum coordinators and teachers manage detailed lesson plans; principals monitor progress across every grade section.", checks(["Set objectives and digital resources","Teaching resources and strategies","Learning differentiation","Evaluate lesson success","Highlight key questions and vocabulary"]), soft=True)}
{cta()}'''
pages["school"] = ("School", "Educore School: all-in-one school management with LMS, performance analytics, online assessment, timetable management and lesson planning.", school())

# ===== EDUCATION GROUPS
pages["education-groups"] = ("Education Institution", "Educore for education groups: classify data across academies, group analytics, training, a control dashboard and single-login protected access.", f'''
{phero([("services","Services"),(None,"Education Institution")], "", 'Empower Education Councils with an Imaginative Edge!', "Engineered to Ignite and Master Every Powerful Operation.", "education-group.png")}
<section class="section"><div class="container">
 {head("", "Discover Our Treasure Trove", "Toggle between academic dashboards, and tailor or standardize options to fit your institution's unique needs.")}
 <div class="bento" data-stagger>
  <div class="card spot span-3"><div class="ic">{ic("layers")}</div><h3>Information Classifying Dynamo</h3><p>High-octane classifying and labeling: organize information from diverse academies, turning complexity into clarity.</p><div class="art"><img src="{IMG}information-classifying.png" alt="" loading="lazy" style="max-height:220px"></div></div>
  <div class="card spot span-3"><div class="ic">{ic("chart")}</div><h3>Conduct Analyzing Blitz</h3><p>Monitor seat availability across all academies and customize analysis per school, raw data into strategic gold.</p><div class="art"><img src="{IMG}conduct-anaylzing.png" alt="" loading="lazy" style="max-height:220px"></div></div>
  <div class="card spot span-2 feature"><div class="ic">{ic("grad")}</div><h3>Training Exercise Extravaganza</h3><p>Complimentary training where new users swiftly grasp the system and experts explore the latest updates.</p></div>
  <div class="card spot span-2"><div class="ic">{ic("spark")}</div><h3>Active Execution Revolution</h3><p>Handle all school accounts from a control dashboard tailored for each academic level, accounts live in record time.</p></div>
  <div class="card spot span-2"><div class="ic">{ic("lock")}</div><h3>Protected Access Powerhouse</h3><p>Group admins access multiple school accounts with a single login and granular, per-staff permissions.</p></div>
 </div>
</div></section>
{split("active-execution.png", "Control dashboard", 'Every school account, one cockpit', "Submit your forms and details and watch your accounts spring into action, managed with turbocharged efficiency.", rev=True, soft=True)}
{split("protected-access.png", "Single sign-on", 'Switch schools seamlessly', "Group-level admins unlock the ultimate gateway to multiple school accounts, with granular permissions so everyone gets exactly what they need.", checks(["One login for every school","Granular, per-staff permissions","Standardize or tailor per school"]))}
{cta()}''')

# ===== FEATURES
FEATS = [
 ("Comprehensive Student Information System", [("student-profiles.png","Student Profiles","Detailed records including personal information, academic history, attendance and health records."),("parent-portal.png","Parent Portal","Parents view grades, attendance and school announcements.")]),
 ("Efficient Administration Tools", [("automated-schedule.png","Automated Scheduling","Create and manage class schedules, exams and events."),("admission-management.png","Admission Management","A streamlined process for applications, enrollments and admissions.")]),
 ("Academic Management", [("gradebook.png","Gradebook","Grade entry, progress reports and report cards."),("curriculum-management.png","Curriculum Management","Plan, manage and assess curriculum standards and lesson plans.")]),
 ("Enhanced Communication Features", [("messaging-system.png","Messaging System","Direct communication between teachers, students and parents."),("announcements.png","Announcements","School-wide notifications and updates.")]),
 ("Detailed Attendance Tracking", [("automated-attendance.png","Automated Attendance","Real-time tracking of attendance and absence management."),("reports-analytics.png","Reports & Analytics","Attendance insights and patterns at a glance.")]),
 ("Integrated Financial Management", [("fee-management.png","Fee Management","Manage tuition fees, track payments and generate invoices."),("expense-tracking.png","Expense Tracking","Record and manage school expenditures.")]),
 ("Human Resource Management", [("staff-records.png","Staff Records","Teacher and staff profiles, contracts and payroll."),("performance-evaluations.png","Performance Evaluations","Staff performance reviews and evaluations.")]),
 ("LMS, Learning Management System", [("online-classrooms.png","Online Classrooms","Virtual learning and online course management."),("performance-evaluations.png","Assignments & Assessments","Assign and grade student work.")]),
 ("Data Security and Privacy", [("secure-access.png","Secure Access","Role-based access and protected sign-in for every user."),("data-backup.png","Data Backup","Reliable backups on enterprise-grade, ISO 27001 certified infrastructure.")]),
]
def features():
    out = ""
    for n, (t, items) in enumerate(FEATS):
        cards = "".join(card(i, a, b, extra_cls="ill") for i, a, b in items)
        out += f'''<div class="split" style="align-items:start;padding:40px 0;border-top:1px solid var(--line)" data-reveal>
 <div style="position:sticky;top:120px"><h3 style="font-size:clamp(1.4rem,2.4vw,2rem)">{t}</h3></div>
 <div class="grid g2">{cards}</div></div>'''
    return f'''
{phero([(None,"Features")], "", 'Educore Core Features', "Discover the leading all-in-one solution for educational institutions with core features and innovative solutions designed to cover all school operations.", "core-features.png")}
<section class="section" style="padding-top:30px"><div class="container">{out}</div></section>
{cta()}'''
pages["features"] = ("Features", "Educore core features: student information system, administration tools, gradebook, communication, attendance, finance, HR, LMS and data security.", features())

for a in AREAS:
    names = ", ".join(m[1] for m in a["mods"])
    pages[f"modules-{a['key']}"] = (a["name"] + " Modules", f"Educore {a['name']} modules: {names}.", area_page(a))

def modules():
    blocks = "".join(f'''<div class="area" style="--area:{a["color"]}" data-reveal>
  <div class="area-head"><span class="area-ic">{ic(a["icon"])}</span><h2>{a["name"]}</h2></div>
  <p class="area-lead">{a["lead"]}</p>
  {mod_list(a, link_to_page=True)}
  <a class="btn btn-sm area-btn" href="{area_href(a)}">Explore {a["name"]} {ic("arrow")}</a>
 </div>''' for a in AREAS)
    return f'''
{phero([(None,"Modules")], "", 'Educore Modules', "Six functional areas, with each module grouped by its main purpose. Choose an area to see what it includes.", None, actions=False, pills=[a["name"] for a in AREAS])}
<section class="section" style="padding-top:20px"><div class="container"><div class="areas">{blocks}</div></div></section>
<section class="section section-soft" id="ai"><div class="container">
 <div class="ai-band" data-reveal>
  <div><span class="area-ic ai-ic">{ic("spark")}</span><h2>EducoreAI</h2><p>Top up your Educore with AI tokens and use AI across every area.</p></div>
  {checks(["Generate activities", "Generate lesson plans", "Enhance your communication and posts", "Enable translation for parents", "Use AI for your admissions and CRM"])}
 </div>
</div></section>
<section class="section" id="services"><div class="container">
 {head("", "Optional Services", "Available on request for schools that need them.")}
 <div class="grid g3" data-stagger>
  {card("cloud", "Private Server", "Your own private ecosystem on Oracle Cloud Infrastructure (OCI), with server maintenance and software updates.")}
  {card("globe", "School Website Integration", "Connect your school website to Educore with a Contact Us form and an online Registration application.")}
  {card("phone", "School-Branded Parent App", "EducoreParent built with your school logo and published on the App Store and Google Play.")}
 </div>
</div></section>
{cta()}'''
pages["modules"] = ("Modules", "Educore modules in six areas: Education, Operations, HR, ERP, Communication and Well-being.", modules())

# Old module page addresses redirect to the area that now contains them
REDIRECTS = {
 "educore-basic-module": "modules-operations.html#sis", "educore-academic-module": "modules-education.html",
 "educore-performance-analysis-module": "modules-education.html#analysis", "educore-crm-module": "modules-operations.html#crm",
 "educore-miscellaneous-module": "modules-operations.html", "educore-hrm-module": "modules-hr.html",
 "educore-finance-module": "modules-erp.html", "modules-finance": "modules-erp.html", "educore-communicator-module": "modules-communication.html#communicator",
}

# ===== MOBILE APP
pages["mobile-app"] = ("Mobile App", "The Educore mobile family: EducoreParent, EducoreTeacher, EducoreHealth, EducoreForms, EducoreTeam, EducoreStudent, EducoreAttendance and EducoreAppraisal.", f"""
{phero([(None,"Mobile App")], "", 'About Educore App', "Educore is a holistic system that serves the entire education system with a digitally empowered platform.", "educore-module-mobile-app.png")}
<section class="section"><div class="container">
 {head("", "Exclusive Mobile Family", "Eight apps for parents, teachers, students, staff and school receptions.")}
 {apps_block()}
</div></section>
<section class="section section-soft"><div class="container">
 {head("", "USP’s")}
 <div class="grid g3" data-stagger>
  {card("layers","All-in-one Holistic System","Every operation of an educational establishment, covered end to end.")}
  {card("puzzle","Highly adaptable","Configured to the way your institution works.")}
  {card("shield","Localized","As per the laws of local authorities.")}
  {card("lang","Multi-lingual","Serve families and staff in the languages they speak.")}
  {card("headset","Distinguished Professional First-line Support","A team that understands schools and childcare.")}
  {card("grid","Modular System","Start with what you need and add more as you grow.")}
 </div>
</div></section>
{cta()}""")

# ===== CERTIFICATES
def certs():
    ind = f'''
<div class="cert" data-reveal><div class="img"><img src="{IMG}page-certificate1.png" alt="ISO 27001 certificate" loading="lazy"></div><div><h3>ISO 27001:2022 Information Security Management System (ISMS)</h3><p>Confirms Educore's commitment to protecting sensitive data and managing information security risks.</p><div class="tags"><span>Information Security</span><span>Data Protection</span><span>Risk Management</span></div></div></div>
<div class="cert" data-reveal><div class="img"><img src="{IMG}page-certificate2.png" alt="ISO 9001 certificate" loading="lazy"></div><div><h3>ISO 9001:2015 Quality Management System</h3><p>Demonstrates our ability to consistently provide products and services that meet customer and regulatory requirements.</p><div class="tags"><span>Quality Management</span><span>Customer Satisfaction</span><span>Process Improvement</span></div></div></div>'''
    PART = [("page-certificate-3.png","Oracle Cloud Infrastructure","Cloud Infrastructure Partner","Our partnership with Oracle Cloud Infrastructure enables Educore to deliver enterprise-grade cloud computing with unmatched performance, security and cost savings.",["High-performance cloud infrastructure","Enhanced security and compliance","Scalable resources for institutions","Cost-effective cloud solutions"]),
            ("page-certificate-4.png","Oracle MySQL HeatWave","Database Technology Partner","Trusted partner for British Schools in the Middle East, powering Educore with enterprise-grade database performance and reliability.",["High-performance database engine","Enhanced security and compliance","Scales with your institution","Cost-effective operations"]),
            ("page-certificate-5.png","HIK Vision Partnership","Security Technology Partner","Integrates advanced security technology with our education management system for comprehensive campus safety and monitoring.",["Integrated campus security management","Real-time monitoring and alerts","Seamless integration with attendance","Advanced access control"])]
    par = "".join(f'<div class="cert" data-reveal><div class="img"><img src="{IMG}{i}" alt="{t}" loading="lazy"></div><div><h3>{t}</h3><p style="color:var(--purple);font-weight:600;margin-top:-4px">{s}</p><p>{d}</p>{checks(b, two=True)}</div></div>' for i, t, s, d, b in PART)
    return f'''
{phero([(None,"Certifications")], "", 'Certifications & Partnerships', "Discover how Educore's industry certifications and strategic partnerships ensure quality, security, and innovation in our educational technology solutions.", "certificates-hero.png", actions=False, pills=["ISO 9001:2015","ISO 27001:2022","Oracle OCI","MySQL HeatWave","HIK Vision"])}
<section class="section" style="padding-top:30px"><div class="container">
 <div class="tabs" data-tabs="c"><button class="on" type="button">Industry Certifications</button><button type="button">Strategic Partnerships</button></div>
 <div class="tab-panel on" data-panel-of="c">{head("", "Industry Certifications", "Our commitment to quality and security is backed by internationally recognized certifications.")}{ind}</div>
 <div class="tab-panel" data-panel-of="c">{head("", "Technology Partnerships", "We collaborate with industry leaders to provide innovative, reliable and secure solutions for educational institutions.")}{par}</div>
</div></section>
{cta()}'''
pages["certificates"] = ("Certifications", "Educore certifications and partnerships: ISO 9001:2015, ISO 27001:2022, Oracle Cloud Infrastructure, Oracle MySQL HeatWave and HIK Vision.", certs())

# ===== FORMS
def side(title, text):
    return f'''<div class="contact-side dark on-dark" data-reveal="left">{MESH}
<h2 style="font-size:clamp(1.6rem,3vw,2.3rem)">{title}</h2><p>{text}</p>
<div class="info-list" style="margin-top:28px">
 <div class="info"><span class="ic">{ic("map")}</span><div><b>Head office</b>Office 703, Wing B, DSO HQ Building, Dubai Silicon Oasis, Dubai, UAE</div></div>
 <div class="info"><span class="ic">{ic("tel")}</span><div><b>Phone / WhatsApp</b><a href="tel:+971504051555">+971 50 405 1555</a></div></div>
 <div class="info"><span class="ic">{ic("mail")}</span><div><b>Email</b><a href="mailto:info@ieducore.com">info@ieducore.com</a></div></div>
</div>
<div class="socials">{"".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{s}</a>' for n,(u,s) in SOCIAL.items())}</div></div>'''

def f(label, name, typ="text", full=False, req=True, ph=""):
    return f'<div class="field{" full" if full else ""}"><label for="{name}">{label}</label><input id="{name}" name="{name}" type="{typ}" placeholder="{ph}"{" required" if req else ""}></div>'
def sel(label, name, opts, full=False):
    o = "".join(f"<option>{x}</option>" for x in opts)
    return f'<div class="field{" full" if full else ""}"><label for="{name}">{label}</label><select id="{name}" name="{name}" required><option value="">Select…</option>{o}</select></div>'
def chips(label, name, opts, typ="checkbox"):
    o = "".join(f'<label><input type="{typ}" name="{name}" value="{x}"><span>{x}</span></label>' for x in opts)
    return f'<div class="field full"><label>{label}</label><div class="choices">{o}</div></div>'

COUNTRIES = "United Arab Emirates|Saudi Arabia|Qatar|Kuwait|Bahrain|Oman|Egypt|Jordan|Lebanon|Iraq|Morocco|Algeria|Tunisia|Libya|Sudan|Yemen|Palestine|Syria|Turkey|Pakistan|India|Bangladesh|Sri Lanka|Nepal|Afghanistan|Iran|Malaysia|Indonesia|Singapore|Philippines|Thailand|Vietnam|China|Hong Kong|Japan|South Korea|Australia|New Zealand|United Kingdom|Ireland|France|Germany|Italy|Spain|Portugal|Netherlands|Belgium|Switzerland|Austria|Sweden|Norway|Denmark|Finland|Poland|Greece|Cyprus|Romania|Bulgaria|Hungary|Czech Republic|Ukraine|Russia|Azerbaijan|Kazakhstan|Uzbekistan|Georgia|Armenia|United States|Canada|Mexico|Brazil|Argentina|Chile|Colombia|Peru|South Africa|Nigeria|Kenya|Ghana|Ethiopia|Tanzania|Uganda|Rwanda|Other".split("|")

pages["contact-us"] = ("Contact Us", "Contact Educore, Dubai Silicon Oasis, UAE. Phone +971 50 405 1555, email info@ieducore.com.", f'''
{phero([(None,"Contact Us")], "", 'Contact Us', "Send us a message and our team will get back to you.", None, actions=False)}
<section class="section" style="padding-top:10px"><div class="container"><div class="form-wrap">
 {side("We’d love to hear from you", "Reach out by form, phone or WhatsApp. Offices in Dubai, London, Toronto, Milan and Istanbul.")}
 <form class="form-card" data-demo="Thanks! Your message has been sent." data-reveal="right"><div class="fields">
  {f("Name","name",ph="Your full name")}{f("Email","email","email",ph="you@school.com")}
  {f("Subject","subject",full=True,ph="How can we help?")}
  <div class="field full"><label for="message">Message</label><textarea id="message" name="message" required placeholder="Tell us about your institution…"></textarea></div>
 </div><button class="btn" style="margin-top:22px" data-magnetic>Send Message {ic("arrow")}</button></form>
</div></div></section>''')

INTERESTS = [("book","Education","LMS, Early Years, IB, Attendance, Appointment, Analysis, Library, Digital Library, Timetable, ECA"),
 ("gear","Operations","SIS, CRM, Admission, Workflow, Transport, Dismissal, Menu, Withdrawal, Report Center"),
 ("team","HR","HRM, Recruitment, Payroll, Evaluation, AdminEvaluation, Teams"),
 ("db","ERP","Billing, Finance, Assets, Inventory, Payments, Budgets, Marketplace, External Operations"),
 ("chat","Communication","Communicator, Alumni, Chat Monitor, EducoreParent, EducoreTeacher"),
 ("pulse","Well-being","Health, SEN, Concerns, SEP"),
 ("spark","EducoreAI","AI for lesson plans, activities, posts, translation and admissions"),
 ("cloud","Optional services","Private server, website integration, school-branded app")]
TICK = '<span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg></span>'
INTEREST_CARDS = "".join(f'<label class="ccard"><input type="checkbox" name="interests" value="{t}" data-label="Interests"><span class="ci2">{ic(i)}</span><span><b>{t}</b><small>{d}</small></span>{TICK}</label>' for i, t, d in INTERESTS)
def lf(label, name, typ="text"):
    return f'<div class="field"><label for="{name}">{label}</label><input id="{name}" name="{name}" type="{typ}" required data-label="{label}"></div>'

pages["get-started"] = ("Get a Quote", "Get a quote for Educore, school management, LMS, early years, finance, HR, payroll, CRM and admissions.", f'''
{phero([(None,"Get a Quote")], "", 'Let’s Start a Journey of Success', "Tell us about your institution and the modules you are interested in, and we will send you a quote.", None, actions=False)}
<section class="section" style="padding-top:10px"><div class="container"><div class="form-wrap">
 {side("Your tailored quote, fast", "Onboarding takes about a day, we can migrate data from your existing system.")}
 <form class="form-card" data-steps data-demo="Thanks! Our team will be in touch with your quote." data-reveal="right">
  <div class="stepper" aria-hidden="true"><span><i>1</i>Details</span><span><i>2</i>Interests</span><span><i>3</i>Review</span></div>
  <div class="fstep"><h3>Your details</h3><p>Tell us who you are and where your institution is.</p><div class="fields">
   {lf("Your Name","name")}{lf("Institution","institution")}
   {lf("Email Address","email","email")}{lf("Phone Number","phone","tel")}
   <div class="field full"><label for="country">Your Country</label><select id="country" name="country" required data-label="Country"><option value="">Select your country</option>{"".join(f"<option>{c}</option>" for c in COUNTRIES)}</select></div>
  </div></div>
  <div class="fstep"><h3>Your interests</h3><p>Choose everything you would like a quote for.</p>
   <div class="ccards" data-min-one>{INTEREST_CARDS}</div><p class="step-err" role="alert">Please choose at least one option.</p></div>
  <div class="fstep"><h3>Review</h3><p>Check your details before sending.</p><dl class="review"></dl></div>
  <div class="step-actions"><button type="button" class="btn btn-ghost" data-prev>Back</button><button type="button" class="btn" data-next>Continue {ic("arrow")}</button><button class="btn" data-send hidden>Get in Touch {ic("arrow")}</button></div>
 </form>
</div></div></section>''')

pages["registration"] = ("Setup School", "Sign up with Educore and set up your school, nursery, ELC, training centre or SEN institution.", f'''
{phero([(None,"Setup School")], "", 'Sign Up With Us!', "Register your institution and our team will contact you to set up your school.", None, actions=False)}
<section class="section" style="padding-top:10px"><div class="container" style="max-width:900px">
 <form class="form-card" data-demo="Registration received! We’ll contact you to set up your school." data-reveal><div class="fields">
  {chips("Your Title","title",["Miss","Ms.","Mr.","Mrs."],"radio")}
  {f("Your Name","name")}{f("Institution Name","institution")}
  {chips("Gender","gender",["Boys","Girls","Mix"],"radio")}
  {chips("Cycles","cycles",["KinderGarten","Cycle 1","Cycle 2","Cycle 3"])}
  <div class="field full"><label for="desc">Institution Description</label><textarea id="desc" name="description" style="min-height:100px"></textarea></div>
  {chips("Organization State","state",["Public","Private"],"radio")}
  {chips("Type","type",["Nursery","School","ELC","Training Centre","SEN"],"radio")}
  {f("Phone","phone","tel")}{f("Email","email","email")}
  {sel("Country","country",COUNTRIES,full=True)}
 </div><button class="btn" style="margin-top:24px" data-magnetic>Register {ic("arrow")}</button></form>
</div></section>''')

# ===== LEGAL
def legal(key, name):
    data = json.load(open(SRC / f"{key}.json"))
    # split combined source: terms = before data-protection heading, privacy = from it
    idx = next(i for i, (t, d) in enumerate(data) if d.upper().startswith("EDUCORE DATA PROTECTION"))
    items = data[1:idx] if key == "terms" else data[idx:]
    toc, body, n = [], [], 0
    for t, d in items:
        e = html.escape(d)
        if t == "h3":
            n += 1; sid = f"s{n}"
            toc.append(f'<a href="#{sid}">{e}</a>'); body.append(f'<h3 id="{sid}">{e}</h3>')
        elif t in ("h4", "h5", "h6"): body.append(f"<h5>{e}</h5>")
        elif t == "li": body.append(f"<ul><li>{e}</li></ul>")
        elif t in ("b", "strong") and body and body[-1].startswith("<p>"): body[-1] = body[-1][:-4] + f" <b>{e}</b></p>"
        elif t in ("a", "span", "b", "strong", "em", "i") and body and body[-1].startswith("<p>"): body[-1] = body[-1][:-4] + f" {e}</p>"
        else: body.append(f"<p>{e}</p>")
    b = "\n".join(body).replace("</ul>\n<ul>", "\n")
    return f'''
{phero([(None,name)], "", name, "Last updated on August 10, 2021. Educore Systems and Technologies FZE.", None, actions=False)}
<section class="section" style="padding-top:10px"><div class="container"><div class="legal">
 <nav><b>On this page</b>{"".join(toc)}</nav><article class="prose">{b}</article>
</div></div></section>'''
pages["terms"] = ("Terms of Service", "Educore terms of use and conditions.", legal("terms", "Terms of Service"))
pages["privacy"] = ("Privacy Policy", "Educore data protection and privacy policy.", legal("privacy", "Privacy Policy"))

# ---------------------------------------------------------------- write
for key, (title, desc, body) in pages.items():
    (OUT / href(key)).write_text(page(key, title, desc, body), encoding="utf-8")
for old, new in REDIRECTS.items():
    (OUT / f"{old}.html").write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved · Educore</title><meta http-equiv="refresh" content="0; url={new}"><link rel="canonical" href="{new}"></head><body><p>This page has moved to <a href="{new}">{new}</a>.</p></body></html>', encoding="utf-8")
print(f"Built {len(pages)} pages → {OUT}")
