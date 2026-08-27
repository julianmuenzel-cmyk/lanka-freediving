#!/usr/bin/env python3
"""Generate publish assets and patch Sleeve HTML with SEO + guides."""

from __future__ import annotations

import json
import re
import textwrap
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLEEVE = ROOT / "explore" / "a-record-sleeve"
ASSETS = ROOT / "explore" / "assets"
PUBLIC = ROOT / "public"
SITE = "https://lankafreediving.com"
TODAY = date.today().isoformat()

SVG_SYMBOLS = """  <svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute;width:0;height:0;overflow:hidden">
    <symbol id="motif-wave" viewBox="0 0 800 70" fill="none">
      <path d="M-6 38 C 36 10, 58 56, 98 31 S 168 4, 208 41 S 278 62, 326 24 S 402 2, 444 39 S 524 66, 572 27 S 650 6, 698 42 S 762 58, 808 33" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
    </symbol>
    <symbol id="motif-spiral" viewBox="0 0 140 140" fill="none">
      <path d="M70 72 m1-5 c 9-1 13 9 6 13 c -11 9 -24-7 -17-20 c 11-20 42 3 35 25 c -9 30 -53 23 -57-8 c -5-35 40-53 68-34 c 30 20 31 74 -8 89 c -46 18 -90-20 -86-64 c 5-48 60-76 104-51" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
    </symbol>
    <symbol id="motif-sun" viewBox="0 0 200 200" fill="none">
      <circle cx="100" cy="100" r="30" stroke="currentColor" stroke-width="4"/>
      <path d="M100 14 C 103 42, 98 52, 100 64" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <path d="M147 28 C 132 50, 126 62, 120 74" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <path d="M178 62 C 150 72, 140 80, 132 90" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <path d="M186 108 C 156 106, 146 102, 134 104" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <path d="M170 150 C 148 132, 138 128, 128 122" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <path d="M132 180 C 122 154, 118 144, 112 134" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <path d="M88 186 C 94 158, 98 148, 100 136" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <path d="M48 168 C 66 148, 74 140, 82 128" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <path d="M20 128 C 46 124, 56 120, 70 118" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <path d="M18 82 C 44 90, 54 94, 68 98" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <path d="M42 40 C 60 58, 70 66, 80 76" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
    </symbol>
    <symbol id="motif-dots" viewBox="0 0 180 80">
      <circle cx="12" cy="40" r="3"/><circle cx="36" cy="18" r="2.4"/><circle cx="58" cy="52" r="3.2"/>
      <circle cx="84" cy="28" r="2.2"/><circle cx="108" cy="58" r="3.6"/><circle cx="132" cy="16" r="2.8"/>
      <circle cx="156" cy="44" r="3"/>
    </symbol>
  </svg>"""

WA_SVG = """  <a class="wa" href="https://wa.me/41787751831" data-lf-wa target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.04 2C6.58 2 2.15 6.37 2.15 11.75c0 1.72.45 3.4 1.3 4.88L2 22l5.55-1.43a10.1 10.1 0 0 0 4.49 1.05h.01c5.46 0 9.89-4.37 9.89-9.75S17.5 2 12.04 2zm0 17.82h-.01a8.4 8.4 0 0 1-4.27-1.17l-.31-.18-3.29.85.88-3.16-.2-.32a8.2 8.2 0 0 1-1.28-4.42c0-4.55 3.76-8.25 8.4-8.25 4.63 0 8.4 3.7 8.4 8.25 0 4.55-3.77 8.25-8.4 8.25zm4.6-6.18c-.25-.13-1.48-.73-1.71-.81-.23-.08-.4-.12-.56.13-.17.25-.64.8-.79.97-.14.16-.29.18-.54.06-.25-.13-1.05-.38-2-1.22-.74-.65-1.24-1.45-1.38-1.7-.15-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.13-.15.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.13-.56-1.33-.77-1.82-.2-.48-.4-.41-.56-.42h-.48c-.16 0-.43.06-.65.31-.23.25-.86.83-.86 2.03s.88 2.36 1 2.52c.12.17 1.73 2.6 4.2 3.64.59.25 1.04.4 1.4.51.59.19 1.12.16 1.54.1.47-.07 1.48-.6 1.69-1.18.21-.58.21-1.08.15-1.18-.06-.1-.23-.16-.48-.29z"/></svg>
  </a>"""

FOOTER_EXTRA = """        <li><a href="{guides_href}">Guides</a></li>"""

NAV_GUIDES = """        <li><a href="{guides_href}">Guides</a></li>"""

PAGES = {
    "index.html": {"path": "/", "priority": "1.0"},
    "courses/index.html": {"path": "/courses/", "priority": "0.9"},
    "retreat/index.html": {"path": "/retreat/", "priority": "0.9"},
    "expedition/index.html": {"path": "/expedition/", "priority": "0.8"},
    "school/index.html": {"path": "/school/", "priority": "0.9"},
    "faq/index.html": {"path": "/faq/", "priority": "0.8"},
    "contact/index.html": {"path": "/contact/", "priority": "0.8"},
}

