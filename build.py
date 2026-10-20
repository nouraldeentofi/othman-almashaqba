#!/usr/bin/env python3
"""Builds Othman Almashaqba's personal site: six pages, Arabic (RTL, default) and English.

Every visible string is written twice, Arabic then English, in one HTML file per page;
the language button swaps them in place. The script also writes the machine-readable
layer: JSON-LD on every page, llms.txt, llms-full.txt, robots.txt and sitemap.xml.

Edit the text below, then run:  python3 build.py
Every fact here traces to brief.md (his LinkedIn profile, his posts and his own site)."""
import html, json, os
from urllib.parse import quote

# ----------------------------------------------------------------------------------
# CONFIG: the only things you normally change. Empty values stay hidden on the site.
# ----------------------------------------------------------------------------------
CONFIG = {
    "BASE_URL": "https://nouraldeentofi.github.io/othman-almashaqba",  # later: his own domain, e.g. "https://othmanalmashaqba.com"
    "PROTOTYPE": True,      # True = noindex (search engines skip it) until Othman approves; then set False and rebuild
    "PHOTO": "assets/img/othman-634.jpg",
    "EMAIL": "othmancs@hotmail.com",
    "PHONE": "+966595094009",          # digits with +, shown as PHONE_SHOW
    "PHONE_SHOW": "+966 59 509 4009",
    "WHATSAPP": "",                    # international digits only, e.g. "966595094009"; empty = no WhatsApp button
    "LINKEDIN": "https://www.linkedin.com/in/othman-almashaqba-b243a2b9/",
    "MAKER": "https://nouraldeentofi.com",  # the site's designer and developer
}
VER = "8"  # bump when CSS/JS change, so browsers fetch the new files

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = CONFIG["BASE_URL"].rstrip("/")
OG_IMG = "assets/img/og.jpg"


def url(path=""):
    if path in ("index.html", ""):
        return BASE + "/"
    return BASE + "/" + path


def esc(s):
    return html.escape(s, quote=True)


def t(ar, en, tag="span", cls="", attrs=""):
    """The same thing in both languages. CSS shows the one that matches <html lang>."""
    c = f' class="{cls}"' if cls else ""
    a = f" {attrs}" if attrs else ""
    return f'<{tag} data-l="ar"{c}{a}>{ar}</{tag}><{tag} data-l="en" lang="en"{c}{a}>{en}</{tag}>'


def L(s):
    """A Latin or numeric run inside Arabic text, kept left-to-right."""
    return f'<span dir="ltr">{s}</span>'


def al(ar, en):
    """A bilingual accessible name; site.js swaps it with the language."""
    return f'aria-label="{esc(ar)}" data-al-ar="{esc(ar)}" data-al-en="{esc(en)}"'


# ----------------------------------------------------------------------------------
# Icons: one set, 24px grid, 1.75 stroke, round ends
# ----------------------------------------------------------------------------------
_S = 'viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "mail": f'<svg {_S}><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7.5 8 5.5 8-5.5"/></svg>',
    "phone": f'<svg {_S}><path d="M6.6 3.5h2.6l1.6 4.4-2.2 1.4a11.6 11.6 0 0 0 6.1 6.1l1.4-2.2 4.4 1.6v2.6a2.1 2.1 0 0 1-2.3 2.1A16.5 16.5 0 0 1 4.5 5.8a2.1 2.1 0 0 1 2.1-2.3z"/></svg>',
    "pin": f'<svg {_S}><path d="M12 21s-6.5-5.7-6.5-11a6.5 6.5 0 0 1 13 0c0 5.3-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/></svg>',
    "home": f'<svg {_S}><path d="M4 11 12 4.5l8 6.5"/><path d="M6 9.5V20h4.5v-5.5h3V20H18V9.5"/></svg>',
    "story": f'<svg {_S}><path d="M12 7.2C10 5.6 7.4 5 4 5v13c3.4 0 6 .6 8 2.2 2-1.6 4.6-2.2 8-2.2V5c-3.4 0-6 .6-8 2.2z"/><path d="M12 7.2V20"/></svg>',
    "approach": f'<svg {_S}><circle cx="12" cy="12" r="8.5"/><path d="m15.4 8.6-2 4.8-4.8 2 2-4.8z"/></svg>',
    "work": f'<svg {_S}><path d="M12 4 3.5 8.3 12 12.6l8.5-4.3z"/><path d="m3.5 12.2 8.5 4.3 8.5-4.3"/><path d="m3.5 16 8.5 4.3 8.5-4.3"/></svg>',
    "knowledge": f'<svg {_S}><path d="M2.5 9.4 12 5l9.5 4.4L12 13.8z"/><path d="M6.5 11.3v4.4c1.6 1.4 3.5 2.1 5.5 2.1s3.9-.7 5.5-2.1v-4.4"/><path d="M21.5 9.4v5"/></svg>',
    "chat": f'<svg {_S}><path d="M20 14.6a2.2 2.2 0 0 1-2.2 2.2H9.4L5 20.3V6.2A2.2 2.2 0 0 1 7.2 4h10.6A2.2 2.2 0 0 1 20 6.2z"/><path d="M8.5 9h7M8.5 12.5h4.5"/></svg>',
    "sun": f'<svg {_S}><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></svg>',
    "moon": f'<svg {_S}><path d="M19.5 14.6A7.8 7.8 0 1 1 9.4 4.5a6.3 6.3 0 0 0 10.1 10.1z"/></svg>',
    "menu": f'<svg {_S}><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "close": f'<svg {_S}><path d="m6 6 12 12M18 6 6 18"/></svg>',
    "copy": f'<svg {_S}><rect x="8.5" y="8.5" width="11" height="11" rx="2.2"/><path d="M15.5 5.5v-.3A1.7 1.7 0 0 0 13.8 3.5H5.2a1.7 1.7 0 0 0-1.7 1.7v8.6a1.7 1.7 0 0 0 1.7 1.7h.3"/></svg>',
    "check": f'<svg {_S}><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
    "prev": f'<svg {_S}><path d="m9 6 6 6-6 6"/></svg>',
    "next": f'<svg {_S}><path d="m15 6-6 6 6 6"/></svg>',
    "out": f'<svg {_S}><path d="M14 4h6v6M20 4l-8.5 8.5"/><path d="M19 14v4.5a1.5 1.5 0 0 1-1.5 1.5h-12A1.5 1.5 0 0 1 4 18.5v-12A1.5 1.5 0 0 1 5.5 5H10"/></svg>',
    "target": f'<svg {_S}><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.8"/><circle cx="12" cy="12" r="1.2"/></svg>',
    "layers": f'<svg {_S}><rect x="3.5" y="4" width="17" height="6" rx="1.8"/><rect x="3.5" y="14" width="7.5" height="6" rx="1.8"/><rect x="13" y="14" width="7.5" height="6" rx="1.8"/><path d="M12 10v2M7.2 12h9.6M7.2 12v2M16.8 12v2"/></svg>',
    "cloud": f'<svg {_S}><path d="M7.2 18.5h9.9a4 4 0 0 0 .6-7.9 6 6 0 0 0-11.5-1A4.5 4.5 0 0 0 7.2 18.5z"/></svg>',
    "shield": f'<svg {_S}><path d="M12 3.3 4.8 6.1v5.3c0 4.4 3 8.1 7.2 9.3 4.2-1.2 7.2-4.9 7.2-9.3V6.1z"/><path d="m9 12 2.2 2.2L15.2 10"/></svg>',
    "data": f'<svg {_S}><ellipse cx="12" cy="6" rx="7" ry="2.7"/><path d="M5 6v12c0 1.5 3.1 2.7 7 2.7s7-1.2 7-2.7V6"/><path d="M5 12c0 1.5 3.1 2.7 7 2.7s7-1.2 7-2.7"/></svg>',
    "chip": f'<svg {_S}><rect x="6.5" y="6.5" width="11" height="11" rx="2.4"/><path d="M10 3.5v3M14 3.5v3M10 17.5v3M14 17.5v3M3.5 10h3M3.5 14h3M17.5 10h3M17.5 14h3"/><path d="M10 12h4"/></svg>',
    "doc": f'<svg {_S}><path d="M7 3.5h6.8L18.5 8v12.5H7z"/><path d="M13.5 3.5V8h5M10 12.5h5.5M10 16h5.5"/></svg>',
    "award": f'<svg {_S}><circle cx="12" cy="9" r="5.2"/><path d="M8.7 13.2 7.5 20.5l4.5-2.3 4.5 2.3-1.2-7.3"/></svg>',
    "lang": f'<svg {_S}><circle cx="12" cy="12" r="8.5"/><path d="M3.8 9h16.4M3.8 15h16.4M12 3.5c-2.4 2.4-3.5 5.2-3.5 8.5s1.1 6.1 3.5 8.5c2.4-2.4 3.5-5.2 3.5-8.5S14.4 5.9 12 3.5z"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm5.8 14.03c-.25.69-1.44 1.32-1.98 1.37-.51.05-1.15.07-1.85-.12-.43-.13-.97-.31-1.67-.61-2.95-1.27-4.87-4.24-5.02-4.44-.15-.2-1.2-1.6-1.2-3.05 0-1.45.76-2.16 1.03-2.46.27-.3.59-.37.79-.37h.57c.18 0 .43-.07.67.51.25.59.84 2.04.91 2.19.07.15.12.32.02.52-.1.2-.15.32-.3.49-.15.17-.31.39-.45.52-.15.15-.3.31-.13.61.17.3.77 1.27 1.65 2.06 1.14 1.01 2.1 1.33 2.4 1.48.3.15.47.12.65-.07.17-.2.74-.86.94-1.16.2-.3.39-.25.67-.15.27.1 1.73.82 2.03.97.3.15.49.22.57.35.07.12.07.71-.17 1.4Z"/></svg>',
    "li": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13ZM7.12 20.45H3.56V9h3.56v11.45ZM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0Z"/></svg>',
}


def icon(k, cls="ic"):
    return ICONS[k].replace("<svg ", f'<svg class="{cls}" ', 1)


# his mark: three threads, tangled at the start of the line and straight at its end
MARK = ('<svg class="mark" viewBox="0 0 40 40" aria-hidden="true">'
        '<path class="mk-a" d="M37 10C30 6 25 15 28 19S35 16 30 13 22 14 18 14H3"/>'
        '<path class="mk-c" d="M37 20C32 25 27 13 22 18S19 20 17 20H3"/>'
        '<path class="mk-b" d="M37 30C30 34 27 22 23 24S21 26 18 26H3"/></svg>')

# ----------------------------------------------------------------------------------
# Who he is, for people and for machines
# ----------------------------------------------------------------------------------
NAME_EN, NAME_AR = "Othman Almashaqba", "عثمان المشاقبة"
NAMES = [NAME_EN, NAME_AR, "Othman Al-Mashaqba", "Othman Al Mashaqba", "Othman Almashaqbeh", "Othman Al-Mashaqbeh",
         "Othman Mashaqba", "Osman Almashaqba", "Uthman Almashaqba", "Othman Almashaqbah", "عثمان مشاقبة",
         "المهندس عثمان المشاقبة", "م. عثمان المشاقبة", "Eng. Othman Almashaqba"]
ROLES_EN = ["Technology Leader", "CTO", "IT Director", "Head of Technology", "Chief Technology Officer", "IT Manager",
            "ERP Project Manager", "ERP Program Manager", "ERP Strategy", "Digital Transformation Leader",
            "Enterprise Architect", "IT Governance", "Odoo ERP expert", "Odoo consultant", "Technology strategy"]
ROLES_AR = ["قائد تقنية", "مدير تقنية المعلومات", "رئيس التقنية", "مدير تقني تنفيذي", "مدير مشروع ERP",
            "استراتيجية ERP", "قائد التحول الرقمي", "خبير أودو", "مستشار Odoo", "حوكمة تقنية المعلومات",
            "المعمارية المؤسسية", "استراتيجية التقنية", "تخطيط موارد المؤسسات"]
KNOWS = ["Technology strategy", "Digital transformation", "Enterprise Resource Planning (ERP)", "Odoo", "Odoo ERP implementation",
         "ERP data migration", "IT governance", "COBIT", "ITIL", "ISO 27001", "Enterprise architecture", "TOGAF",
         "Cloud migration", "Cloud governance", "FinOps", "Cybersecurity", "Business continuity", "Disaster recovery",
         "Data governance", "Data analytics", "Business intelligence", "AI governance", "Responsible AI",
         "Change management", "Process re-engineering", "IT service management", "Python", "AWS", "Microsoft Azure",
         "ZATCA integration requirements"]
KEYWORDS = NAMES[:6] + ROLES_EN[:8] + ROLES_AR[:7] + ["Riyadh", "الرياض", "Saudi Arabia", "Odoo 8–19"]

