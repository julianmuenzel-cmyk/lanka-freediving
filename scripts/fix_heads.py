#!/usr/bin/env python3
"""Fix Sleeve page heads after SEO injection."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLEEVE = ROOT / "explore" / "a-record-sleeve"
SITE = "https://lankafreediving.com"

META = {
    "index.html": {
        "title": "Lanka Freediving — Record Sleeve | Freediving Sri Lanka, Unawatuna",
        "description": "Molchanovs freediving Sri Lanka in Unawatuna. Small-group courses, a week-long retreat, and expeditions — framed like a crate of record sleeves.",
        "path": "/",
        "schema": "local",
    },
    "courses/index.html": {
        "title": "Freediving Courses in Sri Lanka | Lanka Freediving | Unawatuna",
        "description": "Molchanovs freediving Sri Lanka in Unawatuna: Discover, Wave 1, Wave 2, and advanced coaching. Small groups of 4.",
        "path": "/courses/",
        "schema": "courses",
    },
    "retreat/index.html": {
        "title": "5-Day Freediving Retreat in Sri Lanka | Lanka Freediving",
        "description": "Freediving Sri Lanka retreat in Unawatuna: five days of breathwork, pool, open water, and Molchanovs certification. From €900.",
        "path": "/retreat/",
        "schema": None,
    },
    "expedition/index.html": {
        "title": "Freediving Expeditions — Salty Tracks & Sri Lanka | Lanka Freediving",
        "description": "Molchanovs freediving Sri Lanka expeditions and a Batanta Island trip with Salty Tracks. Certified divers, small groups, remote water.",
        "path": "/expedition/",
        "schema": None,
    },
    "school/index.html": {
        "title": "The School | Lanka Freediving | Unawatuna Sri Lanka",
        "description": "Lanka Freediving is a Molchanovs school in Unawatuna, Sri Lanka. Small groups, one instructor, November to April.",
        "path": "/school/",
        "schema": "local",
    },
    "faq/index.html": {
        "title": "FAQ | Lanka Freediving | Unawatuna Sri Lanka",
        "description": "Freediving courses in Unawatuna: safety, what to bring, deposits, and how to book with Lanka Freediving.",
        "path": "/faq/",
        "schema": "faq",
    },
    "contact/index.html": {
        "title": "Get in touch | Lanka Freediving | Unawatuna",
        "description": "Message Lanka Freediving about Molchanovs courses, the retreat, or expeditions in Unawatuna. We reply within 24 hours.",
        "path": "/contact/",
        "schema": None,
    },
}

LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": ["SportsActivityLocation", "LocalBusiness"],
    "name": "Lanka Freediving",
    "description": "Molchanovs freediving school in Unawatuna, Sri Lanka. Small-group courses, retreat, and expeditions. Open November through April.",
    "url": SITE,
    "email": "hello@lankafreediving.com",
    "image": f"{SITE}/assets/og-default.jpg",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Unawatuna",
        "addressRegion": "Southern Province",
        "addressCountry": "LK",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 6.0144, "longitude": 80.2489},
    "areaServed": "Unawatuna, Galle, Southern Province, Sri Lanka",
}


def faq_schema():
    text = (SLEEVE / "faq" / "index.html").read_text()
    pairs = re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", text, re.S)
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q.strip(),
                "acceptedAnswer": {"@type": "Answer", "text": a.strip()},
            }
            for q, a in pairs
        ],
    }


def courses_schema():
    return [
        LOCAL_BUSINESS,
        *[
            {
                "@context": "https://schema.org",
                "@type": "Course",
                "name": name,
                "description": desc,
                "provider": {"@type": "Organization", "name": "Lanka Freediving", "url": SITE},
                "offers": {"@type": "Offer", "price": price, "priceCurrency": "EUR"},
            }
            for name, desc, price in [
                ("Discover Freediving", "Half-day introduction to freediving in Unawatuna.", "120"),
                ("Molchanovs Wave 1", "3-day freediving certification course.", "350"),
                ("Molchanovs Wave 2", "4-day advanced freediving certification.", "450"),
            ]
        ],
    ]


def schemas(kind):
    if kind == "local":
        return [LOCAL_BUSINESS]
    if kind == "faq":
        return [faq_schema()]
    if kind == "courses":
        return courses_schema()
    return []


def build_head(meta: dict, css_href: str) -> str:
    title = meta["title"]
    desc = meta["description"]
    url = SITE + meta["path"]
    schema_lines = ""
    for s in schemas(meta.get("schema")):
        schema_lines += f'\n  <script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
    return f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/og-default.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="sitemap" type="application/xml" href="/sitemap.xml">{schema_lines}
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-LDYRTZ7WJS"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag("js", new Date());
    gtag("config", "G-LDYRTZ7WJS");
  </script>
  <script defer data-domain="lankafreediving.com" src="https://plausible.io/js/script.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Bowlby+One+SC&family=Work+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{css_href}">"""


def fix_file(rel: str) -> None:
    path = SLEEVE / rel
    meta = META[rel]
    css = "styles.css" if rel == "index.html" else "../styles.css"
    html = path.read_text()
    new_head = build_head(meta, css)
    html = re.sub(r"<head>.*?</head>", f"<head>\n{new_head}\n</head>", html, count=1, flags=re.S)
    path.write_text(html)
    print("fixed", rel)


def main():
    for rel in META:
        fix_file(rel)


if __name__ == "__main__":
    main()