GUIDES = [
    {
        "slug": "molchanovs-vs-padi-sri-lanka",
        "title": "Molchanovs vs PADI Freediving in Sri Lanka",
        "description": "PADI is easier to find. Molchanovs is what we teach. How the two systems differ for a course in Unawatuna.",
        "hero_pair": "pair-cobalt",
        "caption": "Compare",
        "h1": "Same ocean. Different school.",
        "subtitle": "PADI shops are everywhere. Molchanovs is a training system — that is the difference.",
        "image": ("photos/julian-line.jpg", "Molchanovs line training in Unawatuna, Sri Lanka"),
        "body": """
          <p>If you search “freediving Sri Lanka” you will mostly find PADI. That is not a slight — PADI is the largest dive organisation in the world, and Unawatuna has long-running PADI shops. <a href="../../school/">Lanka Freediving</a> is a Molchanovs school. This page is the honest split so you book the course that matches what you want, not the logo you recognised first.</p>
          <h2>The short version</h2>
          <p><strong>PADI Freediver</strong> is a recreational pathway. It is familiar if you already scuba, easy to find on the south and east coasts, and designed to get you in the water with a standardised syllabus.</p>
          <p><strong>Molchanovs</strong> is a freediving-only education system built by athletes. The Waves are a progression: breathwork, equalisation, rescue, and depth on a line — closer to how serious freedivers actually train. Certification is digital and recognised worldwide in the Molchanovs network.</p>
          <p>We teach Molchanovs. We do not teach PADI. If you want PADI, book a PADI shop. If you want small-group Molchanovs coaching in Unawatuna, that is us.</p>
          <h2>What actually differs in the water</h2>
          <table class="data-table">
            <thead><tr><th></th><th>Molchanovs (us)</th><th>PADI (typical shop)</th></tr></thead>
            <tbody>
              <tr><td>Focus</td><td>Freediving as a sport and skill</td><td>Recreational intro, scuba-adjacent</td></tr>
              <tr><td>Entry course</td><td>Wave 1 — 3 days, certification</td><td>Freediver — often 2–3 days</td></tr>
              <tr><td>Try-it session</td><td>Discover, half day, €120</td><td>Basic Freediver / try dive</td></tr>
              <tr><td>Group size here</td><td>Maximum 4</td><td>Varies by shop</td></tr>
              <tr><td>Where we run</td><td>Unawatuna, November–April</td><td>South in season; some shops move east in monsoon</td></tr>
            </tbody>
          </table>
          <h2>Which should you book?</h2>
          <p>Book PADI if you already collect PADI cards, you want the most widely recognised recreational logo, or you are on the east coast outside our season.</p>
          <p>Book Molchanovs if you care about technique, you might continue to Wave 2 or coaching, or you want a school that only teaches freediving. Read <a href="../molchanovs-courses-explained/">Discover vs Wave 1 vs Wave 2</a> for depth and time.</p>
          <h2>Can you mix them later?</h2>
          <p>Skills transfer more than cards. A solid Wave 1 student is not starting from zero at a PADI shop, and the reverse is also true — but agencies do not automatically cross-certify. If you already hold PADI Freediver and want Wave 2 with us, <a href="../../contact/">message us</a> with your card and we will place you honestly.</p>
          <h2>Price in Unawatuna</h2>
          <p>Our Molchanovs prices are public: Discover €120, Wave 1 €350, Wave 2 €450. Full numbers and what is included: <a href="../freediving-course-cost-sri-lanka/">how much a freediving course costs</a>.</p>
        """,
        "related": ["molchanovs-courses-explained", "first-freedive-unawatuna", "freediving-course-cost-sri-lanka"],
    },
    {
        "slug": "freediving-course-cost-sri-lanka",
        "title": "How Much a Freediving Course Costs in Sri Lanka",
        "description": "Molchanovs course prices in Unawatuna: Discover €120, Wave 1 €350, Wave 2 €450. What is included, deposits, and how we compare.",
        "hero_pair": "pair-yellow",
        "caption": "Prices",
        "h1": "The numbers. No drip.",
        "subtitle": "Public prices, what they include, and how to budget a week in Unawatuna.",
        "image": ("photos/julian-boat.jpg", "Freediving boat in Unawatuna, Sri Lanka"),
        "body": """
          <p>Freediving course prices in Sri Lanka vary by agency, group size, and whether gear and boat are included. These are <strong>Lanka Freediving</strong> prices for the 2026 season in Unawatuna. They are the same numbers on our <a href="../../courses/">courses page</a> — this article is for people who search “how much” before they click Book.</p>
          <h2>Course prices (EUR)</h2>
          <table class="data-table">
            <thead><tr><th>Course</th><th>Time</th><th>Price</th><th>Certification</th></tr></thead>
            <tbody>
              <tr><td>Discover Freediving</td><td>Half day</td><td>€120</td><td>None — experience only</td></tr>
              <tr><td>Molchanovs Wave 1</td><td>3 days</td><td>€350</td><td>Wave 1, 12–20 m</td></tr>
              <tr><td>Molchanovs Wave 2</td><td>4 days</td><td>€450</td><td>Wave 2, 24–30 m</td></tr>
              <tr><td>5-day retreat</td><td>5 days</td><td>From €900</td><td>Wave 1 or 2, plus hotel and meals</td></tr>
            </tbody>
          </table>
          <p>Maximum four students on courses. Retreat is max eight guests. Advanced coaching is priced on request.</p>
          <h2>What is included</h2>
          <ul class="plain">
            <li>All gear: wetsuit, long fins, mask, snorkel, weights, lanyard</li>
            <li>Pool and open-water sessions, boat when we need it</li>
            <li>Online theory and exam for Wave courses</li>
            <li>Underwater photos on Wave courses</li>
          </ul>
          <p>Not included in a standard course: hotel, meals, airport transfer. Those sit in the <a href="../../retreat/">retreat</a> package.</p>
          <h2>Deposit and cancellation</h2>
          <p>30% deposit to hold a course date (50% for retreat and expeditions). Balance on day one. More than 14 days before start: deposit refunded. Inside 14 days: we transfer you to another date in the same season. Weather cancellations are rescheduled or refunded — we do not run unsafe sessions to keep a booking.</p>
          <h2>Budget around the course</h2>
          <p>Unawatuna guesthouses start cheap on the beach road; boutique rooms cost more on the headland. Tuk-tuks are short money. Food is inexpensive if you eat local. A Wave 1 week is course + 4–5 nights + food + a Galle afternoon — not a €2,000 resort week unless you choose that hotel.</p>
          <h2>Compared with PADI in town</h2>
          <p>PADI Freediver in Unawatuna is often in a similar euro band, sometimes advertised cheaper before materials and certification fees. Always ask what the total is. We publish a single number. Context: <a href="../molchanovs-vs-padi-sri-lanka/">Molchanovs vs PADI</a>.</p>
          <h2>First time? Start smaller</h2>
          <p>If you are not ready to spend three days, Discover is €120. Many guests book Wave 1 after that. Read <a href="../first-freedive-unawatuna/">your first freedive in Unawatuna</a> if you are nervous about depth or swimming.</p>
          <p><a href="../../contact/">Get in touch</a> with dates — we confirm within 24 hours.</p>
        """,
        "related": ["molchanovs-courses-explained", "first-freedive-unawatuna", "molchanovs-vs-padi-sri-lanka"],
    },
    {
        "slug": "first-freedive-unawatuna",
        "title": "Your First Freedive in Unawatuna",
        "description": "Is freediving scary? Do you need to be a strong swimmer? What happens on a first session in Unawatuna — depth, gear, and how we teach beginners.",
        "hero_pair": "pair-pink",
        "caption": "Beginners",
        "h1": "You do not start at 20 metres.",
        "subtitle": "First session in Unawatuna: breath, pool, then a short, supervised dip. Groups of four.",
        "image": ("photos/session-sun.jpg", "Beginner freediving session in warm Unawatuna water"),
        "body": """
          <p>Most people who message us have the same fear: <em>I will panic, I cannot hold my breath, I will look stupid.</em> That is normal. A first freedive in Unawatuna is not a depth attempt. It is breathing, relaxation, and a short, supervised descent with a buddy who is an instructor — not a GoPro boat.</p>
          <h2>Do you need to be a strong swimmer?</h2>
          <p>For <strong>Discover</strong> (half day, €120): you should be comfortable in water. We are not testing laps.</p>
          <p>For <strong>Wave 1</strong> (3 days, €350): you must swim 200 m unassisted. That is a Molchanovs standard, not ours to waive. If you are close, say so — we will tell you honestly whether to start with Discover.</p>
          <h2>Is it scary?</h2>
          <p>The scary version of freediving is social media: blacked-out athletes, huge fins, 40 metres. That is not day one. Day one is learning to exhale slowly, to equalise before it hurts, and to turn around early. Small groups (max four) mean you are not waiting at the back of a crowd while someone else takes the line.</p>
          <h2>What a first session looks like</h2>
          <ol class="plain">
            <li>Breathing and body scan on land — not “take a huge gulp.”</li>
            <li>Pool or sheltered water: float, duck dive, recover on the surface with a buddy.</li>
            <li>If you booked Wave 1, later days add the line, Frenzel equalisation, and open water to a depth you have earned — typically well inside 12–20 m by the end of the course, not on hour one.</li>
          </ol>
          <p>Gear is provided. Bring swimwear, a towel, reef-safe sunscreen. Details: <a href="../../faq/">FAQ</a>.</p>
          <h2>How deep on day one?</h2>
          <p>Discover stays shallow and supervised. Wave 1 builds across three days. Nobody is dropped on a deep line to “see if you can.” Depth is a by-product of equalisation and calm — we stop when either is missing.</p>
          <h2>What you might see</h2>
          <p>Warm water (27–30°C in season), reef fish, sometimes turtles on calm mornings. Read <a href="../turtles-freediving-unawatuna/">turtles and marine life</a> so you know the rules before you get excited and reach.</p>
          <h2>Which course to book</h2>
          <p>One free morning: Discover. Three days and a card you can take home: Wave 1. Already certified and hunting depth: Wave 2. Comparison: <a href="../molchanovs-courses-explained/">Molchanovs courses explained</a> and <a href="../molchanovs-vs-padi-sri-lanka/">Molchanovs vs PADI</a>.</p>
          <p>Still unsure? <a href="../../contact/">Tell us your swimming background and dates</a>. We would rather put you on Discover than rush a Wave 1.</p>
        """,
        "related": ["molchanovs-courses-explained", "turtles-freediving-unawatuna", "freediving-course-cost-sri-lanka"],
    },
    {
        "slug": "turtles-freediving-unawatuna",
        "title": "Turtles and Marine Life While Freediving in Unawatuna",
        "description": "Green turtles in Unawatuna, what else you see on the reef, and how we dive so wildlife stays wild. Season: November–April.",
        "hero_pair": "pair-turq",
        "caption": "Wildlife",
        "h1": "Quiet gets you closer.",
        "subtitle": "Turtles, reef fish, and the rules: look, do not chase, do not touch.",
        "image": ("photos/turtle.jpg", "Sea turtle in the water off Unawatuna, Sri Lanka"),
        "body": """
          <p>Unawatuna is not a private aquarium. It is a busy bay with boats, snorkel tours, and — on the right morning — green turtles grazing or travelling along the reef. Freediving helps because you are silent. No regulator bubbles. That is the whole trick, and it is also why you have to be more careful, not less.</p>
          <h2>Will I see a turtle?</h2>
          <p>Often, in season (November–April), on calm mornings. Not guaranteed. Anyone who sells a “turtle guarantee” is selling a chase. We do not chase. If a turtle is there, we stay off to the side, keep our hands in, and leave it a way out.</p>
          <h2>What else is on the reef</h2>
          <p>Typical south-coast rock reef and sand: parrotfish, bannerfish, lionfish, puffers, the odd moray, sometimes a ray. Coral cover here is not east-coast Nilaveli — bleaching and the 2004 tsunami still show. You come for warm water, easy access, and animals that use the bay, not for a pristine wall.</p>
          <h2>Rules we actually use</h2>
          <ul class="plain">
            <li>No touching turtles, no riding, no grabbing the shell for a photo</li>
            <li>No feeding</li>
            <li>Reef-safe sunscreen, applied on land, not in the water</li>
            <li>Give animals space on the line and on the reef — your turn can wait</li>
          </ul>
          <p>If you want a first session that is about calm, not content, start with <a href="../first-freedive-unawatuna/">your first freedive</a> or a <a href="../../courses/">Discover</a>.</p>
          <h2>Snorkel vs freedive</h2>
          <p>Snorkel tours stay on the surface and often cluster. A freedive course teaches you to duck-dive cleanly and recover — less thrashing, less crowding. You still share the water with other boats. We pick sites and timing around that.</p>
          <h2>When to come</h2>
          <p>South-coast season is November–April. That is when we run the school and when the bay is most usable. Month-by-month: <a href="../best-time-freediving-sri-lanka/">best time for freediving in Sri Lanka</a>.</p>
          <p>Book a course, not a wildlife ticket: <a href="../../contact/">get in touch</a>.</p>
        """,
        "related": ["first-freedive-unawatuna", "freediving-unawatuna", "unawatuna-travel-guide"],
    },
    {
        "slug": "top-10-southern-sri-lanka",
        "title": "Top 10 Things to Do on Sri Lanka's South Coast",
        "description": "From Galle Fort to Mirissa whales — the best activities near Unawatuna on Sri Lanka's southern coast.",
        "hero_pair": "pair-red",
        "caption": "South coast",
        "h1": "Ten reasons to stay longer.",
        "subtitle": "Unawatuna is the base. The south coast is the playground.",
        "image": ("photos/session-open.jpg", "Freediver in open water off Unawatuna, Sri Lanka"),
        "body": """
          <p>The south coast of Sri Lanka packs a lot into a short strip of road. Most travellers land in Colombo, head straight to Galle or Unawatuna, and realise three days is not enough. This list is what we send friends who ask what to do between freediving sessions — or instead of them.</p>
          <h2>1. Galle Fort at golden hour</h2>
          <p>The Dutch fort is fifteen minutes from Unawatuna. Walk the ramparts, get lost in the cobblestone lanes, and eat at one of the courtyard restaurants. Go late afternoon when the light turns the walls amber and the day-trippers leave.</p>
          <h2>2. Freediving or snorkelling in Unawatuna Bay</h2>
          <p>Warm water, reef fish, turtles on calm mornings. If you want more than a snorkel, a <a href="../../courses/">Molchanovs Discover session</a> or <a href="../freediving-unawatuna/">freediving guide</a> is the proper way in — one breath, no bubbles, closer to the reef.</p>
          <h2>3. Jungle Beach and the coastal walk</h2>
          <p>A twenty-minute walk over the headland from Unawatuna brings you to a smaller cove with fewer boats. Good for a swim, a beer, and watching the fishing boats come in.</p>
          <h2>4. Mirissa whale watching (December–April)</h2>
          <p>Blue whales and sperm whales pass offshore in season. Book an early boat from Mirissa — about an hour east. Combine with a night in Mirissa if you want surf and a different vibe.</p>
          <h2>5. Weligama surf lesson</h2>
          <p>Soft beach break, hire boards on the sand, instructors everywhere. Even if you freedive, a morning on a longboard is worth it. Weligama is twenty minutes from Unawatuna.</p>
          <h2>6. Handunugoda tea estate</h2>
          <p>A working tea factory near Koggala where you can see virgin white tea processed by hand. Less touristy than the hill-country factories and easy to reach from the coast.</p>
          <h2>7. Koggala lake boat trip</h2>
          <p>Mangroves, cinnamon islands, monitor lizards, and stilt fishermen on the lake near Koggala airport. Quiet counterpoint to open-ocean days.</p>
          <h2>8. Japanese Peace Pagoda</h2>
          <p>On the hill above Unawatuna. Short tuk-tuk ride, panoramic views over the bay, especially at sunset. Respectful dress required.</p>
          <h2>9. Ahangama / Midigama surf and cafés</h2>
          <p>The stretch between Unawatuna and Weligama has grown into a café-and-surf corridor. Rent a scooter, stop where it looks busy, swim where it looks empty.</p>
          <h2>10. Five-day freediving retreat</h2>
          <p>If you have a week, structure it around water. Our <a href="../../retreat/">Unawatuna retreat</a> combines daily pool and open-water sessions with accommodation and meals — Molchanovs Wave 1 or Wave 2 included. See also our <a href="../south-coast-7-day-itinerary/">seven-day south coast itinerary</a>.</p>
          <h2>Planning tips</h2>
          <p>November through April is dry season on the south coast — the same window we run <a href="../../school/">Lanka Freediving</a>. Shoulder months (November, April) mean fewer crowds. Peak is Christmas through January; book accommodation and courses early.</p>
        """,
        "related": ["unawatuna-travel-guide", "galle-and-unawatuna", "south-coast-7-day-itinerary"],
    },
    {
        "slug": "unawatuna-travel-guide",
        "title": "Unawatuna Travel Guide — Beaches, Food & Freediving",
        "description": "How to get to Unawatuna, where to stay, what to eat, and how to plan freediving on Sri Lanka's south coast.",
        "hero_pair": "pair-yellow",
        "caption": "Unawatuna",
        "h1": "Small bay. Big week.",
        "subtitle": "Everything you need before you land in the south.",
        "image": ("photos/session-sun.jpg", "Freediver descending in warm Unawatuna water"),
        "body": """
          <p>Unawatuna is a curved bay on Sri Lanka's south coast, tucked between Galle and Mirissa. It became a traveller staple for good reason: swimmable water most of the year (in season), restaurants along the beach road, and easy day trips in every direction. It is also where we run <a href="../../school/">Lanka Freediving</a> from November to April.</p>
          <h2>Getting there</h2>
          <p>Colombo Bandaranaike Airport (CMB) is roughly 2.5 hours by car. Pre-book a transfer or take the coastal train to Galle then a tuk-tuk — the train is slow but scenic. From Galle Fort it is fifteen minutes to Unawatuna.</p>
          <h2>Best time to visit</h2>
          <p>Dry season on the south coast runs <strong>November through April</strong>. Sea is calmest, visibility best for diving and freediving. Monsoon pushes rain and swell to this coast from May onward — we close the school outside season. More detail in our <a href="../best-time-freediving-sri-lanka/">best time for freediving</a> guide.</p>
          <h2>Where to stay</h2>
          <p>Beach-road guesthouses suit budget travellers; boutique hotels on the headland suit couples and retreat guests. Book early for December–January. If you join our <a href="../../retreat/">five-day retreat</a>, preferential hotel rates apply (property confirmed per date).</p>
          <h2>Food</h2>
          <p>Beach restaurants serve grilled fish, kottu, and curry-and-rice. Galle Fort has higher-end options. Try a proper Sri Lankan breakfast — hoppers, string hoppers, dal — at least once.</p>
          <h2>Getting around</h2>
          <p>Tuk-tuks are everywhere and cheap for short hops. Scooter rental is common; wear a helmet and go slow. For Galle, Mirissa, or Weligama, a half-day driver is often easier than multiple tuk-tuk rides.</p>
          <h2>Freediving in Unawatuna</h2>
          <p>Water temperature is typically 27–30°C in season. Reef and sand patches sit a short boat ride out; turtles are common on calm mornings. We teach Molchanovs <a href="../../courses/">Discover, Wave 1, and Wave 2</a> in groups of four maximum. Read our full <a href="../freediving-unawatuna/">freediving in Unawatuna</a> guide for course fit and what to bring.</p>
          <h2>Safety and etiquette</h2>
          <p>Reef-safe sunscreen, respect temple dress codes on the pagoda hill, and do not touch marine life. Currents are usually mild in bay mornings; open-water sessions follow weather and visibility.</p>
        """,
        "related": ["best-time-freediving-sri-lanka", "freediving-unawatuna", "top-10-southern-sri-lanka"],
    },
    {
        "slug": "galle-and-unawatuna",
        "title": "Galle Fort & Unawatuna — Day Trip Guide",
        "description": "Combine Galle Fort history with Unawatuna beach life. How to spend one day or a full week on Sri Lanka's south coast.",
        "hero_pair": "pair-pink",
        "caption": "Galle · Unawatuna",
        "h1": "Fort in the morning. Water in the afternoon.",
        "subtitle": "Two places, one trip — fifteen minutes apart.",
        "image": ("photos/julian-boat.jpg", "Freediving boat departing Unawatuna near Galle"),
        "body": """
          <p>Galle and Unawatuna are often booked as one trip — and they should be. Galle Fort is UNESCO-listed Dutch colonial history, cafés, and rampart walks. Unawatuna is the bay where you actually swim, dive, and slow down. Together they are the anchor of the south coast.</p>
          <h2>One-day split</h2>
          <p><strong>Morning in Galle Fort:</strong> enter through the main gate, walk clockwise on the walls, visit the lighthouse, and explore Pedlar Street shops. Coffee at one of the fort roasters. <strong>Afternoon in Unawatuna:</strong> swim in the bay, sunset from the pagoda hill or beach. Tuk-tuk between them takes fifteen to twenty minutes depending on traffic.</p>
          <h2>Why base in Unawatuna</h2>
          <p>Galle has more hotels but less beach access. Unawatuna puts you in the water daily — useful if you are freediving or learning. Our school meets in Unawatuna; Galle is an easy add-on, not a commute.</p>
          <h2>What to see in the fort</h2>
          <ul class="plain">
            <li>Ramparts and sunset viewpoints</li>
            <li>Dutch Reformed Church and maritime museum</li>
            <li>Boutiques and gem shops (buy carefully)</li>
            <li>Fort restaurants — book dinner for weekends</li>
          </ul>
          <h2>Beyond the fort</h2>
          <p>Don't skip the rest of Galle town if you have time — local markets and the cricket ground give a different feel from the tourist fort interior. East toward Koggala, you can combine a lake boat trip on the same day as a fort visit if you start early.</p>
          <h2>Freediving between the two</h2>
          <p>If you have three or more days, slot a <a href="../../courses/">Wave 1 course</a> in Unawatuna and use Galle for your rest days. See our <a href="../top-10-southern-sri-lanka/">top ten south coast activities</a> for Mirissa, Weligama, and tea country options within an hour.</p>
        """,
        "related": ["unawatuna-travel-guide", "top-10-southern-sri-lanka", "south-coast-7-day-itinerary"],
    },
    {
        "slug": "best-time-freediving-sri-lanka",
        "title": "Best Time for Freediving in Sri Lanka",
        "description": "When to visit Unawatuna for calm seas and warm water. Sri Lanka freediving season explained month by month.",
        "hero_pair": "pair-turq",
        "caption": "Season",
        "h1": "November to April. That's the window.",
        "subtitle": "Dry season on the south coast is freediving season.",
        "image": ("photos/session-line.jpg", "Freediver on the line in calm Sri Lankan seas"),
        "body": """
          <p>Sri Lanka has two monsoons, which means the "best" coast depends on the month. For Unawatuna and the south, the answer is straightforward: <strong>November through April</strong>. That is when we operate <a href="../../school/">Lanka Freediving</a> and when conditions are most reliable for courses and open-water sessions.</p>
          <h2>Month by month</h2>
          <p><strong>November:</strong> Season opens. Seas settle after the southwest monsoon; fewer tourists than peak. Good visibility building.</p>
          <p><strong>December–January:</strong> Peak travel. Book courses and hotels early. Calm mornings, warm water 27–29°C.</p>
          <p><strong>February–March:</strong> Often excellent visibility and still dry. Our favourite teaching months.</p>
          <p><strong>April:</strong> Still diveable; occasional heat and humidity rising. Last weeks of our season.</p>
          <p><strong>May–October:</strong> Southwest monsoon affects this coast — more rain, less predictable seas. We do not run scheduled courses; some operators move to the east (Trincomalee) where season is inverted.</p>
          <h2>Water conditions</h2>
          <p>Expect 27–30°C water — most students fine in 3 mm or rash vest. Visibility on calm mornings often exceeds 15 m on reef sites. Afternoon wind can chop the surface; we schedule around it.</p>
          <h2>Planning your course</h2>
          <p>Wave 1 needs three days plus theory time before arrival. Discover fits a free half-day. The <a href="../../retreat/">five-day retreat</a> is best with a full week in country. Check <a href="../molchanovs-courses-explained/">which Molchanovs course</a> fits your trip length.</p>
          <h2>Whales and weather</h2>
          <p>Whale-watching off Mirissa overlaps our season (roughly December–April). Combine with freediving if you have spare days — see the <a href="../top-10-southern-sri-lanka/">south coast top ten</a>.</p>
        """,
        "related": ["freediving-unawatuna", "unawatuna-travel-guide", "molchanovs-courses-explained"],
    },
    {
        "slug": "freediving-unawatuna",
        "title": "Freediving in Unawatuna — Complete Guide",
        "description": "Why Unawatuna works for freediving, what courses are available, and how to book Molchanovs training in Sri Lanka.",
        "hero_pair": "pair-forest",
        "caption": "Freediving",
        "h1": "Warm water. Small groups. Real certification.",
        "subtitle": "Molchanovs courses from Discover to Wave 2 in Unawatuna.",
        "image": ("photos/julian-depth.jpg", "Freediving depth session in Unawatuna, Sri Lanka"),
        "body": """
          <p>Unawatuna is one of the most practical places in Sri Lanka to learn freediving: warm water, reef access by boat, a full tourist infrastructure, and calm mornings in season. <a href="../../school/">Lanka Freediving</a> is a Molchanovs school running November–April with a maximum of four students per course.</p>
          <h2>Why freedive here (not just snorkel)</h2>
          <p>One breath changes how you move underwater — quieter, slower, closer to turtles and reef fish without bubble noise. Proper training covers breathwork, equalisation, buddy safety, and rescue skills scuba courses never touch.</p>
          <h2>Courses we run</h2>
          <ul class="plain">
            <li><strong>Discover</strong> — half day, €120, no certification, taste of breath-hold and pool/shallow water</li>
            <li><strong>Wave 1</strong> — 3 days, €350, full Molchanovs certification to 12–20 m</li>
            <li><strong>Wave 2</strong> — 4 days, €450, advanced techniques to 24–30 m</li>
            <li><strong>Retreat</strong> — 5 days immersive, from €900, certification + hotel + meals</li>
          </ul>
          <p>Full breakdown: <a href="../../courses/">courses page</a> and <a href="../molchanovs-courses-explained/">Molchanovs explained</a>.</p>
          <h2>Typical day</h2>
          <p>Morning theory or breathwork, pool skills mid-morning, open water after lunch when the bay is calm. Small groups mean actual coaching time — not waiting on twelve other students.</p>
          <h2>Who teaches</h2>
          <p>Julian is a Molchanovs instructor, Evolution Spearfishing instructor, and competition safety diver. Training follows Molchanovs standards with conservative progression — depth is earned, not forced.</p>
          <h2>What to bring</h2>
          <p>Swimwear, reef-safe sunscreen, towel. We provide wetsuits, fins, masks, and lines. Must swim 200 m for Wave 1+. More in our <a href="../../faq/">FAQ</a>.</p>
          <h2>Book</h2>
          <p><a href="../../contact/">Contact form</a>, WhatsApp, or hello@lankafreediving.com — we confirm within 24 hours. Deposit secures your date and theory access.</p>
        """,
        "related": ["molchanovs-courses-explained", "first-freedive-unawatuna", "turtles-freediving-unawatuna"],
    },
    {
        "slug": "molchanovs-courses-explained",
        "title": "Molchanovs Courses Explained — Discover vs Wave 1 vs Wave 2",
        "description": "Which Molchanovs freediving course should you take in Sri Lanka? Compare Discover, Wave 1, and Wave 2.",
        "hero_pair": "pair-cream",
        "caption": "Molchanovs",
        "h1": "Pick the right wave.",
        "subtitle": "Discover, Wave 1, or Wave 2 — what each course actually gives you.",
        "image": ("photos/julian-line.jpg", "Molchanovs instructor on the freediving line in Unawatuna"),
        "body": """
          <p>Molchanovs is the world's largest freediving education system — structured progression, digital certification, and standards recognised from Sri Lanka to competition circuits. At <a href="../../courses/">Lanka Freediving</a> we teach Discover, Wave 1, Wave 2, and advanced coaching.</p>
          <h2>Discover Freediving</h2>
          <p><strong>Half day · €120 · no certification</strong></p>
          <p>For curious travellers — snorkellers, surfers, partners of divers. You learn breathing fundamentals and try supervised breath-holds in pool or shallow water. Good if you are unsure about a full course.</p>
          <h2>Wave 1</h2>
          <p><strong>3 days · €350 · Molchanovs Wave 1 certification</strong></p>
          <p>The proper entry point. Online theory before arrival, pool sessions (static, dynamic, rescue), then open water to 12–20 m on line and constant weight. You must swim 200 m unassisted. Leaves you certified worldwide.</p>
          <h2>Wave 2</h2>
          <p><strong>4 days · €450 · Molchanovs Wave 2 certification</strong></p>
          <p>For Wave 1 graduates or equivalent. Mouthfill equalisation, freefall, no-fins technique, rescue from depth, open water to 24–30 m. Where technique replaces adrenaline.</p>
          <h2>Wave 2+ / coaching</h2>
          <p>Flexible duration, price on request. Depth prep, competition lines, spearfishing crossover for qualified students.</p>
          <h2>Which should you book?</h2>
          <table class="data-table">
            <thead><tr><th>Situation</th><th>Course</th></tr></thead>
            <tbody>
              <tr><td>One free morning, first time</td><td>Discover</td></tr>
              <tr><td>3–4 days, want certification</td><td>Wave 1</td></tr>
              <tr><td>Already Wave 1, want depth</td><td>Wave 2</td></tr>
              <tr><td>Full week, immersive</td><td><a href="../../retreat/">Retreat</a></td></tr>
            </tbody>
          </table>
          <p>Still unsure? <a href="../../contact/">Message us</a> with your dates and experience — we place you correctly.</p>
        """,
        "related": ["freediving-unawatuna", "molchanovs-vs-padi-sri-lanka", "freediving-course-cost-sri-lanka"],
    },
    {
        "slug": "freediving-vs-scuba-sri-lanka",
        "title": "Freediving vs Scuba Diving in Sri Lanka",
        "description": "Should you freedive or scuba in Sri Lanka? Compare experience, training time, cost, and marine life encounters.",
        "hero_pair": "pair-burnt",
        "caption": "Compare",
        "h1": "One breath. No tanks.",
        "subtitle": "How freediving and scuba differ on the south coast.",
        "image": ("photos/session-pair.jpg", "Two freedivers descending together in Sri Lanka"),
        "body": """
          <p>Sri Lanka offers both scuba and freediving on the south coast in season. They look similar from the beach — boats, wetsuits, fish — but the experience and skill set are different. Here is an honest comparison if you are planning a trip to Unawatuna or Galle.</p>
          <h2>The basic difference</h2>
          <p>Scuba divers breathe compressed air from a tank and can stay down longer at recreational depths. Freedivers take one breath, descend, and return on that single lungful — relying on relaxation, equalisation, and efficiency rather than equipment.</p>
          <h2>Experience underwater</h2>
          <p>Freediving is silent. No bubbles, less disturbance, often closer approaches from turtles and reef fish. Scuba gives more bottom time to explore wrecks and deeper reef walls with less athletic demand per dive.</p>
          <h2>Training time</h2>
          <p>A Discover freediving session is half a day. Molchanovs Wave 1 is three days. Open Water scuba is typically three to four days as well — similar commitment for entry certification, but skills do not transfer automatically.</p>
          <h2>Cost in Sri Lanka</h2>
          <p>Discover freediving from €120; Wave 1 from €350 at Lanka Freediving. Scuba fun dives and courses vary by shop — compare what is included (gear, boat, park fees).</p>
          <h2>Can you do both?</h2>
          <p>Yes, on a long trip — but not usually the same day. Freediving after scuba requires careful scheduling because of residual nitrogen; we advise separating them by 24 hours or planning freediving first.</p>
          <h2>Which fits you?</h2>
          <p>Choose scuba if you want maximum underwater time with less breath-hold stress. Choose freediving if you want minimal gear, a meditative sport, and the challenge of self-reliance on one breath. Many travellers try <a href="../../courses/">Discover</a> before committing to either path.</p>
        """,
        "related": ["freediving-unawatuna", "molchanovs-vs-padi-sri-lanka", "molchanovs-courses-explained"],
    },
    {
        "slug": "south-coast-7-day-itinerary",
        "title": "Sri Lanka South Coast — 7-Day Itinerary",
        "description": "A one-week south coast Sri Lanka itinerary: Galle, Unawatuna, freediving, Mirissa, and Weligama surf.",
        "hero_pair": "pair-red",
        "caption": "Itinerary",
        "h1": "Seven days. One coast.",
        "subtitle": "A practical week with water, fort, and whales.",
        "image": ("photos/session-pair.jpg", "Freedivers on the line off Sri Lanka south coast"),
        "body": """
          <p>This itinerary assumes <strong>November–April</strong> dry season and bases you in Unawatuna with day trips east and west. Adjust if you are taking a full <a href="../../courses/">Wave 1 course</a> (three water days) or the <a href="../../retreat/">five-day retreat</a>.</p>
          <h2>Day 1 — Arrive, Unawatuna</h2>
          <p>Transfer from Colombo (2.5 h). Check in, swim the bay, sunset walk to Jungle Beach or the pagoda. Early night — jet lag and tomorrow's water.</p>
          <h2>Day 2 — Galle Fort</h2>
          <p>Morning ramparts and coffee in the fort. Afternoon back in Unawatuna for snorkel or beach. Dinner on the beach road.</p>
          <h2>Days 3–5 — Freediving Wave 1 (or retreat)</h2>
          <p>Three-day certification: theory, pool, open water. If not diving, substitute Weligama surf (day 3), Koggala lake boat (day 4), and Handunugoda tea (day 5). See <a href="../top-10-southern-sri-lanka/">top ten activities</a>.</p>
          <h2>Day 6 — Mirissa</h2>
          <p>Whale watching if in season (book ahead). Lunch in Mirissa, optional coconut hill viewpoint. Return to Unawatuna for last-night dinner.</p>
          <h2>Day 7 — Depart or extend</h2>
          <p>Last swim, transfer to airport, or head east toward Yala safari (add 2–3 days) or hill country (add 3–4 days). Many guests wish they booked two weeks.</p>
          <h2>Extensions</h2>
          <ul class="plain">
            <li><strong>+3 days:</strong> Yala national park safari</li>
            <li><strong>+4 days:</strong> Ella tea country and trains</li>
            <li><strong>+5 days:</strong> Our <a href="../../retreat/">freediving retreat</a> instead of scattered day trips</li>
          </ul>
          <p>Questions on dates? <a href="../../contact/">Get in touch</a> — we help fit courses into your route.</p>
        """,
        "related": ["unawatuna-travel-guide", "top-10-southern-sri-lanka", "best-time-freediving-sri-lanka"],
    },
]