BIO_EN = ("Othman Almashaqba (عثمان المشاقبة) is a technology leader based in Riyadh, Saudi Arabia. Since 2014 he has worked "
          "across Jordan, the UAE and Saudi Arabia on technology strategy, ERP modernisation, digital transformation and IT "
          "governance. He has led more than ten enterprise ERP transformation programmes, including Odoo from version 8 to 19, "
          "and works on ERP strategy at Meela Investment Company in Riyadh.")
BIO_AR = ("عثمان المشاقبة قائد تقنية مقيم في الرياض. يعمل منذ 2014 بين الأردن والإمارات والسعودية في استراتيجية التقنية "
          "وتحديث أنظمة ERP والتحول الرقمي وحوكمة تقنية المعلومات، وقاد أكثر من عشرة برامج تحول ERP مؤسسية بينها Odoo من "
          "الإصدار 8 حتى 19، ويعمل اليوم على استراتيجية ERP في Meela Investment Company بالرياض.")

# ----------------------------------------------------------------------------------
# Navigation
# ----------------------------------------------------------------------------------
NAV = [("index", "الرئيسية", "Home", "home"), ("story", "القصة", "Story", "story"),
       ("approach", "المنهج", "Approach", "approach"), ("work", "الأعمال", "Work", "work"),
       ("knowledge", "المعرفة", "Knowledge", "knowledge"), ("contact", "تواصل", "Contact", "chat")]
DOCK = ["index", "story", "contact", "work", "approach"]  # contact sits raised in the middle

# ----------------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------------
RESULTS = [  # all his own figures, see brief.md
    dict(id="cost", ar="تكاليف تشغيل التقنية", en="Technology operating costs", kind="bars", before=100, after=85,
         sign="−", to=15, ctx_ar=f"بالحوكمة والتحسين وإدارة الموردين، في مجموعة العمران",
         ctx_en="Through governance, optimisation and vendor management at Alomran Group"),
    dict(id="perf", ar="أداء البنية التحتية", en="Infrastructure performance", kind="bars", before=100, after=120,
         sign="+", to=20, ctx_ar="بالترحيل إلى السحابة والأتمتة، في مجموعة العمران",
         ctx_en="Through cloud migration and automation at Alomran Group"),
    dict(id="down", ar="توقف الأنظمة", en="System downtime", kind="bars", before=100, after=70,
         sign="−", to=30, ctx_ar="وقت أقل تكون فيه الأنظمة متوقفة عن العمل",
         ctx_en="Less time with business systems down"),
    dict(id="acc", ar="دقة ترحيل البيانات", en="Data migration accuracy", kind="dots", sign="", to=99.9, dec=1,
         ctx_ar=f"999 من كل 1000 سجل، في ترحيلات بيانات مؤسسية معقدة مع {L('No Errors IT Services')}",
         ctx_en="999 of every 1,000 records, in complex enterprise data migrations with No Errors IT Services"),
]

VOICES = [
    ("كل مشروع تقني يبدأ من الناس الذين سيستخدمونه.",
     "Every technology project starts with the people who will use it.",
     "أجلس معهم وأسمع ما يعطّل عملهم، ثم أختار الحل: ربط أنظمة، أو أتمتة إجراء، أو نقل خدمة إلى السحابة، وأمن المعلومات حاضر من البداية.",
     "I sit with them and hear what slows their work down, then choose the fix: connecting systems, automating a step or moving a service to the cloud, with security there from the start."),
    ("لا تضع نظامًا جديدًا فوق بيروقراطية قديمة.",
     "Don’t put a new system on top of old bureaucracy.",
     "تقنية حديثة فوق إجراء مكسور ليست تحولًا رقميًا؛ إنها تجعل الفوضى أسرع وأغلى.",
     "Modern technology on a broken process is not digital transformation. It just makes the chaos faster and more expensive."),
    ("غيّر عملياتك لتناسب أفضل الممارسات، قبل أن تغيّر النظام ليناسب عملياتك.",
     "Change your processes to fit best practice before you change the system to fit your processes.",
     "كل تخصيص زائد اليوم يصير دينًا تقنيًا غدًا، عند التحديث أو الربط أو الانتقال إلى السحابة.",
     "Every extra customisation today becomes technical debt tomorrow, when you upgrade, integrate or move to the cloud."),
    ("الأمن ثقافة وحوكمة، لا منتج تشتريه وتنساه.",
     "Security is culture and governance, not a product you buy and forget.",
     "يُبنى من أحدث موظف حتى مجلس الإدارة: صلاحيات بقدر المهام، وخطط تعافٍ مجرّبة، ووعي كل يوم.",
     "It is built from the newest employee to the board: access that matches the job, tested recovery plans, everyday awareness."),
    ("قبل أن تتوسع في الذكاء الاصطناعي: من يقرر؟ من يراجع؟ ومن يتحمل المسؤولية؟",
     "Before you scale AI: who decides, who reviews, and who is accountable?",
     "القيمة تظهر حين تعرف المؤسسة متى تثق به، ومتى تتحداه، ومتى تتجاهله.",
     "The value shows when an organisation knows when to trust it, when to challenge it and when to ignore it."),
]

STATIONS = [  # year, place, organisation, one line
    ("2014", "الأردن", "Jordan", "اليونيسف", "UNICEF",
     "الدعم التقني وتحليل البيانات لمشاريع اليونيسف.", "Technical support and data analysis for UNICEF projects."),
    ("2018", "الأردن", "Jordan", L("Shahwan"), "Shahwan",
     f"تطوير وحدات {L('Odoo')} من الإصدار 8 إلى 13.", "Building Odoo modules, versions 8 to 13."),
    ("2020", "دبي", "Dubai", L("No Errors IT Services"), "No Errors IT Services",
     "إدارة تقنية المعلومات وفريقها وسياساتها وميزانياتها.", "Running IT, its team, policies and budgets."),
    ("2021", "الأردن", "Jordan", f"{L('CellBay')} و {L('Smart Rock')}", "CellBay & Smart Rock",
     f"إدارة تقنية المعلومات، وتحول {L('ERP')} على {L('Odoo 13')}.", "Running IT, and an ERP transformation on Odoo 13."),
    ("2022", "السعودية", "Saudi Arabia", "مجموعة العمران", "Alomran Group",
     "استراتيجية التقنية، وتحول ERP، وحوكمة تقنية المعلومات.", "Technology strategy, ERP transformation and IT governance."),
    ("2025", "الرياض", "Riyadh", L("Meela Investment Company"), "Meela Investment Company",
     "استراتيجية ERP في خدمة قرارات الاستثمار.", "ERP strategy in service of investment decisions."),
]

# Odoo programmes placed on the 8–19 scale (Alomran's version is unconfirmed, so it is not placed)
VERSIONS = list(range(8, 20))
ON_RULER = [
    dict(id="shahwan", at=8.5, row=0, v="8–9", org_ar=L("Shahwan Group"), org_en="Shahwan Group", place_ar="الأردن", place_en="Jordan",
         ar="أسس التحول: وحدات ERP مترابطة وأتمتة، على الإصدارين 8 و9.", en="The foundations: connected ERP modules and automation, on versions 8 and 9."),
    dict(id="romex", at=13, row=0, v="13", org_ar=L("Romex Dubai"), org_en="Romex Dubai", place_ar="دبي", place_en="Dubai",
         ar="منصة ERP وتجارة إلكترونية في منظومة واحدة.", en="An ERP and e-commerce platform in one system."),
    dict(id="cellbay", at=13, row=1, v="13", org_ar=L("CellBay Jordan"), org_en="CellBay Jordan", place_ar="الأردن", place_en="Jordan",
         ar="تحول ERP مؤسسي، من الأنظمة إلى الأتمتة.", en="An enterprise ERP transformation, from systems to automation."),
    dict(id="meela", at=18, row=0, v="18", org_ar=L("Meela Investment"), org_en="Meela Investment", place_ar="الرياض", place_en="Riyadh",
         ar="منصة ERP وإدارة أصول لشركة استثمار.", en="An ERP and asset-management platform for an investment company."),
    dict(id="toto", at=19, row=1, v="19", org_ar=L("TOTO Saudi Arabia"), org_en="TOTO Saudi Arabia", place_ar="السعودية", place_en="Saudi Arabia",
         ar="تحول ERP على أحدث جيل من Odoo.", en="An ERP transformation on the newest generation of Odoo."),
]

PROGRAMMES = [
    dict(tag="Odoo 8 · 9", org_ar=L("Shahwan Group"), org_en="Shahwan Group", place_ar="الأردن", place_en="Jordan",
         ar="أسس التحول المؤسسي: وحدات للموارد البشرية والرواتب وسجلات الوقت والدعم، مترابطة ومؤتمتة.",
         en="Foundations of the enterprise system: HR, payroll, timesheet and support modules, connected and automated."),
    dict(tag="Odoo 13", org_ar=L("Romex Dubai"), org_en="Romex Dubai", place_ar="دبي", place_en="Dubai",
         ar="منصة ERP وتجارة إلكترونية في منظومة واحدة.",
         en="An ERP and e-commerce platform in one system."),
    dict(tag="Odoo 13", org_ar=L("CellBay Jordan"), org_en="CellBay Jordan", place_ar="الأردن", place_en="Jordan",
         ar="تحول ERP مؤسسي، من الأنظمة إلى الأتمتة.",
         en="An enterprise ERP transformation, from systems to automation."),
    dict(tag="Odoo", org_ar="مجموعة العمران", org_en="Alomran Group", place_ar="السعودية", place_en="Saudi Arabia",
         ar="تحول ERP عبر عدة وظائف، بحوكمة مبنية على COBIT وITIL.",
         en="An ERP transformation across several functions, governed with COBIT and ITIL."),
    dict(tag="Odoo 19", org_ar=L("TOTO Saudi Arabia"), org_en="TOTO Saudi Arabia", place_ar="السعودية", place_en="Saudi Arabia",
         ar="تحول ERP على أحدث جيل من Odoo.", en="An ERP transformation on the newest generation of Odoo."),
    dict(tag="Odoo 18", org_ar=L("Meela Investment"), org_en="Meela Investment", place_ar="الرياض", place_en="Riyadh",
         ar="منصة ERP وإدارة أصول، تربط التقنية بعمليات الاستثمار وقرار الإدارة.",
         en="An ERP and asset-management platform that ties technology to investment operations and management decisions."),
    dict(tag_ar="تحول رقمي", tag_en="Digital", org_ar=L("Mina Hotel"), org_en="Mina Hotel", place_ar="أبها", place_en="Abha",
         ar="برنامج تحول رقمي في قطاع الضيافة.", en="A digital transformation programme in hospitality."),
    dict(tag_ar="ذكاء اصطناعي", tag_en="AI", org_ar=L("Enterprise IT Quality Platform"), org_en="Enterprise IT Quality Platform",
         place_ar="حوكمة وجودة", place_en="Governance & quality",
         ar="حل قائم على الذكاء الاصطناعي لحوكمة تقنية المعلومات وإدارة الجودة.",
         en="An AI-based solution for IT governance and quality management."),
]

MODULES = [("المالية", "Finance"), ("الموارد البشرية والرواتب", "HR & payroll"), ("إدارة العملاء", "CRM"),
           ("المبيعات", "Sales"), ("المشتريات", "Purchasing"), ("المخزون", "Inventory"), ("نقاط البيع", "Point of sale"),
           ("التجارة الإلكترونية", "E-commerce"), ("التصنيع", "Manufacturing"), ("المشاريع", "Projects"),
           ("التسويق", "Marketing"), ("الأسطول", "Fleet")]

AREAS = [
    ("target", "الاستراتيجية والحوكمة", "Strategy & governance",
     "خطط التقنية وميزانياتها ومخاطرها في خدمة أولويات العمل، على COBIT وITIL.",
     "Technology roadmaps, budgets and risk in service of business priorities, on COBIT and ITIL."),
    ("layers", "ERP والتطبيقات المؤسسية", "ERP & enterprise applications",
     "تحديث ERP، والتكاملات، وترحيل البيانات، وإعادة تصميم العمليات.",
     "ERP modernisation, integrations, data migration and process redesign."),
    ("cloud", "البنية التحتية والسحابة", "Infrastructure & cloud",
     "عمليات تقنية آمنة وقابلة للتوسع، وانتقال إلى السحابة بحوكمة وضبط للتكلفة.",
     "Secure, scalable IT operations, and moves to the cloud with governance and cost control."),
    ("shield", "الأمن والمخاطر", "Security & risk",
     "ضوابط متوافقة مع ISO 27001، وصلاحيات بقدر المهام، واستمرارية أعمال وخطط تعافٍ.",
     "ISO 27001-aligned controls, access that matches the job, business continuity and recovery plans."),
    ("data", "البيانات والتحليلات", "Data & analytics",
     "حوكمة البيانات، وذكاء أعمال يوصل المعلومة إلى صاحب القرار.",
     "Data governance, and business intelligence that gets information to the person deciding."),
    ("chip", "الذكاء الاصطناعي في العمليات", "AI-enabled operations",
     "ذكاء اصطناعي بحوكمة واضحة: من يقرر، ومن يراجع، ومن يتحمل المسؤولية.",
     "AI with clear governance: who decides, who reviews, who is accountable."),
]

CHAPTERS = [
    dict(y="2010–2014", place_ar="الأردن", place_en="Jordan", org_ar="جامعة آل البيت", org_en="Al al-Bayt University",
         role_ar="بكالوريوس علوم الحاسوب", role_en="Bachelor’s degree, Computer Science",
         ar="بدأت من علوم الحاسوب، وما زلت أنظر إلى المؤسسات بعين المتخصص فيها: في الأنظمة لا نقيس الأداء بالدقة وحدها، بل بزمن الاستجابة أيضًا.",
         en="It began with computer science, and I still look at organisations as a computer scientist: in systems, performance is not only accuracy, it is response time too."),
    dict(y="2014–2018", place_ar="الأردن", place_en="Jordan", org_ar="اليونيسف", org_en="UNICEF",
         role_ar="الدعم التقني وتحليل البيانات", role_en="Technical support & data analysis",
         ar="قدّمت الدعم التقني وتحليل البيانات لمشاريع اليونيسف في الأردن: أنظمة يجب أن تبقى موثوقة، وبيانات تُجمع وتتحول إلى تقارير لتقييم البرامج.",
         en="I provided technical support and data analysis for UNICEF projects in Jordan: systems that had to stay reliable, and data collected and turned into reports to evaluate programmes.",
         q_ar="إذا لم نستطع قياس الفرق قبل التقنية وبعدها، فربما نجحنا في تنفيذ مشروع، لا في تحقيق تحول.",
         q_en="If we can’t measure the difference before and after the technology, we may have delivered a project, not a transformation."),
    dict(y="2018–2020", place_ar="الأردن", place_en="Jordan", org_ar=L("Shahwan"), org_en="Shahwan",
         role_ar=f"مطوّر {L('Odoo')} بلغة {L('Python')}", role_en="Odoo developer (Python)",
         ar=f"كتبت وحدات {L('Odoo')} وصنتها من الإصدار 8 حتى 13، وربطت وحدات الموارد البشرية والرواتب وسجلات الوقت والدعم، بلغات {L('Python')} و{L('XML')} و{L('JavaScript')} و{L('SQL')}.",
         en="I built and maintained Odoo modules from version 8 to 13, and integrated the HR, payroll, timesheet and support modules, in Python, XML, JavaScript and SQL.",
         q_ar="كل تعديل برمجي يُطلب لإرضاء طريقة عمل ترفض أن تتغير، يصير غدًا دينًا تقنيًا.",
         q_en="Every custom change made to please a way of working that refuses to change becomes technical debt tomorrow."),
    dict(y="2020–2021", place_ar="دبي، الإمارات", place_en="Dubai, UAE", org_ar=L("No Errors IT Services"), org_en="No Errors IT Services",
         role_ar=f"مدير تقنية المعلومات، {L('Odoo')} والدعم التقني", role_en="IT Manager, Odoo & technical support",
         ar=f"أدرت أنظمة تقنية المعلومات وعمليات البيانات، ووظّفت فريق التقنية ودرّبته وقيّمت أداءه، ووضعت سياسات التقنية وإجراءاتها وضوابطها الأمنية، وأدرت ميزانياتها. ومن هذه المرحلة ترحيلات بيانات مؤسسية بدقة {L('99.9%')}.",
         en="I ran IT systems and data operations, hired, trained and evaluated the IT team, wrote the IT policies, procedures and security controls, and managed the budgets. Enterprise data migrations at 99.9% accuracy come from this period.",
         q_ar="هل نملك أسسًا واضحة وممارسات قياسية، أم ندير التقنية بالاجتهادات الشخصية؟",
         q_en="Do we have clear foundations and standard practices, or are we running technology on personal judgement?"),
    dict(y="2020–2022", place_ar="الأردن", place_en="Jordan", org_ar="جامعة العلوم التطبيقية", org_en="Applied Science University",
         role_ar="ماجستير علوم الحاسوب", role_en="Master’s degree, Computer Science",
         ar="وإلى جانب العمل، أكملت الماجستير في علوم الحاسوب.",
         en="Alongside the work, I completed a master’s degree in computer science."),
    dict(y="2021–2023", place_ar="الأردن", place_en="Jordan", org_ar=f"{L('Marshall School')}، {L('Smart Rock')}، {L('CellBay')}",
         org_en="Marshall School, Smart Rock & CellBay", role_ar="مدير تقنية المعلومات", role_en="IT Manager",
         ar=f"أدرت تقنية المعلومات في مدرسة ثم في شركتين: استمرارية الأعمال، وفريق الدعم، والترقيات، وأمن البيانات والامتثال. وفي {L('CellBay')} قدت تحول {L('ERP')} على {L('Odoo 13')}، من الأنظمة إلى الأتمتة.",
         en="I ran IT for a school and then for two companies: business continuity, the support team, upgrades, data security and compliance. At CellBay I led an ERP transformation on Odoo 13, from systems to automation.",
         q_ar=f"التحول الرقمي الناجح {L('80%')} منه إدارة تغيير وهندسة عمليات، و{L('20%')} فقط برمجة وتقنية.",
         q_en="Successful digital transformation is 80% change management and process re-engineering, and only 20% code and technology."),
    dict(y="2022–2025", place_ar="السعودية", place_en="Saudi Arabia", org_ar="مجموعة العمران", org_en="Alomran Group",
         role_ar="قيادة التقنية والتحول", role_en="Leading technology and transformation",
         ar=f"وضعت استراتيجية التقنية للمؤسسة ونفّذتها، وقدت تحول {L('ERP')} على {L('Odoo')} عبر عدة وظائف، ورفعت أداء البنية التحتية {L('20%')} بالترحيل إلى السحابة والأتمتة، وبنيت حوكمة تقنية المعلومات على {L('COBIT')} و{L('ITIL')}، وخفّضت تكاليف التقنية {L('15%')}.",
         en="I defined and delivered the company’s technology strategy, led an ERP transformation on Odoo across several functions, lifted infrastructure performance by 20% through cloud migration and automation, built IT governance on COBIT and ITIL, and cut technology costs by 15%.",
         q_ar="الأساس دائمًا يسبق الأداة.", q_en="The foundation always comes before the tool."),
    dict(y="2025–اليوم", y_en="2025–today", place_ar="الرياض", place_en="Riyadh", org_ar=L("Meela Investment Company"), org_en="Meela Investment Company",
         role_ar="استراتيجية ERP والتقنية", role_en="ERP & technology strategy",
         ar=f"أقود استراتيجية {L('ERP')} للتحول والنمو في شركة استثمار، وأوائم معمارية النظام مع عمليات الاستثمار وقرارات الإدارة التنفيذية، وأشرف على قابلية التوسع والتكاملات وحوكمة البيانات، وأقدّم المشورة في الاستثمار التقني ومخاطره.",
         en="At an investment company, I lead ERP strategy for transformation and growth, align the system’s architecture with investment operations and executive decisions, oversee scalability, integrations and data governance, and advise management on technology investment and its risks.",
         q_ar="الهدف أن نقلّل الوقت الضائع بين المعرفة والفعل، دون أن نضحّي بجودة القرار.",
         q_en="The aim is to cut the time lost between knowing and acting, without giving up the quality of the decision."),
]

STEPS = [
    ("أفهم السياق", "Understand the context",
     "أبدأ بالعمل وأنظمته وأولوياته: أجلس مع من سيستخدم الحل، وأسمع ما يعطّل يومه.",
     "I start with the business, its systems and its priorities: I sit with the people who will use the solution and hear what slows their day."),
    ("أبني الاتجاه", "Set the direction",
     "أحوّل الأهداف إلى أولويات تقنية واضحة، وأوازن بين القيمة والمخاطر والتكلفة.",
     "I turn goals into clear technology priorities, weighing value, risk and cost."),
    ("أربط التنفيذ", "Connect the delivery",
     "أربط الأنظمة والبيانات وعمليات التقنية بالفرق والموردين الذين يعتمدون عليها.",
     "I connect systems, data and IT operations to the teams and vendors who depend on them."),
    ("أقرأ الأثر", "Read the impact",
     "هل وفّرنا وقتًا؟ هل قلّت الأخطاء؟ هل تصل المعلومة إلى الشخص الصحيح في الوقت المناسب؟",
     "Did we save time? Are there fewer errors? Does the information reach the right person at the right moment?"),
]

BELIEFS = [
    ("الناس أولًا", "People first",
     "كل مشروع تقني يبدأ من الناس الذين سيستخدمونه، لا من النظام.",
     "Every technology project starts with the people who will use it, not with the system."),
    ("لا رقمنة للفوضى", "Don’t digitise chaos",
     "لا تضع نظامًا جديدًا فوق بيروقراطية قديمة؛ أعد هندسة الإجراء أولًا.",
     "Don’t put a new system on top of old bureaucracy; re-engineer the process first."),
    ("أفضل الممارسات قبل التخصيص", "Best practice before customisation",
     "غيّر عملياتك لتناسب أفضل الممارسات في النظام، قبل أن تغيّر النظام ليناسب عملياتك.",
     "Change your processes to fit the best practice in the system before you change the system to fit your processes."),
    ("الأساس قبل الأداة", "Foundation before tools",
     "السحابة نموذج تشغيل مختلف، لا مركز بيانات بديل: نظّف البيانات، وأعد هيكلة التطبيقات، وضع الحوكمة، ثم انتقل.",
     "The cloud is a different operating model, not a spare data centre: clean the data, restructure the applications, set the governance, then move."),
    ("الأمن ثقافة", "Security is culture",
     "الأمن ليس منتجًا يوضع في غرفة الخوادم ويُنسى؛ إنه حوكمة ووعي من أحدث موظف حتى مجلس الإدارة.",
     "Security is not a product you put in the server room and forget; it is governance and awareness from the newest employee to the board."),
    ("التقنية شريك في القرار", "IT is a partner",
     "قسم التقنية ليس فرقة إطفاء للأعطال؛ إنه شريك يحوّل الإنفاق إلى قيمة تمكّن العمل.",
     "The IT department is not a fire brigade for outages; it is a partner that turns spending into value that enables the business."),
    ("قِس ما تغيّر", "Measure what changed",
     "عدد الأنظمة التي أطلقناها ليس المؤشر. المؤشر هو ما تغيّر في العمل بعد الاستثمار.",
     "The number of systems launched is not the measure. The measure is what changed in the business after the investment."),
    ("المسؤولية قبل الذكاء الاصطناعي", "Accountability before AI",
     "قبل التوسع: من يقرر؟ من يراجع؟ ومن يتحمل المسؤولية؟",
     "Before scaling: who decides, who reviews, and who is accountable?"),
]

FRAMEWORKS = [("COBIT", "حوكمة تقنية المعلومات وربطها بأهداف المؤسسة", "Governing IT and tying it to business goals"),
              ("ITIL", "إدارة خدمات التقنية بمعايير واضحة", "Running IT services to clear standards"),
              ("ISO 27001", "ضوابط أمن المعلومات", "Information security controls")]

EDUCATION = [
    ("2020–2022", "ماجستير علوم الحاسوب", "Master’s degree, Computer Science", "جامعة العلوم التطبيقية", "Applied Science University"),
    ("2010–2014", "بكالوريوس علوم الحاسوب", "Bachelor’s degree, Computer Science", "جامعة آل البيت", "Al al-Bayt University"),
]

RESEARCH = [
    dict(field_ar="الأمن والسجلات الموزّعة", field_en="Security & distributed ledgers",
         title_ar="أمن دورة الاختبارات الرقمية", title_en="Securing the digital exam lifecycle",
         ar=f"معمارية {L('SSExam')} تربط التسجيل، وتسليم الأسئلة مشفّرة، والإجابات الموقّعة، والتصحيح، وشهادات يمكن التحقق منها، وتفصل الهوية والمحتوى عن السجل.",
         en="The SSExam architecture links registration, encrypted question delivery, signed answers, grading and verifiable certificates, and keeps identity and content apart from the ledger.",
         journal="Information Security Journal: A Global Perspective"),
    dict(field_ar="الصحة والتوائم الرقمية", field_en="Health & digital twins",
         title_ar="توائم رقمية لرعاية وقائية", title_en="Digital twins for preventive care",
         ar="إطار تنفيذي لتوائم رقمية مدعومة بالذكاء الاصطناعي للوقاية من الأمراض المزمنة في السعودية، بحوكمة بشرية ومسؤولية واضحة عن الخدمة.",
         en="An executive framework for AI-supported digital twins in chronic-disease prevention in Saudi Arabia, with human governance and clear accountability for the service.",
         journal="International Journal of Healthcare Management"),
    dict(field_ar="الذكاء المكاني والعقار", field_en="Spatial AI & real estate",
         title_ar=f"تقييم عقاري قابل للتفسير بـ {L('GeoAI')}", title_en="Explainable GeoAI for property valuation",
         ar="بروتوكول يجمع البيانات المنظمة والصور والنص العربي والسياق المكاني لتحليل العقار السكني في السعودية، مع تتبّع المصادر وعدم اليقين وتفسيرات قابلة للتدقيق.",
         en="A protocol that combines structured data, images, Arabic text and spatial context to analyse Saudi residential property, with source tracing, uncertainty and auditable explanations.",
         journal="Applied Geomatics"),
]