GUIDE_SEO = {
    "molchanovs-vs-padi-sri-lanka": (
        "Molchanovs vs PADI Freediving in Sri Lanka",
        "PADI is easier to find. Molchanovs is what we teach. How the two systems differ for a course in Unawatuna.",
    ),
    "freediving-course-cost-sri-lanka": (
        "How Much a Freediving Course Costs in Sri Lanka",
        "Molchanovs prices in Unawatuna: Discover €120, Wave 1 €350, Wave 2 €450. What is included, deposits, and how to budget.",
    ),
    "first-freedive-unawatuna": (
        "Your First Freedive in Unawatuna (Beginners)",
        "Is freediving scary? Do you need to swim 200 m? What happens on a first Discover or Wave 1 session in Unawatuna.",
    ),
    "turtles-freediving-unawatuna": (
        "Turtles While Freediving in Unawatuna",
        "Green turtles and reef life in Unawatuna — when you might see them, and the rules so wildlife stays wild.",
    ),
    "top-10-southern-sri-lanka": (
        "10 Things to Do on Sri Lanka's South Coast",
        "Galle Fort, Unawatuna beach, whales in Mirissa, and a freediving course — the best days near Lanka Freediving.",
    ),
    "unawatuna-travel-guide": (
        "Unawatuna Travel Guide: Beach, Food & Freediving",
        "How to get to Unawatuna, where to stay, what to eat, and how to plan a Molchanovs freediving course on Sri Lanka's south coast.",
    ),
    "galle-and-unawatuna": (
        "Galle Fort & Unawatuna Day Trip Guide",
        "How to combine Galle Fort with Unawatuna beach and a freediving course. Fifteen minutes apart on Sri Lanka's south coast.",
    ),
    "best-time-freediving-sri-lanka": (
        "Best Time for Freediving in Sri Lanka (Nov–April)",
        "South-coast season is November to April. Month-by-month water, weather, and when Lanka Freediving is open in Unawatuna.",
    ),
    "freediving-unawatuna": (
        "Freediving in Unawatuna: Courses, Sites & Season",
        "Why Unawatuna works for freediving, which Molchanovs course to take, and how to book small-group training in Sri Lanka.",
    ),
    "molchanovs-courses-explained": (
        "Molchanovs Discover vs Wave 1 vs Wave 2",
        "Which Molchanovs course to take in Sri Lanka: half-day Discover, 3-day Wave 1, or 4-day Wave 2. Depth, time, and who each is for.",
    ),
    "freediving-vs-scuba-sri-lanka": (
        "Freediving vs Scuba Diving in Sri Lanka",
        "Compare training time, cost, and marine life on the south coast — and when a Molchanovs course is the better fit.",
    ),
    "south-coast-7-day-itinerary": (
        "7-Day Sri Lanka South Coast Itinerary",
        "A one-week plan: Galle, Unawatuna freediving, Mirissa, and Weligama — built around a Molchanovs course.",
    ),
}

LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": ["SportsActivityLocation", "LocalBusiness"],
    "name": "Lanka Freediving",
    "description": "Molchanovs freediving school in Unawatuna, Sri Lanka. Small-group courses, retreat, and expeditions. Open November through April.",
    "url": SITE,
    "email": "hello@lankafreediving.com",
    "image": f"{SITE}/assets/og-default.jpg",
    "logo": f"{SITE}/icon-192.png",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Unawatuna",
        "addressRegion": "Southern Province",
        "addressCountry": "LK",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 6.0144, "longitude": 80.2489},
    "areaServed": "Unawatuna, Galle, Southern Province, Sri Lanka",
    "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "08:00",
        "closes": "17:00",
        "validFrom": "2026-11-01",
        "validThrough": "2027-04-30",
    },
}


def seo_head(title: str, description: str, canonical_path: str, schema_extra: list | None = None) -> str:
    url = SITE + canonical_path
    schemas = schema_extra or []
    if not schemas and canonical_path in ("/", "/school/"):
        schemas = [LOCAL_BUSINESS]
    schema_blocks = ""
    for s in schemas:
        schema_blocks += f'\n  <script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
    return f"""  <link rel="canonical" href="{url}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/og-default.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Freediver on the line in Unawatuna, Sri Lanka">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:site_name" content="Lanka Freediving">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="robots" content="max-image-preview:large">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="sitemap" type="application/xml" href="/sitemap.xml">{schema_blocks}
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-LDYRTZ7WJS"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag("js", new Date());
    gtag("config", "G-LDYRTZ7WJS");
  </script>
  <script defer data-domain="lankafreediving.com" src="https://plausible.io/js/script.js"></script>"""