CERTS = [("PMP", "إدارة المشاريع", "Project Management Professional", "PMI"),
         ("AWS", "معماري حلول، المستوى الاحترافي", "Solutions Architect – Professional", "Amazon Web Services"),
         ("Azure", "خبير معمارية الحلول", "Solutions Architect Expert", "Microsoft"),
         ("CISM", "إدارة أمن المعلومات", "Certified Information Security Manager", "ISACA"),
         ("TOGAF", "المعمارية المؤسسية", "Enterprise Architecture", "The Open Group")]

TOPICS = [("lead", "قيادة التقنية", "Technology leadership", "حوار حول قيادة التقنية", "A conversation about technology leadership"),
          ("transform", "التحول المؤسسي", "Enterprise transformation", "حوار حول التحول المؤسسي", "A conversation about enterprise transformation"),
          ("erp", f"ERP و{L('Odoo')}", "ERP & Odoo", "حوار حول ERP وOdoo", "A conversation about ERP and Odoo"),
          ("ai", "الذكاء الاصطناعي المسؤول", "Responsible AI", "حوار حول الذكاء الاصطناعي المسؤول", "A conversation about responsible AI"),
          ("other", "موضوع آخر", "Something else", "رسالة من موقعك", "A message from your website")]

FAQ = [
    ("من هو عثمان المشاقبة؟", "Who is Othman Almashaqba?",
     f"قائد تقنية مقيم في الرياض. يعمل منذ 2014 بين الأردن والإمارات والسعودية في استراتيجية التقنية وتحولات {L('ERP')} وحوكمة تقنية المعلومات، ويعمل اليوم على استراتيجية {L('ERP')} في {L('Meela Investment Company')}.",
     "A technology leader based in Riyadh. Since 2014 he has worked across Jordan, the UAE and Saudi Arabia on technology strategy, ERP transformation and IT governance, and he now works on ERP strategy at Meela Investment Company."),
    ("ما مجالات خبرته؟", "What does he specialise in?",
     f"استراتيجية التقنية والتحول الرقمي، و{L('ERP')} و{L('Odoo')}، وحوكمة تقنية المعلومات على {L('COBIT')} و{L('ITIL')} بضوابط متوافقة مع {L('ISO 27001')}، والمعمارية المؤسسية، والسحابة، والأمن السيبراني، والبيانات والتحليلات، والذكاء الاصطناعي في العمليات.",
     "Technology strategy and digital transformation, ERP and Odoo, IT governance on COBIT and ITIL with ISO 27001-aligned controls, enterprise architecture, cloud, cybersecurity, data and analytics, and AI-enabled operations."),
    ("مع أي إصدارات Odoo عمل؟", "Which Odoo versions has he worked with?",
     f"من الإصدار 8 حتى 19، في أكثر من عشرة برامج تحول {L('ERP')}، منها تطوير وحدات {L('Odoo')} بلغة {L('Python')} على الإصدارات من 8 إلى 13.",
     "From version 8 to 19, across more than ten ERP transformation programmes, including building Odoo modules in Python for versions 8 to 13."),
    ("أين عمل؟", "Where has he worked?",
     f"في الأردن: اليونيسف و{L('Shahwan')} و{L('Marshall School')} و{L('Smart Rock')} و{L('CellBay')}. وفي دبي: {L('No Errors IT Services')}. وفي السعودية: مجموعة العمران، ثم {L('Meela Investment Company')} في الرياض.",
     "In Jordan: UNICEF, Shahwan, Marshall School, Smart Rock and CellBay. In Dubai: No Errors IT Services. In Saudi Arabia: Alomran Group, then Meela Investment Company in Riyadh."),
    ("كيف أتواصل معه؟", "How can I reach him?",
     f"بالبريد {L(CONFIG['EMAIL'])}، أو بالهاتف {L(CONFIG['PHONE_SHOW'])}، أو برسالة على {L('LinkedIn')}.",
     f"By email at {CONFIG['EMAIL']}, by phone on {CONFIG['PHONE_SHOW']}, or with a LinkedIn message."),
]


def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


# ----------------------------------------------------------------------------------
# Page chrome
# ----------------------------------------------------------------------------------
def header(cur):
    links = "".join(
        f'<a href="{s}.html"{" aria-current=\"page\"" if s == cur else ""}>{t(a, e)}</a>' for s, a, e, _ in NAV)
    return f'''<a class="skip" href="#main">{t("انتقل إلى المحتوى", "Skip to content")}</a>
<header class="top" id="top">
  <div class="top-glass" aria-hidden="true"></div>
  <div class="wrap top-in">
    <a class="brand" href="index.html" {al("عثمان المشاقبة، الصفحة الرئيسية", "Othman Almashaqba, home")}>{MARK}<span class="brand-txt">{t("<b>عثمان المشاقبة</b><small>قيادة التقنية والتحول</small>", "<b>Othman Almashaqba</b><small>Technology leadership</small>")}</span></a>
    <nav class="nav" {al("الصفحات", "Pages")}>{links}</nav>
    <div class="acts">
      <button class="icon-btn" id="themeBtn" type="button" {al("الوضع الداكن", "Dark mode")}>{icon("moon", "ic i-moon")}{icon("sun", "ic i-sun")}</button>
      <button class="lang-btn" id="langBtn" type="button" lang="en" aria-label="Switch to English">EN</button>
      <a class="btn btn-ink btn-sm top-cta" href="contact.html">{t("راسلني", "Get in touch")}</a>
      <button class="icon-btn menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="sheet" {al("القائمة", "Menu")}>{icon("menu", "ic i-menu")}{icon("close", "ic i-close")}</button>
    </div>
  </div>
  <span class="progress" aria-hidden="true"></span>
</header>'''


def sheet(cur):
    links = "".join(
        f'<a href="{s}.html"{" aria-current=\"page\"" if s == cur else ""} style="--k:{i}">{icon(ic)}{t(a, e)}</a>'
        for i, (s, a, e, ic) in enumerate(NAV))
    return f'''<div class="sheet" id="sheet" hidden>
  <div class="sheet-panel glass" role="dialog" aria-modal="true" {al("القائمة", "Menu")}>
    <nav class="sheet-nav">{links}</nav>
    <div class="sheet-foot">
      <a class="btn btn-ink" href="mailto:{CONFIG['EMAIL']}">{icon("mail")}{t("راسلني بالبريد", "Email me")}</a>
      <a class="btn btn-line js-li" href="{CONFIG['LINKEDIN']}" rel="noopener" target="_blank">{icon("li")}LinkedIn</a>
    </div>
  </div>
</div>'''


def dock(cur):
    items = []
    for s in DOCK:
        _, a, e, ic = next(n for n in NAV if n[0] == s)
        main = " dock-main" if s == "contact" else ""
        cur_attr = ' aria-current="page"' if s == cur else ""
        items.append(f'<a class="dock-i{main}" href="{s}.html"{cur_attr}><span class="dock-ic">{icon(ic)}</span>{t(a, e, cls="dock-t")}</a>')
    return f'<nav class="dock glass" id="dock" {al("التنقل", "Navigation")}>{"".join(items)}</nav>'


def contact_cards(cls="cards-contact"):
    c = CONFIG
    out = []
    if c["EMAIL"]:
        out.append(f'<a class="ccard" href="mailto:{c["EMAIL"]}"><span class="ccard-ic">{icon("mail")}</span><span class="ccard-txt">{t("البريد الإلكتروني", "Email")}<b dir="ltr">{c["EMAIL"]}</b></span></a>')
    if c["PHONE"]:
        out.append(f'<a class="ccard" href="tel:{c["PHONE"]}"><span class="ccard-ic">{icon("phone")}</span><span class="ccard-txt">{t("الهاتف", "Phone")}<b dir="ltr">{c["PHONE_SHOW"]}</b></span></a>')
    if c["WHATSAPP"]:
        out.append(f'<a class="ccard" href="https://wa.me/{c["WHATSAPP"]}" rel="noopener" target="_blank"><span class="ccard-ic">{icon("wa")}</span><span class="ccard-txt">{t("واتساب", "WhatsApp")}<b dir="ltr">+{c["WHATSAPP"]}</b></span></a>')
    if c["LINKEDIN"]:
        out.append(f'<a class="ccard js-li" href="{c["LINKEDIN"]}" rel="me noopener" target="_blank"><span class="ccard-ic">{icon("li")}</span><span class="ccard-txt">LinkedIn<b>{t("عثمان المشاقبة", "Othman Almashaqba")}</b></span></a>')
    return f'<div class="{cls}">{"".join(out)}</div>'


def footer(cur):
    links = "".join(f'<a href="{s}.html">{t(a, e)}</a>' for s, a, e, _ in NAV)
    cards = "" if cur == "contact" else contact_cards("cards-contact foot-cards")
    m = CONFIG["MAKER"]
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">{MARK}<p>{t("<b>عثمان المشاقبة</b><span>قيادة التقنية والتحول المؤسسي، من الرياض.</span>", "<b>Othman Almashaqba</b><span>Technology leadership and enterprise transformation, from Riyadh.</span>")}</p></div>
      <nav class="foot-nav" {al("صفحات الموقع", "Site pages")}>{links}</nav>
    </div>
    {cards}
    <div class="foot-base">
      <span>{t("© 2026 عثمان المشاقبة", "© 2026 Othman Almashaqba")}</span>
      <p class="credit">{t("تصميم وتطوير", "Designed &amp; built by")} <a href="{m}" rel="noopener" target="_blank" lang="ar" dir="rtl">نور الدين طفي</a><span class="sep" aria-hidden="true">·</span><a href="{m}" rel="noopener" target="_blank" lang="en" dir="ltr">Nour Aldeen Tofi</a></p>
    </div>
  </div>
</footer>'''


def cta_band():
    return f'''<section class="cta-band" aria-labelledby="ctaH">
  <canvas class="threads" data-threads="band" data-density="soft" aria-hidden="true"></canvas>
  <div class="wrap cta-in">
    <h2 class="h2" id="ctaH">{t("لنتحدث عن قيادة التقنية، أو التحول المؤسسي، أو ERP، أو الذكاء الاصطناعي المسؤول.", "Let’s talk technology leadership, enterprise transformation, ERP or responsible AI.")}</h2>
    <div class="cta-row">
      <a class="btn btn-paper shine" href="mailto:{CONFIG['EMAIL']}">{icon("mail")}{t("راسلني بالبريد", "Email me")}</a>
      <a class="btn btn-glass js-li" href="{CONFIG['LINKEDIN']}" rel="noopener" target="_blank">{icon("li")}LinkedIn</a>
    </div>
  </div>
</section>'''


def sec_head(h_ar, h_en, p_ar=None, p_en=None, hid=None, more=None):
    i = f' id="{hid}"' if hid else ""
    p = f'<p class="lede rv">{t(p_ar, p_en)}</p>' if p_ar else ""
    m = ""
    if more:
        href, ma, me = more
        m = f'<a class="more rv" href="{href}">{t(ma, me)}<span class="more-ic" aria-hidden="true">{icon("next")}</span></a>'
    return f'<div class="sec-head"><h2 class="h2 rv-h"{i}>{t(h_ar, h_en)}</h2>{p}{m}</div>'


def portrait(sizes="(max-width: 760px) 92vw, 400px", eager=True):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="assets/img/othman-400.webp 400w, assets/img/othman-634.webp 634w" sizes="{sizes}">'
            f'<img src="assets/img/othman-634.jpg" srcset="assets/img/othman-400.jpg 400w, assets/img/othman-634.jpg 634w" sizes="{sizes}" '
            f'width="634" height="792" {load} decoding="async" alt="{esc("عثمان المشاقبة")}" data-alt-ar="{esc("عثمان المشاقبة")}" data-alt-en="{esc("Othman Almashaqba")}"></picture>')


# ----------------------------------------------------------------------------------
# Components
# ----------------------------------------------------------------------------------
def measure(prefix="m"):
    items = []
    for r in RESULTS:
        if r["kind"] == "bars":
            mx = max(r["before"], r["after"])
            vis = (f'<div class="m-vis bars"><div class="bar b0"><span>{t("قبل", "Before")}</span><i style="--w:{r["before"] / mx:.3f}"></i></div>'
                   f'<div class="bar b1"><span>{t("بعد", "After")}</span><i style="--w:{r["after"] / mx:.3f}"></i></div></div>')
            final = f'{r["sign"]}{r["to"]}%'
            num = f'<span class="count" data-to="{r["to"]}" data-sign="{r["sign"]}" data-suffix="%">{final}</span>'
        else:
            pid = f"{prefix}dots"
            vis = (f'<div class="m-vis dots"><svg viewBox="0 0 250 100" aria-hidden="true">'
                   f'<defs><pattern id="{pid}" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.45"/></pattern></defs>'
                   f'<rect class="dots-all" width="250" height="100" fill="url(#{pid})"/>'
                   f'<circle class="dot-miss" cx="187.5" cy="62.5" r="2.1"/></svg></div>')
            num = f'<span class="count" data-to="{r["to"]}" data-dec="{r["dec"]}" data-suffix="%">{r["to"]}%</span>'
        items.append(f'''<li class="m-item rv">
  <h3 class="m-title">{t(r["ar"], r["en"])}</h3>
  {vis}
  <p class="m-num" dir="ltr">{num}</p>
  <p class="m-ctx">{t(r["ctx_ar"], r["ctx_en"])}</p>