def inject_seo(html: str, title: str, description: str, canonical_path: str, schema_extra: list | None = None) -> str:
    og_type_m = re.search(r'<meta property="og:type" content="([^"]*)"', html)
    og_type = og_type_m.group(1) if og_type_m else "website"
    block = seo_head(title, description, canonical_path, schema_extra)
    html = re.sub(
        r"</title>\s*(?:<link rel=\"canonical\"[^>]*>\s*)?(?:<meta[^>]*>\s*)*(?:<script[^>]*>.*?</script>\s*)*(?=<link rel=\"preconnect\"|<meta name=\"description\")",
        f"</title>\n  <meta name=\"description\" content=\"{description}\">\n  <meta property=\"og:title\" content=\"{title}\">\n  <meta property=\"og:description\" content=\"{description}\">\n  <meta property=\"og:type\" content=\"{og_type}\">\n{block}\n  ",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(r'\n  <meta name="description" content="[^"]*">\n  <meta property="og:title"[^>]*>\n  <meta property="og:description"[^>]*>\n  <meta property="og:type"[^>]*>\n', "\n  ", html)
    html = re.sub(r'<meta property="og:url" content="[^"]*">\n?', "", html)
    return html


def add_guides_nav(html: str, depth: int) -> str:
    guides_href = "../" * depth + "guides/"
    if "href=\"" + guides_href + "\"" in html or '>Guides<' in html:
        return html
    html = html.replace(
        '<li><a href="../faq/"',
        NAV_GUIDES.format(guides_href=guides_href) + '\n        <li><a href="../faq/"',
        1,
    )
    html = html.replace(
        '<li><a href="faq/"',
        NAV_GUIDES.format(guides_href="guides/") + '\n        <li><a href="faq/"',
        1,
    )
    html = html.replace(
        '<li><a href="../faq/">FAQ</a></li>\n        <li><a href="../contact/',
        '<li><a href="../faq/">FAQ</a></li>\n' + FOOTER_EXTRA.format(guides_href=guides_href) + '\n        <li><a href="../contact/',
        1,
    )
    html = html.replace(
        '<li><a href="faq/">FAQ</a></li>\n        <li><a href="contact/',
        '<li><a href="faq/">FAQ</a></li>\n' + FOOTER_EXTRA.format(guides_href="guides/") + '\n        <li><a href="contact/',
        1,
    )
    return html


def add_scripts(html: str, depth: int) -> str:
    prefix = "../" * depth
    cfg = f'  <script src="{prefix}site-config.js"></script>\n'
    if "site-config.js" not in html:
        html = html.replace(
            f'  <script src="{prefix}site.js"></script>',
            cfg + f'  <script src="{prefix}site.js"></script>',
        )
    return html


def guide_page(g: dict) -> str:
    slug = g["slug"]
    canonical = f"/guides/{slug}/"
    url = SITE + canonical
    related_html = "".join(
        f'<li><a href="../{s}/">{next(x["title"] for x in GUIDES if x["slug"] == s)}</a></li>'
        for s in g["related"]
    )
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": g["title"],
            "description": g["description"],
            "url": url,
            "datePublished": TODAY,
            "dateModified": TODAY,
            "author": {"@type": "Person", "name": "Julian", "jobTitle": "Molchanovs Instructor"},
            "publisher": {"@type": "Organization", "name": "Lanka Freediving", "url": SITE},
            "image": f"{SITE}/assets/{g['image'][0]}",
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE + "/guides/"},
                {"@type": "ListItem", "position": 3, "name": g["title"], "item": url},
            ],
        },
    ]
    seo_title, seo_desc = GUIDE_SEO.get(g["slug"], (g["title"], g["description"]))
    head = seo_head(seo_title, seo_desc, canonical, schema)
    img_path, img_alt = g["image"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{seo_title}</title>
  <meta name="description" content="{seo_desc}">
  <meta property="og:title" content="{seo_title}">
  <meta property="og:description" content="{seo_desc}">
  <meta property="og:type" content="article">
{head}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Bowlby+One+SC&family=Work+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../styles.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
{SVG_SYMBOLS}

  <header class="site-header pair-cream">
    <nav class="nav" aria-label="Primary">
      <a class="logo-mark" href="../../">
        <img src="../../../assets/logo.png" width="1024" height="1024" alt="Lanka Freediving">
      </a>
      <button class="nav-toggle" id="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-menu" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav-menu" id="nav-menu">
        <li><a href="../../courses/">Courses</a></li>
        <li><a href="../../retreat/">Retreat</a></li>
        <li><a href="../../expedition/">Expedition</a></li>
        <li><a href="../../school/">The School</a></li>
        <li><a href="../" aria-current="page">Guides</a></li>
        <li><a href="../../faq/">FAQ</a></li>
        <li><a href="../../contact/" class="nav-cta">Get in touch</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section class="panel {g["hero_pair"]} reveal">
      <p class="caption">{g["caption"]}</p>
      <h1 class="hero-title">{g["h1"]}</h1>
      <p class="hero-sub">{g["subtitle"]}</p>
    </section>
    <section class="panel pair-cream reveal guide-body">
      <figure class="guide-figure">
        <img src="../../../assets/{img_path}" alt="{img_alt}" loading="lazy">
      </figure>
      {g["body"].strip()}
      <h2>Related guides</h2>
      <ul class="plain">{related_html}</ul>
      <p style="margin-top:1.5rem"><a class="btn btn-solid" href="../../courses/">View courses</a> <a class="btn" href="../../contact/">Get in touch</a></p>
    </section>
  </main>

  <footer class="panel pair-ink site-footer">
    <div class="footer-grid">
      <ul class="footer-links">
        <li><a href="../../courses/">Courses</a></li>
        <li><a href="../../retreat/">Retreat</a></li>
        <li><a href="../../expedition/">Expedition</a></li>
        <li><a href="../../school/">The School</a></li>
        <li><a href="../">Guides</a></li>
        <li><a href="../../faq/">FAQ</a></li>
        <li><a href="../../contact/">Get in touch</a></li>
      </ul>
      <div>
        <p class="caption">Open November – April · Unawatuna, Sri Lanka</p>
        <p><a href="mailto:hello@lankafreediving.com" data-lf-email>hello@lankafreediving.com</a></p>
        <p class="caption" style="margin-top:0.8rem">© Lanka Freediving</p>
      </div>
    </div>
  </footer>
{WA_SVG}
  <script src="../../site-config.js"></script>
  <script src="../../site.js"></script>
</body>
</html>
"""


def guides_index() -> str:
    cards = ""
    for g in GUIDES:
        cards += f"""
        <article class="guide-card reveal">
          <h2><a href="{g["slug"]}/">{g["title"]}</a></h2>
          <p>{g["description"]}</p>
          <p><a class="btn" href="{g["slug"]}/">Read guide</a></p>
        </article>"""
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Sri Lanka & Unawatuna Guides",
            "url": SITE + "/guides/",
            "description": "Travel and freediving guides for Sri Lanka's south coast and Unawatuna.",
        }
    ]
    head = seo_head(
        "Sri Lanka Freediving & Unawatuna Guides | Lanka Freediving",
        "When to go, how to get there, course comparisons, and a 7-day south-coast itinerary — written from a Molchanovs school in Unawatuna.",
        "/guides/",
        schema,
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sri Lanka Freediving & Unawatuna Guides | Lanka Freediving</title>
  <meta name="description" content="When to go, how to get there, course comparisons, and a 7-day south-coast itinerary — written from a Molchanovs school in Unawatuna.">
  <meta property="og:title" content="Sri Lanka Freediving & Unawatuna Guides | Lanka Freediving">
  <meta property="og:description" content="When to go, how to get there, course comparisons, and a 7-day south-coast itinerary — written from a Molchanovs school in Unawatuna.">
  <meta property="og:type" content="website">
{head}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Bowlby+One+SC&family=Work+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
{SVG_SYMBOLS}

  <header class="site-header pair-cream">
    <nav class="nav" aria-label="Primary">
      <a class="logo-mark" href="../">
        <img src="../../assets/logo.png" width="1024" height="1024" alt="Lanka Freediving">
      </a>
      <button class="nav-toggle" id="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-menu" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav-menu" id="nav-menu">
        <li><a href="../courses/">Courses</a></li>
        <li><a href="../retreat/">Retreat</a></li>
        <li><a href="../expedition/">Expedition</a></li>
        <li><a href="../school/">The School</a></li>
        <li><a href="./" aria-current="page">Guides</a></li>
        <li><a href="../faq/">FAQ</a></li>
        <li><a href="../contact/" class="nav-cta">Get in touch</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section class="panel pair-red reveal">
      <p class="caption">Guides</p>
      <h1 class="hero-title">Plan the trip. Then go deeper.</h1>
      <p class="hero-sub">South coast travel, freediving in Unawatuna, and itineraries — written from the water.</p>
    </section>
    <section class="panel pair-cream reveal">
      <div class="guide-grid">{cards}
      </div>
    </section>
  </main>

  <footer class="panel pair-ink site-footer">
    <div class="footer-grid">
      <ul class="footer-links">
        <li><a href="../courses/">Courses</a></li>
        <li><a href="../retreat/">Retreat</a></li>
        <li><a href="../expedition/">Expedition</a></li>
        <li><a href="../school/">The School</a></li>
        <li><a href="./">Guides</a></li>
        <li><a href="../faq/">FAQ</a></li>
        <li><a href="../contact/">Get in touch</a></li>
      </ul>
      <div>
        <p class="caption">Open November – April · Unawatuna, Sri Lanka</p>
        <p><a href="mailto:hello@lankafreediving.com" data-lf-email>hello@lankafreediving.com</a></p>
        <p class="caption" style="margin-top:0.8rem">© Lanka Freediving</p>
      </div>
    </div>
  </footer>
{WA_SVG}
  <script src="../site-config.js"></script>
  <script src="../site.js"></script>
</body>
</html>
"""


def faq_schema() -> dict:
    faq_path = SLEEVE / "faq" / "index.html"
    text = faq_path.read_text()
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


def courses_schema() -> list:
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


def write_sitemap() -> None:
    urls = []
    for rel, meta in PAGES.items():
        urls.append((meta["path"], meta["priority"]))
    urls.append(("/guides/", "0.85"))
    for g in GUIDES:
        urls.append((f'/guides/{g["slug"]}/', "0.75"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for path, pri in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE}{path}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{'weekly' if path == '/' else 'monthly'}</changefreq>")
        lines.append(f"    <priority>{pri}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (PUBLIC / "sitemap.xml").write_text("\n".join(lines) + "\n")


def write_llms() -> None:
    (PUBLIC / "llms.txt").write_text(textwrap.dedent(f"""\
        # Lanka Freediving

        > Molchanovs freediving school in Unawatuna, Sri Lanka. Small groups, warm water, November–April.

        Lanka Freediving teaches Molchanovs freediving courses on Sri Lanka's south coast. Maximum four students per course. Instructor Julian is a Molchanovs instructor and competition safety diver.

        ## Season
        - Open: November through April (dry season, south coast)
        - Closed: May through October

        ## Location
        - Unawatuna, Southern Province, Sri Lanka
        - 15 minutes from Galle Fort, ~2.5 hours from Colombo airport

        ## Services
        - Discover Freediving (half day, €120)
        - Molchanovs Wave 1 (3 days, €350)
        - Molchanovs Wave 2 (4 days, €450)
        - 5-day freediving retreat (from €900)
        - Expeditions including Batanta Island with Salty Tracks

        ## Contact
        - Email: hello@lankafreediving.com
        - Website contact form: {SITE}/contact/
        - WhatsApp: available on website

        ## Key pages
        - Home: {SITE}/
        - Courses: {SITE}/courses/
        - Retreat: {SITE}/retreat/
        - School: {SITE}/school/
        - FAQ: {SITE}/faq/
        - Guides: {SITE}/guides/
        - Contact: {SITE}/contact/

        ## Extended facts
        See {SITE}/llms-full.txt
    """))

    (PUBLIC / "llms-full.txt").write_text(textwrap.dedent(f"""\
        Lanka Freediving — extended reference (for AI assistants and search)

        ENTITY
        Name: Lanka Freediving
        Type: Molchanovs freediving school / SportsActivityLocation
        URL: {SITE}
        Email: hello@lankafreediving.com
        Location: Unawatuna, Galle district, Southern Province, Sri Lanka
        Coordinates (approximate): 6.0144, 80.2489
        Season: November 1 – April 30 (courses and open water)
        Group size: Maximum 4 students per course; retreat up to 8 guests

        INSTRUCTOR
        Julian — Molchanovs instructor, Evolution Spearfishing instructor, certified competition safety diver.

        COURSES AND PRICING (EUR, 2026)
        Discover Freediving: half day, €120, no certification, max 4 students
        Molchanovs Wave 1: 3 days, €350, certification to 12–20 m, swim 200 m required
        Molchanovs Wave 2: 4 days, €450, certification to 24–30 m, Wave 1 prerequisite
        Wave 2+ / advanced coaching: flexible, price on request
        5-day retreat: from €900, includes accommodation (TBC hotel), meals, daily sessions, Wave 1 or 2 certification

        WHAT IS INCLUDED (typical Wave course)
        Online theory and exam, pool sessions, open water sessions, boat access, all equipment, underwater photos.
        Accommodation and meals not included in standard course price (included in retreat).

        BOOKING
        Contact via website form, WhatsApp, or hello@lankafreediving.com
        Confirmation within 24 hours
        Deposit: 30% courses, 50% retreat/expedition
        Balance due day one
        Cancellation: >14 days full deposit refund; within 14 days transfer same season; weather cancellations rescheduled or refunded

        CONDITIONS
        Water temperature: 27–30°C in season
        Visibility: often 15 m+ on calm mornings
        Terrain: reef, sand, blue water short boat ride from Unawatuna

        NEARBY TRAVEL
        Galle Fort (15 min), Mirissa whales (Dec–Apr), Weligama surf, Koggala lake, Jungle Beach

        GUIDES (organic content)
        {chr(10).join(f"        {SITE}/guides/{g['slug']}/" for g in GUIDES)}
    """))


def generate_images() -> None:
    try:
        from PIL import Image
    except ImportError:
        print("Pillow not installed — skip image generation")
        return
    logo = ASSETS / "logo.png"
    hero = ASSETS / "photos" / "session-sun.jpg"
    if logo.exists():
        img = Image.open(logo).convert("RGBA")
        img = img.resize((64, 64), Image.Resampling.LANCZOS)
        bg = Image.new("RGBA", (64, 64), (255, 255, 255, 255))
        bg.paste(img, (0, 0), img)
        bg.convert("RGB").save(PUBLIC / "favicon.ico", format="ICO", sizes=[(64, 64)])
        print("wrote favicon.ico")
    if hero.exists() and not (ASSETS / "og-default.jpg").exists():
        img = Image.open(hero).convert("RGB")
        w, h = img.size
        target = 630 / 1200
        if h / w > target:
            nh = int(w * target)
            top = (h - nh) // 2
            img = img.crop((0, top, w, top + nh))
        else:
            nw = int(h / target)
            left = (w - nw) // 2
            img = img.crop((left, 0, left + nw, h))
        img = img.resize((1200, 630), Image.Resampling.LANCZOS)
        out = ASSETS / "og-default.jpg"
        img.save(out, quality=88)
        print("wrote og-default.jpg")


def patch_pages() -> None:
    guides_dir = SLEEVE / "guides"
    guides_dir.mkdir(exist_ok=True)
    (guides_dir / "index.html").write_text(guides_index())
    for g in GUIDES:
        d = guides_dir / g["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(guide_page(g))
        print("guide", g["slug"])

    for rel, meta in PAGES.items():
        path = SLEEVE / rel
        html = path.read_text()
        title_m = re.search(r"<title>(.*?)</title>", html)
        desc_m = re.search(r'<meta name="description" content="(.*?)"', html)
        title = title_m.group(1) if title_m else "Lanka Freediving"
        desc = desc_m.group(1) if desc_m else ""
        depth = 0 if rel == "index.html" else 1
        schema = None
        if rel == "faq/index.html":
            schema = [faq_schema()]
        elif rel == "courses/index.html":
            schema = courses_schema()
        elif rel in ("index.html", "school/index.html"):
            schema = [LOCAL_BUSINESS]
        html = inject_seo(html, title, desc, meta["path"], schema)
        html = add_guides_nav(html, depth)
        html = add_scripts(html, depth)
        path.write_text(html)
        print("patched", rel)


def add_home_guide_cards() -> None:
    path = SLEEVE / "index.html"
    html = path.read_text()
    if "guide-teasers" in html:
        return
    block = """
    <section class="panel pair-cream reveal" id="guides" aria-labelledby="guides-label">
      <p class="section-label reveal" id="guides-label">Guides</p>
      <h2 class="tease-title reveal">Plan your south coast trip</h2>
      <div class="guide-teasers reveal">
        <p><a href="guides/molchanovs-vs-padi-sri-lanka/">Molchanovs vs PADI in Sri Lanka</a></p>
        <p><a href="guides/first-freedive-unawatuna/">Your first freedive in Unawatuna</a></p>
        <p><a href="guides/freediving-course-cost-sri-lanka/">How much a course costs</a></p>
        <p style="margin-top:1rem"><a class="btn" href="guides/">All guides</a></p>
      </div>
    </section>
"""
    html = html.replace(
        '<section class="panel pair-red" aria-labelledby="see-you-title">',
        block + '\n    <section class="panel pair-red" aria-labelledby="see-you-title">',
        1,
    )
    path.write_text(html)
    print("home guide teasers")


def add_internal_links() -> None:
    links = {
        "school/index.html": '<p class="hero-sub">Small groups, serious instruction, warm water. Unawatuna, November to April.</p>\n      <p><a href="../guides/freediving-unawatuna/">Freediving in Unawatuna</a> · <a href="../guides/best-time-freediving-sri-lanka/">Best season</a></p>',
        "courses/index.html": '<p class="hero-sub">Theory, pool, and open water. Small groups, real certification, no rush.</p>\n      <p><a href="../guides/molchanovs-courses-explained/">Which Molchanovs course?</a></p>',
        "retreat/index.html": '<p class="hero-sub">Five days of freediving and breathwork. Max 8 guests. Boutique hotel in Unawatuna. From €900.</p>\n      <p><a href="../guides/south-coast-7-day-itinerary/">7-day south coast itinerary</a></p>',
    }
    for rel, snippet in links.items():
        path = SLEEVE / rel
        html = path.read_text()
        if "guides/" in html.split("<main")[1][:800]:
            continue
        old = snippet.split("\n")[0]
        if old in html:
            html = html.replace(old, snippet, 1)
            path.write_text(html)
            print("internal link", rel)


def main() -> None:
    PUBLIC.mkdir(exist_ok=True)
    generate_images()
    write_sitemap()
    write_llms()
    patch_pages()
    add_home_guide_cards()
    add_internal_links()
    print("done")


if __name__ == "__main__":
    main()