</li>''')
    return f'<ul class="measure swipe" role="list" data-swipe>{"".join(items)}</ul><div class="swipe-dots" aria-hidden="true"></div>'


def voices():
    figs, tabs = [], []
    for i, (qa, qe, sa, se) in enumerate(VOICES):
        on = i == 0
        figs.append(f'<figure class="voice{" is-on" if on else ""}" id="voice{i}" role="tabpanel" aria-labelledby="vtab{i}"{"" if on else " aria-hidden=\"true\" inert"}>'
                    f'<blockquote class="voice-q">{t(qa, qe, tag="p")}</blockquote>'
                    f'<figcaption class="voice-sub">{t(sa, se)}</figcaption></figure>')
        tabs.append(f'<button class="vtab" id="vtab{i}" type="button" role="tab" aria-controls="voice{i}" aria-selected="{"true" if on else "false"}" '
                    f'{al(f"الفكرة {i + 1} من {len(VOICES)}", f"Idea {i + 1} of {len(VOICES)}")}><i></i></button>')
    return f'''<div class="bed">
<canvas class="threads" data-threads="band" data-density="soft" aria-hidden="true"></canvas>
<div class="voices glass rv" data-rotator data-interval="7500">
  <div class="voices-stage">{"".join(figs)}</div>
  <div class="voices-ctl">
    <button class="icon-btn vprev" type="button" {al("السابق", "Previous")}>{icon("prev")}</button>
    <div class="vtabs" role="tablist" {al("أفكار", "Ideas")}>{"".join(tabs)}</div>
    <button class="icon-btn vnext" type="button" {al("التالي", "Next")}>{icon("next")}</button>
  </div>
</div>
</div>'''


def journey():
    lis = []
    for i, (y, pa, pe, oa, oe, la, le) in enumerate(STATIONS):
        lis.append(f'<li class="st rv" style="--k:{i}"><span class="st-dot" aria-hidden="true"></span>'
                   f'<span class="st-year" dir="ltr">{y}</span><span class="st-place">{t(pa, pe)}</span>'
                   f'<b class="st-org">{t(oa, oe)}</b><p class="st-line">{t(la, le)}</p></li>')
    return f'''<div class="journey">
  <ol class="stations swipe" data-swipe>{"".join(lis)}</ol>
  <div class="swipe-dots" aria-hidden="true"></div>
</div>'''


def ruler(full=False):
    ticks = "".join(f'<li class="tick" style="--i:{i}"><span dir="ltr">{v}</span></li>' for i, v in enumerate(VERSIONS))
    marks, panels = [], []
    for k, p in enumerate(ON_RULER):
        pos = (p["at"] - 8 + 0.5) / len(VERSIONS)
        on = k == 0
        nm_ar, nm_en = strip_tags(p["org_ar"]), p["org_en"]
        marks.append(f'<button class="rmark{" is-on" if on else ""}" type="button" role="tab" id="rm-{p["id"]}" aria-controls="rp-{p["id"]}" {al(f"{nm_ar}، Odoo {p['v']}", f"{nm_en}, Odoo {p['v']}")} '
                     f'aria-selected="{"true" if on else "false"}" style="--pos:{pos:.4f};--row:{p["row"]}">'
                     f'<span class="rmark-dot" aria-hidden="true"></span><span class="rmark-l">{t(p["org_ar"], p["org_en"])}</span></button>')
        panels.append(f'<div class="rpanel{" is-on" if on else ""}" id="rp-{p["id"]}" role="tabpanel" aria-labelledby="rm-{p["id"]}"{"" if on else " aria-hidden=\"true\" inert"}>'
                      f'<p class="rp-v" dir="ltr">Odoo {p["v"]}</p>'
                      f'<p class="rp-org">{t(p["org_ar"], p["org_en"], tag="b")}<span class="rp-place">{icon("pin", "ic ic-s")}{t(p["place_ar"], p["place_en"])}</span></p>'
                      f'<p class="rp-txt">{t(p["ar"], p["en"])}</p></div>')
    return f'''<div class="bed bed-lanes">
<div class="ruler glass rv" data-ruler data-interval="5200">
  <div class="ruler-track">
    <div class="ruler-marks" role="tablist" {al("برامج على مقياس الإصدارات", "Programmes on the version scale")}>{"".join(marks)}</div>
    <ol class="ruler-ticks" aria-hidden="true">{ticks}</ol>
    <p class="ruler-cap">{t("إصدارات Odoo", "Odoo versions")}</p>
  </div>
  <div class="ruler-panels">{"".join(panels)}</div>
</div>
</div>'''


def programme_cards():
    out = []
    for p in PROGRAMMES:
        tag = t(p["tag_ar"], p["tag_en"]) if "tag_ar" in p else f'<span dir="ltr">{p["tag"]}</span>'
        out.append(f'''<li class="prog rv">
  <span class="prog-tag">{tag}</span>
  <h3 class="prog-org">{t(p["org_ar"], p["org_en"])}</h3>
  <p class="prog-txt">{t(p["ar"], p["en"])}</p>
  <p class="prog-place">{icon("pin", "ic ic-s")}{t(p["place_ar"], p["place_en"])}</p>
</li>''')
    return f'<ul class="progs swipe" role="list" data-swipe>{"".join(out)}</ul><div class="swipe-dots" aria-hidden="true"></div>'


def module_map():
    n = len(MODULES)
    import math
    nodes, lines = [], []
    for i, (a, e) in enumerate(MODULES):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        x, y = 50 + 41 * math.cos(ang), 50 + 40 * math.sin(ang)
        nodes.append(f'<li class="mod" style="--x:{x:.2f}%;--y:{y:.2f}%;--k:{i}">{t(a, e)}</li>')
        cx, cy = 300 + 246 * math.cos(ang), 200 + 160 * math.sin(ang)
        mx, my = 300 + 120 * math.cos(ang + .35), 200 + 80 * math.sin(ang + .35)
        lines.append(f'<path d="M300 200 Q{mx:.1f} {my:.1f} {cx:.1f} {cy:.1f}" pathLength="1" style="--k:{i}"/>')
    return f'''<div class="modmap rv">
  <svg class="modmap-lines" viewBox="0 0 600 400" preserveAspectRatio="none" aria-hidden="true"><g class="ml-base">{"".join(lines)}</g><g class="ml-flow">{"".join(lines)}</g></svg>
  <div class="mod-core"><b dir="ltr">Odoo</b>{t("نظام واحد", "One system")}</div>
  <ul class="mods" role="list">{"".join(nodes)}</ul>
</div>'''


def area_cards():
    out = []
    for ic, a, e, da, de in AREAS:
        out.append(f'<li class="area rv"><span class="area-ic">{icon(ic)}</span><h3 class="h3">{t(a, e)}</h3><p>{t(da, de)}</p></li>')
    return f'<ul class="areas swipe" role="list" data-swipe>{"".join(out)}</ul><div class="swipe-dots" aria-hidden="true"></div>'


def research_cards(compact=False):
    out = []
    for r in RESEARCH:
        body = "" if compact else f'<p class="rs-txt">{t(r["ar"], r["en"])}</p>'
        out.append(f'''<li class="rs rv">
  <span class="rs-field">{icon("doc", "ic ic-s")}{t(r["field_ar"], r["field_en"])}</span>
  <h3 class="h3">{t(r["title_ar"], r["title_en"])}</h3>
  {body}
  <p class="rs-status">{t("مقدّمة للنشر في", "Submitted to")} <i lang="en" dir="ltr">{r["journal"]}</i></p>
</li>''')
    return f'<ul class="research swipe" role="list" data-swipe>{"".join(out)}</ul><div class="swipe-dots" aria-hidden="true"></div>'


def cert_tiles():
    out = []
    for code, a, e, org in CERTS:
        out.append(f'<li class="cert rv"><b dir="ltr">{code}</b><span>{t(a, e)}</span><small dir="ltr">{org}</small></li>')
    return f'<ul class="certs" role="list">{"".join(out)}</ul>'


# ----------------------------------------------------------------------------------
# Structured data
# ----------------------------------------------------------------------------------
def person():
    c = CONFIG
    p = {
        "@type": "Person", "@id": url() + "#othman", "name": NAME_EN, "alternateName": NAMES[1:],
        "givenName": "Othman", "familyName": "Almashaqba",
        "jobTitle": ["Technology Leader", "ERP & Technology Strategy", "Enterprise Resources Planning Project Manager"],
        "description": BIO_EN,
        "disambiguatingDescription": BIO_AR,
        "url": url(), "image": url(c["PHOTO"]), "sameAs": [c["LINKEDIN"]],
        "worksFor": {"@type": "Organization", "name": "Meela Investment Company", "address": {"@type": "PostalAddress", "addressLocality": "Riyadh", "addressCountry": "SA"}},
        "workLocation": {"@type": "Place", "name": "Riyadh, Saudi Arabia"},
        "address": {"@type": "PostalAddress", "addressLocality": "Riyadh", "addressCountry": "SA"},
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Applied Science University", "alternateName": "جامعة العلوم التطبيقية"},
                     {"@type": "CollegeOrUniversity", "name": "Al al-Bayt University", "alternateName": "جامعة آل البيت"}],
        "knowsLanguage": [{"@type": "Language", "name": "Arabic", "alternateName": "ar"},
                          {"@type": "Language", "name": "English", "alternateName": "en"}],
        "knowsAbout": KNOWS,
        "hasOccupation": {"@type": "Occupation", "name": "Technology leader (CTO / IT Director track), ERP and IT governance",
                          "alternateName": ROLES_EN + ROLES_AR,
                          "occupationLocation": [{"@type": "Country", "name": n} for n in ["Saudi Arabia", "United Arab Emirates", "Jordan"]],
                          "skills": "Digital Transformation, IT Strategy, ERP, Odoo, IT Governance, Enterprise Architecture, COBIT, ITIL, ISO 27001, Cloud, Cybersecurity, Data Governance, AI Governance"},
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "name": "Master's degree, Computer Science", "credentialCategory": "degree",
             "recognizedBy": {"@type": "CollegeOrUniversity", "name": "Applied Science University"}},
            {"@type": "EducationalOccupationalCredential", "name": "Bachelor's degree, Computer Science", "credentialCategory": "degree",
             "recognizedBy": {"@type": "CollegeOrUniversity", "name": "Al al-Bayt University"}},
        ] + [{"@type": "EducationalOccupationalCredential", "name": f"{code} {e}", "credentialCategory": "certification",
              "recognizedBy": {"@type": "Organization", "name": org}} for code, a, e, org in CERTS],
    }
    if c["EMAIL"]:
        p["email"] = "mailto:" + c["EMAIL"]
    if c["PHONE"]:
        p["telephone"] = c["PHONE"]
    return p


def graph(slug, kind, name_en, desc, faq=False):
    g = [person(),
         {"@type": "WebSite", "@id": url() + "#site", "name": NAME_EN, "alternateName": NAME_AR, "url": url(),
          "inLanguage": ["ar", "en"], "about": {"@id": url() + "#othman"}, "author": {"@id": url() + "#othman"},
          "creator": {"@type": "Person", "name": "Nour Aldeen Tofi", "alternateName": "نور الدين طفي", "url": CONFIG["MAKER"]}},
         {"@type": kind, "@id": url(slug + ".html") + "#page", "name": name_en, "description": desc, "url": url(slug + ".html"),
          "inLanguage": ["ar", "en"], "isPartOf": {"@id": url() + "#site"}, "about": {"@id": url() + "#othman"},
          "mainEntity" if kind == "ProfilePage" else "mentions": {"@id": url() + "#othman"},
          "primaryImageOfPage": {"@type": "ImageObject", "url": url(OG_IMG), "width": 1200, "height": 630}}]
    nm = next((n for n in NAV if n[0] == slug), None)
    if nm and slug != "index":
        g.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": url()},
            {"@type": "ListItem", "position": 2, "name": nm[2], "item": url(slug + ".html")}]})
    if faq:
        g.append({"@type": "FAQPage", "@id": url("contact.html") + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for qa, qe, aa, ae in FAQ for q, a in ((qa, aa), (qe, ae))]})
    return {"@context": "https://schema.org", "@graph": g}


# ----------------------------------------------------------------------------------
# The page template
# ----------------------------------------------------------------------------------
HEAD_JS = ('(function(){var d=document.documentElement,l="ar",th="light";'
           'try{l=localStorage.getItem("oa-lang")||"ar";th=localStorage.getItem("oa-theme")||"light"}catch(e){}'
           'var q=/[?&]lang=(ar|en)/.exec(location.search);if(q)l=q[1];if(location.hash==="#en")l="en";'
           'd.lang=l;d.dir=l==="ar"?"rtl":"ltr";d.setAttribute("data-theme",th);'
           'var t=d.getAttribute("data-title-"+l);if(t)document.title=t;'
           'try{if(!matchMedia("(prefers-reduced-motion: reduce)").matches&&"IntersectionObserver" in window){d.classList.add("motion");'
           'setTimeout(function(){if(!d.classList.contains("js-ok"))d.classList.remove("motion")},2600)}}catch(e){}})()')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='15' fill='%2313213E'/%3E"
           "%3Cg transform='translate(5 5) scale(1.35)' fill='none' stroke-linecap='round' stroke-linejoin='round' stroke-width='3.3'%3E"
           "%3Cpath d='M37 10C30 6 25 15 28 19S35 16 30 13 22 14 18 14H3' stroke='%23C99B79'/%3E"
           "%3Cpath d='M37 20C32 25 27 13 22 18S19 20 17 20H3' stroke='%23FFFFFF'/%3E"
           "%3Cpath d='M37 30C30 34 27 22 23 24S21 26 18 26H3' stroke='%238FAEF2'/%3E%3C/g%3E%3C/svg%3E")


def page(slug, title_ar, title_en, desc, body, kind="WebPage", faq=False, bodycls="", noindex=False):
    full_ar = f"{title_ar} | عثمان المشاقبة" if slug != "index" else title_ar
    full_en = f"{title_en} | Othman Almashaqba" if slug != "index" else title_en
    ld = json.dumps(graph(slug, kind, full_en, desc, faq), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    robots = "noindex, nofollow" if (CONFIG["PROTOTYPE"] or noindex) else "index, follow, max-image-preview:large"
    canon = url(slug + ".html")
    og_alt = "Othman Almashaqba (عثمان المشاقبة), technology leader in Riyadh: ERP, Odoo, IT governance"
    site = json.dumps({k: CONFIG[k] for k in ("EMAIL", "PHONE", "WHATSAPP", "LINKEDIN")}, separators=(",", ":"))
    base_tag = f'<base href="{BASE}/">\n' if slug == "404" else ""  # the 404 page is served at any depth
    return f'''<!doctype html>
<html lang="ar" dir="rtl" data-theme="light" data-title-ar="{esc(full_ar)}" data-title-en="{esc(full_en)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_ar)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(", ".join(KEYWORDS))}">
<meta name="author" content="Othman Almashaqba (عثمان المشاقبة)">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="ar" href="{canon}">
<link rel="alternate" hreflang="en" href="{canon}?lang=en">
<link rel="alternate" hreflang="x-default" href="{canon}">
<meta property="og:title" content="{esc(full_en)} · {esc(full_ar)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="profile">
<meta property="profile:first_name" content="Othman"><meta property="profile:last_name" content="Almashaqba">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{url(OG_IMG)}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta property="og:locale" content="ar_SA"><meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{url(OG_IMG)}">
<meta name="theme-color" content="#F3F5F8" id="themeColor">
<link rel="me" href="{CONFIG['LINKEDIN']}">
<link rel="alternate" type="text/plain" href="llms.txt" title="Othman Almashaqba: summary for AI assistants">
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="assets/img/icon-180.png">
<link rel="preload" href="assets/fonts/plex-ar-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/kufi-ar.woff2" as="font" type="font/woff2" crossorigin>
{base_tag}<link rel="stylesheet" href="assets/style.css?v={VER}">
<script>{HEAD_JS}</script>
<script type="application/ld+json">{ld}</script>
</head>
<body data-page="{slug}" class="{bodycls}">
{header(slug)}
{sheet(slug)}
<main id="main">
{body}
</main>
{footer(slug)}
{dock(slug)}
<script id="siteConfig" type="application/json">{site}</script>
<script src="assets/threads.js?v={VER}" defer></script>
<script src="assets/site.js?v={VER}" defer></script>
</body>
</html>
'''


def phead(h_ar, h_en, lede_ar, lede_en):
    return f'''<section class="phead">
  <canvas class="threads" data-threads="band" aria-hidden="true"></canvas>
  <div class="wrap phead-in">
    <h1 class="h1 page-title">{t(h_ar, h_en)}</h1>
    <p class="lede">{t(lede_ar, lede_en)}</p>
  </div>
</section>'''


# ----------------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------------
def home():
    ledger = [("منذ", "Since", L("2014"), "2014"),
              ("بين", "Across", "الأردن والإمارات والسعودية", "Jordan, the UAE and Saudi Arabia"),
              ("قدت", "Led", f"أكثر من 10 تحولات {L('ERP')}", "10+ ERP transformations"),
              ("مع " + L("Odoo"), "With Odoo", "من الإصدار 8 إلى 19", "from version 8 to 19")]
    dl = "".join(f'<div class="lg-row rv" style="--k:{i}"><dt>{t(a, e)}</dt><dd>{t(va, ve)}</dd></div>' for i, (a, e, va, ve) in enumerate(ledger))
    return f'''
<section class="hero" id="hero">
  <canvas class="threads" data-threads="hero" aria-hidden="true"></canvas>
  <div class="wrap hero-grid">
    <div class="hero-copy" id="heroCopy">
      <h1 class="hero-name page-title rise" style="--k:0">{t("عثمان المشاقبة", "Othman Almashaqba")}</h1>
      <p class="hero-statement rise" style="--k:1">{t("أبدأ من الناس، وأنتهي بأثر يُقاس.", "I start with people, and end with impact you can measure.")}</p>
      <p class="lede rise" style="--k:2">{t(f"قائد تقنية في الرياض. منذ 2014 أعمل بين الأردن والإمارات والسعودية على استراتيجية التقنية وتحولات {L('ERP')} وحوكمة تقنية المعلومات، والهدف واحد: أن يصير الاستثمار في التقنية قيمة يلمسها العمل.", "A technology leader in Riyadh. Since 2014 I have worked across Jordan, the UAE and Saudi Arabia on technology strategy, ERP transformation and IT governance, with one aim: technology investment that the business can feel.")}</p>
      <div class="cta-row rise" style="--k:3">
        <a class="btn btn-ink shine" href="story.html">{icon("story")}{t("اقرأ قصتي", "Read my story")}</a>
        <a class="btn btn-line" href="contact.html">{icon("chat")}{t("لنتحدث", "Let’s talk")}</a>
      </div>
    </div>
    <div class="hero-strip" aria-hidden="true"></div>
    <figure class="hero-portrait rise-img" id="heroGate">
      <div class="portrait-frame">{portrait()}</div>
      <figcaption class="now glass"><span class="now-dot" aria-hidden="true"></span><span class="now-txt">{t("اليوم في الرياض", "Today, in Riyadh")}<b>{t(f"أقود استراتيجية {L('ERP')} في شركة استثمار", "Leading ERP strategy at an investment company")}</b></span></figcaption>
    </figure>
  </div>
</section>

<section class="intro" aria-labelledby="introQ">
  <div class="wrap intro-grid">
    <div class="intro-main">
      <p class="pull rv-h" id="introQ">{t("التقنية تصبح أكثر قيمة حين يفهمها العمل، ويستفيد منها الناس.", "Technology creates more value when the business understands it and people benefit from it.")}</p>
      <p class="body-l rv">{t(f"أساعد المؤسسات على تحويل استثمارها في التقنية إلى قيمة أعمال يمكن قياسها. أبني فرقًا تجمع {L('ERP')} والبنية التحتية والتكاملات والبيانات والعمليات الرقمية، وأعمل مع الإدارة التنفيذية لتتوافق خطط التقنية وميزانياتها ومخاطرها مع أولويات العمل.", "I help organisations turn technology investment into business value they can measure. I build teams that bring together ERP, infrastructure, integrations, data and digital operations, and I work with executives so that technology roadmaps, budgets and risk line up with business priorities.")}</p>
    </div>
    <dl class="ledger">{dl}</dl>
  </div>
</section>

<section class="sec" aria-labelledby="hMeasure">
  <div class="wrap">
    {sec_head("لا أعدّ الأنظمة التي أطلقناها. أقيس ما تغيّر بعدها.", "I don’t count the systems we launched. I measure what changed after them.", "أرقام من البرامج التي قدتها، قبل التقنية وبعدها.", "Figures from the programmes I led, before and after.", "hMeasure")}
    {measure("h")}
  </div>
</section>

<section class="sec sec-tint" aria-labelledby="hVoices">
  <div class="wrap voices-wrap">
    {sec_head("كيف أفكّر", "How I think", "خمس أفكار أعود إليها في كل مشروع.", "Five ideas I come back to on every project.", "hVoices", ("approach.html", "المنهج كاملًا", "The full approach"))}
    {voices()}
  </div>
</section>

<section class="sec" aria-labelledby="hJourney">
  <div class="wrap">
    {sec_head("اثنا عشر عامًا بين ثلاث دول", "Twelve years across three countries", f"من الدعم التقني وتحليل البيانات، إلى كتابة أنظمة {L('Odoo')}، ثم إدارة تقنية المعلومات وقيادة استراتيجيتها.", "From technical support and data analysis, to building Odoo systems, to running IT and leading its strategy.", "hJourney", ("story.html", "القصة كاملة", "The full story"))}
    {journey()}
  </div>
</section>

<section class="sec sec-tint" aria-labelledby="hOdoo">
  <div class="wrap">
    {sec_head("من Odoo 8 إلى 19", "Odoo, from 8 to 19", f"أكثر من عشرة برامج تحول {L('ERP')} في الأردن والإمارات والسعودية، من التجارة الإلكترونية إلى الأصول والاستثمار.", "More than ten ERP programmes in Jordan, the UAE and Saudi Arabia, from e-commerce to assets and investment.", "hOdoo", ("work.html", "كل الأعمال", "All the work"))}
    {ruler()}
  </div>
</section>

<section class="sec" aria-labelledby="hKnow">
  <div class="wrap">
    {sec_head("علوم الحاسوب في الأساس", "Computer science at the core", "بكالوريوس وماجستير في علوم الحاسوب، وثلاث أوراق بحثية قُدّمت للنشر في الأمن والصحة والعقار.", "A bachelor’s and a master’s in computer science, and three research papers submitted for publication in security, health and real estate.", "hKnow", ("knowledge.html", "المعرفة", "Knowledge"))}
    {research_cards(compact=True)}
  </div>
</section>

{cta_band()}
'''


def story():
    chs = []
    for i, c in enumerate(CHAPTERS):
        q = ""
        if c.get("q_ar"):
            q = f'<blockquote class="ch-q">{t(c["q_ar"], c["q_en"], tag="p")}</blockquote>'
        y_en = c.get("y_en", c["y"])
        if "اليوم" in c["y"]:
            years_ar = f'<span dir="ltr">{c["y"].split("–")[0]}</span>–اليوم'
        else:
            years_ar = f'<span dir="ltr">{c["y"]}</span>'
        years = t(years_ar, f'<span dir="ltr">{y_en}</span>')
        chs.append(f'''<li class="ch rv" style="--k:{i}">
  <span class="ch-knot" aria-hidden="true"></span>
  <p class="ch-years">{years}</p>
  <div class="ch-body">
    <h2 class="h3 ch-org">{t(c["org_ar"], c["org_en"])}</h2>
    <p class="ch-meta">{t(c["role_ar"], c["role_en"])}<span class="ch-place">{icon("pin", "ic ic-s")}{t(c["place_ar"], c["place_en"])}</span></p>
    <p class="ch-txt">{t(c["ar"], c["en"])}</p>
    {q}
  </div>
</li>''')
    body = phead("خيط واحد عبر اثني عشر عامًا", "One thread through twelve years",
                 f"مسيرتي تتدرّج من البيانات والأنظمة، إلى تطوير {L('ERP')}، ثم إدارة التقنية وقيادة استراتيجيتها. هذا التدرّج هو ما يجعلني أرى الصورة الكاملة وأفهم تفاصيلها في الوقت نفسه.",
                 "My career runs from data and systems, to ERP development, to running technology and leading its strategy. That progression is what lets me see the whole picture and still understand its details.")
    body += f'''
<section class="sec chapters-sec">
  <div class="wrap">
    <ol class="chapters" id="chapters"><span class="thread-line" aria-hidden="true"><i></i></span>{"".join(chs)}</ol>
  </div>
</section>

<section class="sec sec-tint" aria-labelledby="hNow">
  <div class="wrap now-next">
    <h2 class="h2 rv-h" id="hNow">{t("ما يشغلني اليوم", "What occupies me now")}</h2>
    <p class="pull pull-s rv">{t("كيف تُدخل المؤسسة الذكاء الاصطناعي في قراراتها دون أن تفقد وضوح المسؤولية: من يقرر، ومن يراجع، ومن يتحمل النتيجة.", "How an organisation can bring AI into its decisions without losing clarity about responsibility: who decides, who reviews, and who answers for the outcome.")}</p>
    <a class="more rv" href="knowledge.html">{t("ما أتابعه وأبحث فيه", "What I read and research")}<span class="more-ic" aria-hidden="true">{icon("next")}</span></a>
  </div>
</section>
{cta_band()}'''
    return body


def approach():
    steps = "".join(f'''<li class="step rv" style="--k:{i}">
  <span class="step-n" dir="ltr">{i + 1}</span>
  <h3 class="h3">{t(a, e)}</h3>
  <p>{t(da, de)}</p>
</li>''' for i, (a, e, da, de) in enumerate(STEPS))
    beliefs = "".join(f'<li class="belief rv"><h3 class="h3">{t(a, e)}</h3><p>{t(da, de)}</p></li>' for a, e, da, de in BELIEFS)
    fw = "".join(f'<li class="fw rv"><b dir="ltr">{n}</b><span>{t(a, e)}</span></li>' for n, a, e in FRAMEWORKS)
    body = phead("أرتّب العمل قبل أن أؤتمته.", "I fix the work before I automate it.",
                 "التقنية بطبيعتها مُكبّر: إن كانت العمليات واضحة ضاعفت الإنتاجية، وإن كانت مرتبكة ضاعفت الفوضى. لذلك تبدأ كل مبادرة عندي من العمل نفسه، لا من الأداة.",
                 "Technology is a magnifier by nature: when processes are clear it multiplies productivity, and when they are confused it multiplies the chaos. So every initiative I run starts with the work itself, not the tool.")
    body += f'''
<section class="sec" aria-labelledby="hLens">
  <div class="wrap lens-grid">
    <div class="lens-copy">
      <h2 class="h2 rv-h" id="hLens">{t("التقنية تكبّر ما تجده أمامها.", "Technology enlarges whatever it finds.")}</h2>
      <p class="body-l rv">{t("مرّر العدسة نفسها على عمليتين: في الأولى تصير الخطوات الواضحة إنتاجية أعلى، وفي الثانية تصير الخطوات المرتبكة أخطاء أسرع. لهذا أسأل عن العملية قبل أن أسأل عن النظام.", "Pass the same lens over two processes: on the first, clear steps become more productivity; on the second, confused steps become faster mistakes. That is why I ask about the process before I ask about the system.")}</p>
    </div>
    <figure class="lens-demo glass rv" id="lensDemo" aria-hidden="true">
      <svg viewBox="0 0 520 300">
        <defs><clipPath id="lensClip"><circle id="lensHole" cx="150" cy="150" r="74"/></clipPath></defs>
        <g class="lens-rows" id="lensRows"></g>
        <g clip-path="url(#lensClip)"><rect class="lens-bg" x="0" y="0" width="520" height="300"/><g class="lens-zoom" id="lensZoom"></g></g>
        <g class="lens-glass" id="lensGlass"><circle cx="150" cy="150" r="74"/><path d="M202 202 236 236"/></g>
      </svg>
      <figcaption class="lens-cap">{t("عملية واضحة", "A clear process", cls="lc-a")}{t("عملية مرتبكة", "A confused process", cls="lc-b")}</figcaption>
    </figure>
  </div>
</section>

<section class="sec sec-tint" aria-labelledby="hSplit">
  <div class="wrap">
    {sec_head(f"النجاح {L('80%')} منه إدارة تغيير وهندسة عمليات", "80% of success is change management and process design", "التحدي في التحول الرقمي لم يكن يومًا في كتابة الكود؛ التحدي الحقيقي هو إدارة التغيير، ومساعدة الفرق على الخروج من منطقة الراحة.", "The challenge in digital transformation was never writing the code. The real challenge is managing change and helping teams leave their comfort zone.", "hSplit")}
    <div class="split rv" role="img" {al("ثمانون بالمئة إدارة تغيير وهندسة عمليات، وعشرون بالمئة برمجة وتقنية", "Eighty per cent change management and process re-engineering, twenty per cent code and technology")}>
      <div class="split-a" style="--w:.8"><b dir="ltr">80%</b>{t("إدارة التغيير وهندسة العمليات", "Change management & process re-engineering")}</div>
      <div class="split-b" style="--w:.2"><b dir="ltr">20%</b>{t("البرمجة والتقنية", "Code & technology")}</div>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="hSteps">
  <div class="wrap">
    {sec_head("أربع خطوات، بالترتيب", "Four steps, in order", "مع كل خطوة يصير الخيط أوضح: من فهم ما هو قائم، إلى قراءة ما تغيّر.", "With every step the thread gets clearer: from understanding what exists to reading what changed.", "hSteps")}
    <div class="steps-wrap">
      <svg class="steps-thread" viewBox="0 0 1000 120" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M0 60 C40 10 70 110 110 55 S170 20 200 70 S260 95 290 50 S350 40 380 64 S450 70 500 58 S580 56 620 61 S700 60 760 60 S880 60 1000 60"/></svg>
      <ol class="steps" role="list">{steps}</ol>
    </div>
  </div>
</section>

<section class="sec sec-tint" aria-labelledby="hBeliefs">
  <div class="wrap">
    {sec_head("ما أتمسك به", "What I hold to", None, None, "hBeliefs")}
    <ul class="beliefs" role="list">{beliefs}</ul>
  </div>
</section>

<section class="sec" aria-labelledby="hFw">
  <div class="wrap">
    {sec_head("أطر عمل، لا اجتهادات", "Frameworks, not guesswork", f"أبني حوكمة التقنية على {L('COBIT')} و{L('ITIL')}، بضوابط متوافقة مع {L('ISO 27001')}.", "I build technology governance on COBIT and ITIL, with ISO 27001-aligned controls.", "hFw")}
    <ul class="fws" role="list">{fw}</ul>
  </div>
</section>
{cta_band()}'''
    return body


def work():
    body = phead("أكثر من عشر تحولات ERP، وأرقام يمكن قياسها.", "More than ten ERP transformations, and numbers you can measure.",
                 f"عملت مع {L('Odoo')} من الإصدار 8 إلى 19، على المالية والموارد البشرية والمخزون والمبيعات والتجارة الإلكترونية والأصول، في الأردن والإمارات والسعودية.",
                 "I have worked with Odoo from version 8 to 19, across finance, HR, inventory, sales, e-commerce and assets, in Jordan, the UAE and Saudi Arabia.")
    body += f'''
<section class="sec" aria-labelledby="hRuler">
  <div class="wrap">
    {sec_head("رحلة متصلة مع Odoo", "One continuous journey with Odoo", "كل برنامج في مكانه على مقياس الإصدارات. اختر واحدًا لتقرأ عنه.", "Each programme in its place on the version scale. Pick one to read about it.", "hRuler")}
    {ruler(full=True)}
  </div>
</section>

<section class="sec sec-tint" aria-labelledby="hProgs">
  <div class="wrap">
    {sec_head("برامج مختارة", "Selected programmes", "أنظمة مؤسسية وتجارة وأصول وضيافة وذكاء اصطناعي.", "Enterprise systems, commerce, assets, hospitality and AI.", "hProgs")}
    {programme_cards()}
  </div>
</section>

<section class="sec" aria-labelledby="hMods">
  <div class="wrap mods-grid">
    <div class="mods-copy">
      <h2 class="h2 rv-h" id="hMods">{t("نظام واحد لمؤسسة سعودية كاملة", "One system for a whole Saudi organisation")}</h2>
      <p class="body-l rv">{t(f"حلّلت متطلبات حل {L('Odoo')} متكامل يغطي اثنتي عشرة وظيفة، مع إجراءات المحاسبة والموارد البشرية الخاصة بالسعودية ومتطلبات الربط مع هيئة الزكاة والضريبة والجمارك.", "I analysed the requirements for an integrated Odoo solution covering twelve functions, with Saudi-specific accounting and HR workflows and the integration requirements of the Zakat, Tax and Customs Authority.")}</p>
    </div>
    {module_map()}
  </div>
</section>

<section class="sec sec-tint" aria-labelledby="hRes">
  <div class="wrap">
    {sec_head("النتائج، قبل وبعد", "Results, before and after", "كل رقم مرتبط بمكانه، وكل مكان بدأ بهدف واضح.", "Each figure tied to where it happened, and each place began with a clear goal.", "hRes")}
    {measure("w")}
  </div>
</section>

<section class="sec" aria-labelledby="hAreas">
  <div class="wrap">
    {sec_head("ستة مجالات تعمل معًا", "Six fields working together", f"أتعامل مع {L('ERP')} والبيانات والبنية التحتية والأمن كأجزاء من منظومة واحدة تخدم المؤسسة كلها.", "I treat ERP, data, infrastructure and security as parts of one system that serves the whole organisation.", "hAreas")}
    {area_cards()}
  </div>
</section>
{cta_band()}'''
    return body


def knowledge():
    edu = "".join(f'<li class="edu rv"><span class="edu-y" dir="ltr">{y}</span><h3 class="h3">{t(a, e)}</h3><p>{t(ua, ue)}</p></li>' for y, a, e, ua, ue in EDUCATION)
    body = phead("المعرفة التي يقوم عليها القرار", "The knowledge behind the decisions",
                 "علوم الحاسوب في الأساس، وشهادات في إدارة المشاريع والمعمارية والسحابة والأمن، وأبحاث تختبر أفكارًا في الأمن والذكاء الاصطناعي والحوكمة.",
                 "Computer science at the core, certifications in project management, architecture, cloud and security, and research that tests ideas in security, AI and governance.")
    body += f'''
<section class="sec" aria-labelledby="hEdu">
  <div class="wrap">
    {sec_head("الدراسة", "Education", None, None, "hEdu")}
    <ul class="edus" role="list">{edu}</ul>
  </div>
</section>

<section class="sec sec-tint" aria-labelledby="hRs">
  <div class="wrap">
    {sec_head("أبحاث قُدّمت للنشر", "Research submitted for publication", "ثلاث مخطوطات قُدّمت إلى مجلات علمية، ولم تصدر بعد بنسختها النهائية.", "Three manuscripts submitted to academic journals, not yet published in final form.", "hRs")}
    {research_cards()}
  </div>
</section>

<section class="sec" aria-labelledby="hCerts">
  <div class="wrap">
    {sec_head("شهادات مهنية", "Professional certifications", None, None, "hCerts")}
    {cert_tiles()}
    <div class="langs rv">
      <h3 class="h3">{t("اللغات", "Languages")}</h3>
      <p>{t("العربية، اللغة الأم", "Arabic, native")}</p>
      <p>{t("الإنجليزية، بطلاقة", "English, fluent")}</p>
    </div>
  </div>
</section>

<section class="sec sec-tint" aria-labelledby="hFollow">
  <div class="wrap now-next">
    <h2 class="h2 rv-h" id="hFollow">{t("ما أتابعه الآن", "What I’m following now")}</h2>
    <p class="pull pull-s rv">{t("حوكمة الذكاء الاصطناعي ووكلائه داخل المؤسسات، وإعادة تصميم العمل نفسه حول ما يستطيعه الذكاء الاصطناعي: لو صممنا هذه الوظيفة من الصفر اليوم، هل سنصممها بالشكل نفسه؟", "The governance of AI and AI agents inside organisations, and redesigning the work itself around what AI can do: if we designed this job from scratch today, would we design it the same way?")}</p>
  </div>
</section>
{cta_band()}'''
    return body


def contact():
    chips = "".join(
        f'<button class="chip{" is-on" if i == 0 else ""}" type="button" role="radio" aria-checked="{"true" if i == 0 else "false"}" data-topic="{k}" '
        f'data-sub-ar="{esc(sa)}" data-sub-en="{esc(se)}">{t(a, e)}</button>'
        for i, (k, a, e, sa, se) in enumerate(TOPICS))
    faqs = "".join(f'''<details class="faq rv">
  <summary><span class="faq-q">{t(qa, qe)}</span><span class="faq-ic" aria-hidden="true"></span></summary>
  <div class="faq-a"><p>{t(aa, ae)}</p></div>
</details>''' for qa, qe, aa, ae in FAQ)
    s0 = TOPICS[0]
    subs = "".join(f'<span data-sub="{k}"{" class=\"is-on\"" if i == 0 else ""}>{t(sa, se)}</span>' for i, (k, a, e, sa, se) in enumerate(TOPICS))
    body = phead("لنتحدث.", "Let’s talk.",
                 f"يسعدني الحوار حول قيادة التقنية، والتحول المؤسسي، و{L('ERP')}، والذكاء الاصطناعي المسؤول.",
                 "I’m glad to talk about technology leadership, enterprise transformation, ERP and responsible AI.")
    body += f'''
<section class="sec" aria-labelledby="hCompose">
  <div class="wrap compose-grid">
    <div class="compose rv">
      <h2 class="h2" id="hCompose">{t("اختر موضوعًا، وأبدأ الرسالة عنك", "Pick a topic and I’ll start the email for you")}</h2>
      <div class="chips" role="radiogroup" {al("موضوع الرسالة", "Topic")}>{chips}</div>
      <div class="letter glass" aria-live="polite">
        <p class="letter-k">{t("إلى", "To")} <b dir="ltr">{CONFIG["EMAIL"]}</b></p>
        <p class="letter-k">{t("الموضوع", "Subject")} <b class="letter-sub" id="letterSub">{subs}</b></p>
        <p class="letter-hi">{t("مرحبًا عثمان،", "Hello Othman,")}</p>
        <p class="letter-note">{t("يفتح بريدك والموضوع والتحية جاهزان، وتكمل أنت الباقي.", "Your mail app opens with the subject and greeting ready; you write the rest.")}</p>
      </div>
      <div class="cta-row">
        <a class="btn btn-ink shine" id="composeGo" href="mailto:{CONFIG["EMAIL"]}?subject={quote(s0[3])}">{icon("mail")}{t("اكتب الرسالة", "Write the email")}</a>
        <button class="btn btn-line" id="copyMail" type="button" data-copy="{CONFIG["EMAIL"]}">{icon("copy", "ic i-copy")}{icon("check", "ic i-check")}{t("انسخ البريد", "Copy email", cls="copy-l")}{t("تم النسخ", "Copied", cls="copied-l")}</button>
      </div>
    </div>
    <div class="reach">
      <h2 class="h2 rv-h">{t("أو مباشرة", "Or directly")}</h2>
      {contact_cards("cards-contact cards-stack")}
      <p class="city rv">{icon("pin", "ic ic-s")}{t("الرياض، المملكة العربية السعودية", "Riyadh, Saudi Arabia")}</p>
    </div>
  </div>
</section>

<section class="sec sec-tint" aria-labelledby="hFaq">
  <div class="wrap faq-wrap">
    {sec_head("أسئلة قبل التواصل", "Before you write", None, None, "hFaq")}
    <div class="faqs">{faqs}</div>
  </div>
</section>'''
    return body


def notfound():
    return f'''<section class="phead phead-404">
  <canvas class="threads" data-threads="band" aria-hidden="true"></canvas>
  <div class="wrap phead-in">
    <h1 class="h1 page-title">{t("هذه الصفحة غير موجودة.", "This page doesn’t exist.")}</h1>
    <p class="lede">{t("ربما تغيّر الرابط. هذه الصفحات موجودة:", "The link may have changed. These pages are here:")}</p>
    <div class="cta-row">{"".join(f'<a class="btn btn-line" href="{s}.html">{icon(ic)}{t(a, e)}</a>' for s, a, e, ic in NAV)}</div>
  </div>
</section>'''


# ----------------------------------------------------------------------------------
# Machine-readable layer
# ----------------------------------------------------------------------------------
FACTS_EN = [
    "Name: Othman Almashaqba (Arabic: عثمان المشاقبة). Also written Othman Al-Mashaqba, Othman Almashaqbeh.",
    "Headline: Technology Leader | CTO / IT Director | Digital Transformation, ERP & IT Governance | Secure, Scalable Operations.",
    "Based in Riyadh, Saudi Arabia. Has worked since 2014 across Jordan, the UAE and Saudi Arabia.",
    "Now (since July 2025): ERP strategy (Enterprise Resources Planning Project Manager) at Meela Investment Company, Riyadh: leads enterprise ERP strategy, aligns ERP architecture with investment operations and executive decision-making, oversees scalability, integrations and data governance, advises management on technology investment and risk.",
    "2022 – June 2025: led technology at Alomran Group (Saudi Arabia; on LinkedIn: Information Technology Manager): enterprise technology strategy, ERP transformation on Odoo across several functions, infrastructure performance +20% through cloud migration and automation, IT governance on COBIT and ITIL, technology costs −15%.",
    "2021 – 2023: IT Manager in Jordan at Marshall School (2021), Smart Rock (2021–2023) and CellBay Jordan (2021–2023), including an ERP transformation on Odoo 13 at CellBay.",
    "2020 – 2021: IT Manager, ERP (Odoo) & technical support at No Errors IT Services, Dubai: IT team, policies, security controls and budgets; enterprise data migrations at 99.9% accuracy.",
    "2018 – 2020: Odoo developer (Python) at Shahwan, Jordan: Odoo modules from version 8 to 13; HR, payroll, timesheet and support modules.",
    "2014 – 2018: technical support and data analyst for UNICEF projects in Jordan.",
    "Led more than ten enterprise ERP transformation programmes, including Odoo from version 8 to 19 (Shahwan Group, Romex Dubai, CellBay Jordan, Alomran Group, TOTO Saudi Arabia, Meela Investment), a digital transformation for Mina Hotel in Abha, and an AI-based IT governance and quality platform.",
    "Analysed requirements for an integrated Odoo solution across finance, HR and payroll, CRM, sales, purchasing, inventory, POS, e-commerce, manufacturing, projects, marketing and fleet, with Saudi accounting and HR workflows and ZATCA integration requirements.",
    "Results he reports: technology operating costs −15%; infrastructure performance +20%; system downtime −30%; data migration accuracy 99.9%.",
    "Governance: COBIT and ITIL, with ISO 27001-aligned controls.",
    "Education: Master's degree in Computer Science, Applied Science University (2020–2022); Bachelor's degree in Computer Science, Al al-Bayt University (2010–2014).",
    "Certifications (as listed on his own site): PMP (PMI), AWS Solutions Architect – Professional, Microsoft Azure Solutions Architect Expert, CISM (ISACA), TOGAF (The Open Group).",
    "Research: three manuscripts submitted to journals (not yet published): SSExam, security of the digital exam lifecycle (Information Security Journal: A Global Perspective); digital twins for chronic-disease prevention in Saudi Arabia (International Journal of Healthcare Management); explainable GeoAI for Saudi residential property valuation (Applied Geomatics).",
    "Languages: Arabic (native), English (fluent).",
    "Convictions: every technology project starts with the people who will use it; don't put a new system on top of old bureaucracy; change processes to fit best practice before customising the system; the foundation comes before the tool; security is culture and governance; measure what changed after the investment; before scaling AI, define who decides, who reviews and who is accountable.",
    f"Contact: {CONFIG['EMAIL']}; phone {CONFIG['PHONE_SHOW']}; LinkedIn {CONFIG['LINKEDIN']}.",
]

PAGES = [("index", "الرئيسية", "Home", "Who he is, how he thinks, the journey, Odoo 8–19, research and contact", "ProfilePage"),
         ("story", "القصة", "Story", "His career from 2010 to today as one story: UNICEF, Shahwan, Dubai, Jordan, Alomran, Meela", "AboutPage"),
         ("approach", "المنهج", "Approach", "How he works: process before automation, four steps, convictions, COBIT/ITIL/ISO 27001", "WebPage"),
         ("work", "الأعمال", "Work", "ERP programmes on Odoo 8–19, a Saudi integrated Odoo scope, results before and after, six fields", "CollectionPage"),
         ("knowledge", "المعرفة", "Knowledge", "Education, research manuscripts, certifications, languages, current interests", "WebPage"),
         ("contact", "تواصل", "Contact", "Email, phone, LinkedIn, and answers to common questions", "ContactPage")]


def llms_txt():
    lines = [f"# {NAME_EN} ({NAME_AR})", "", f"> {BIO_EN}", "", "## Facts", ""]
    lines += [f"- {f}" for f in FACTS_EN[:9]]
    lines += ["", "## Pages", ""]
    lines += [f"- [{e}]({url(s + '.html')}): {d}" for s, a, e, d, k in PAGES]
    lines += ["", "## More", "", f"- [Full profile for AI assistants]({url('llms-full.txt')})", f"- [LinkedIn]({CONFIG['LINKEDIN']})", ""]
    return "\n".join(lines)


def llms_full():
    lines = [f"# {NAME_EN} ({NAME_AR}): full profile", "", BIO_EN, "", BIO_AR, "", "## Facts", ""]
    lines += [f"- {f}" for f in FACTS_EN]
    lines += ["", "## Career, as told on the site", ""]
    for c in CHAPTERS:
        lines.append(f"- {c.get('y_en', c['y'])}, {c['place_en']}: {strip_tags(c['org_en'])}, {c['role_en']}. {c['en']}")
    lines += ["", "## Programmes", ""]
    for p in PROGRAMMES:
        tag = p.get("tag", p.get("tag_en", ""))
        lines.append(f"- {strip_tags(p['org_en'])} ({p['place_en']}, {tag}): {p['en']}")
    lines += ["", "## How he works", ""]
    for i, (a, e, da, de) in enumerate(STEPS):
        lines.append(f"{i + 1}. {e}: {de}")
    for a, e, da, de in BELIEFS:
        lines.append(f"- {e}: {de}")
    lines += ["", "## Questions", ""]
    for qa, qe, aa, ae in FAQ:
        lines += [f"### {qe}", strip_tags(ae), ""]
    lines += [f"Site designed and built by Nour Aldeen Tofi ({CONFIG['MAKER']}).", ""]
    return "\n".join(lines)


def robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Googlebot", "Bingbot", "Applebot", "Applebot-Extended",
            "DuckDuckBot", "YandexBot", "CCBot", "Meta-ExternalAgent"]
    out = [f"User-agent: {b}\nAllow: /\n" for b in bots]
    out.append("User-agent: *\nAllow: /\n")
    out.append(f"Sitemap: {url('sitemap.xml')}\n")
    return "\n".join(out)


def sitemap():
    items = "".join(f"  <url><loc>{url(s + '.html')}</loc><lastmod>2026-10-20</lastmod></url>\n" for s, *_ in PAGES)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n'


# ----------------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------------
def write(name, text):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(text)


def main():
    desc = {
        "index": "عثمان المشاقبة، قائد تقنية في الرياض: استراتيجية التقنية، وتحولات ERP وOdoo من 8 إلى 19، وحوكمة تقنية المعلومات. Othman Almashaqba, technology leader in Riyadh: technology strategy, ERP and Odoo transformation, IT governance.",
        "story": "قصة عثمان المشاقبة من علوم الحاسوب واليونيسف إلى قيادة استراتيجية ERP في الرياض. Othman Almashaqba's career, from computer science and UNICEF to leading ERP strategy in Riyadh.",
        "approach": "كيف يعمل عثمان المشاقبة: العملية قبل الأتمتة، أربع خطوات، وحوكمة على COBIT وITIL. How Othman Almashaqba works: process before automation, four steps, COBIT and ITIL governance.",
        "work": "أكثر من عشر تحولات ERP على Odoo من 8 إلى 19، ونتائج قبل وبعد. More than ten ERP transformations on Odoo 8 to 19, with results before and after.",
        "knowledge": "دراسة عثمان المشاقبة وأبحاثه وشهاداته. Othman Almashaqba's education, research manuscripts and certifications.",
        "contact": "تواصل مع عثمان المشاقبة بالبريد أو الهاتف أو LinkedIn. Contact Othman Almashaqba by email, phone or LinkedIn.",
    }
    titles = {"index": ("عثمان المشاقبة | قيادة التقنية والتحول المؤسسي", "Othman Almashaqba | Technology leadership & enterprise transformation"),
              "story": ("القصة", "Story"), "approach": ("المنهج", "Approach"), "work": ("الأعمال", "Work"),
              "knowledge": ("المعرفة", "Knowledge"), "contact": ("تواصل", "Contact")}
    builders = {"index": home, "story": story, "approach": approach, "work": work, "knowledge": knowledge, "contact": contact}
    kinds = {s: k for s, a, e, d, k in PAGES}
    for s, fn in builders.items():
        ta, te = titles[s]
        write(f"{s}.html", page(s, ta, te, desc[s], fn(), kind=kinds[s], faq=(s == "contact"), bodycls=f"p-{s}"))
    write("404.html", page("404", "الصفحة غير موجودة", "Page not found", desc["index"], notfound(), bodycls="p-404", noindex=True))
    write("llms.txt", llms_txt())
    write("llms-full.txt", llms_full())
    write("robots.txt", robots())
    write("sitemap.xml", sitemap())
    write(".nojekyll", "")
    print("built:", ", ".join(f"{s}.html" for s in builders), "+ 404, llms, robots, sitemap")


if __name__ == "__main__":
    main()
