# IBO Mixed Farm Ltd — Website

Static website for **IBO Mixed Farm Ltd**, Bwizibwera, Rwanyamahembe Sub-county,
Mbarara, Uganda. Built by Bbotica Company Limited (Code & Build) under agreement
ref **BBC-IBO-WSM-2026-004**.

Seven pages, no framework, no database, no build dependencies beyond Python.
Uploads to any host — shared hosting, Netlify, Vercel, GitHub Pages, cPanel.

---

## Contents

- [Running it locally](#running-it-locally)
- [Editing the site](#editing-the-site)
- [Before launch — the must-do list](#before-launch--the-must-do-list)
- [Content still needed from the farm](#content-still-needed-from-the-farm)
- [Replacing the placeholder images](#replacing-the-placeholder-images)
- [Where the content came from](#where-the-content-came-from)
- [Design notes](#design-notes)
- [Scope check against the agreement](#scope-check-against-the-agreement)

---

## Running it locally

```bash
python -m http.server 8123
```

Then open <http://localhost:8123>. Opening the `.html` files directly with
`file://` also works, but a server is closer to production.

---

## Editing the site

Page content lives in **`src/`**. The shared header, navigation, footer,
`<head>` and structured data live in **`build.py`**. Running the build stitches
them together and writes the finished pages to the project root.

```bash
python build.py
```

```
src/index.html      →  index.html
src/about.html      →  about.html
src/training.html   →  training.html
src/services.html   →  services.html
src/gallery.html    →  gallery.html
src/journal.html    →  journal.html
src/contact.html    →  contact.html
                    →  sitemap.xml, robots.txt   (generated)
```

**Edit `src/`, not the root files** — the root files are overwritten on every
build.

Each source file starts with a small metadata block that supplies the page
title, meta description and Open Graph title:

```html
<!--META {
  "title": "…",
  "description": "…",
  "og_title": "…"
} -->
```

Adding a page means: create `src/newpage.html` with a META block, add it to the
`NAV` list near the top of `build.py`, and rebuild. Navigation, the mobile
drawer, the sitemap and the "current page" highlight all follow automatically.

### Files

```
├── build.py              Build script — also holds the shared header/footer
├── src/                  Page content (edit here)
├── assets/
│   ├── css/style.css     All styling, one file, tokens at the top
│   ├── js/main.js        All behaviour, one file, contact details at the top
│   └── img/              Real farm photographs, the logo and partner logos
│                         (a few specific subjects still open — see below)
├── *.html                Generated output (do not edit by hand)
├── sitemap.xml           Generated
└── robots.txt            Generated
```

---

## Before launch — the must-do list

**Target launch date: 15 August 2026** (the client asked for Assumption Day).
Final approval on design and content rests with the Managing Director.


These are the items that must be settled before the site goes live. Everything
marked **TODO** is a placeholder deliberately left visible so it cannot be
missed.

| # | Item | Status | Where |
|---|------|--------|-------|
| 1 | **Phone / WhatsApp number.** Currently `+256 700 000 000`. The number on the farm's exhibition banner was not legible in the photographs supplied. | Still open | `assets/js/main.js` → `IBO.WHATSAPP` and `IBO.PHONE_DISPLAY` |
| 2 | **Domain.** The site is written against `https://www.ibomixfarm.com`. Confirm the final domain and update. | Still open | `build.py` → `SITE_URL` |
| 3 | **Logo.** ~~A green circle marked "IBO" stands in for the real logo.~~ | **Done** — real logo now in the header, footer and favicon | `assets/img/ibo-logo.png` |
| 4 | **Photographs.** ~~Every image is a blank placeholder.~~ | **Mostly done** — real farm photographs throughout; a handful of specific subjects are still open, see below | throughout |
| 5 | **Social links.** ~~Facebook, Instagram, YouTube and X icons point at `#`.~~ | **Mostly done** — Facebook, Instagram, X and TikTok now link to the real accounts; YouTube still pending | `build.py` → `FOOTER` |
| 6 | **Exact map pin.** The map is centred on Bwizibwera. Set the precise pin once the Google Business Profile is verified. | Still open | `src/contact.html` |
| 7 | **Where enquiries go.** See the note on forms below. | Still open | `assets/js/main.js` → `FORM_ENDPOINT` |
| 8 | **Fee inclusions.** UGX 400,000 per month is stated as all-inclusive; confirm exactly what that covers. | Still open | `src/training.html` |

### How the forms work right now

The brief was *"start with enquiries"*, so nothing on this site takes a payment
and nothing is stored on a server. When a visitor submits a form, the browser
assembles their answers into one readable message and opens either **WhatsApp**
or **email** prefilled with it — the visitor chooses which. The Director
receives a complete, structured enquiry either way, and there is no backend to
host, secure or pay for.

To move to a hosted form service later (Formspree, Basin, Netlify Forms), set
`FORM_ENDPOINT` in `assets/js/main.js` to the endpoint URL. The existing
handler will POST to it and fall back to WhatsApp/email if the request fails.

---

## Content still needed from the farm

Drawn from the four unanswered questions in the information-gathering sheet, and
from answers that pointed at documents rather than content.

- [ ] **Phone number(s)** for the farm — the single highest-priority gap.
- [ ] **Testimonials.** Q46 and Q67 confirm these exist. One placeholder quote
      sits on the home page waiting for a real one.
- [ ] **Success stories.** Q40: *"Innocent to share a list with Remy."*
- [ ] **The printed course outline / brochure** (Q54, Q68) — to confirm the exact
      course names and durations, and to upload as a PDF download on the
      training page.
- [ ] **Certificates** (Q34, Q76) — scans of the UVTAB accreditation and company
      registration for the credentials section.
- [x] ~~**Partner logos** (Q77)~~ — done. Ten real, linked partner logos now
      appear on the About page and the homepage.
- [ ] **Milestone dates.** The About timeline has the sequence of events but not
      the years for each. Confirm with the Director.
- [ ] **Impact numbers** (Q39). The sheet's own note asks: how many jobs created,
      how many trainees now employed or self-employed? Real figures here would
      be the strongest credibility content on the site.
- [ ] **Individual portraits** of Dr. Innocent Arinaitwe, Betty Arinaitwe and
      Olla Allan. Several group photos were supplied, but nobody in them is
      identified, so the three bios still show a blank photo slot rather than
      risk mislabelling someone. A close, individual photo of each person
      (with a name attached) resolves this immediately.
- [ ] **Four more specific photographs** the supplied batch didn't cover, now
      that everything else has a real photo: a plant clinic / disease-diagnosis
      session in progress, soil sampling or testing being carried out, a farm
      layout sketch or aerial view of the blocks, and a value-addition /
      processing activity (packaging, bottling, etc.).
- [ ] **Named awards, certificates or press mentions** from the last few
      quarters — useful for the content-calendar "achievement spotlight" posts,
      which currently draw only on figures already published on the site.
- [ ] **Style references** (Q47, unanswered) — if the Director has sites he likes,
      the look can still be adjusted.
- [ ] **Competitor sites** (Q75, unanswered) — useful for the SEO work.
- [ ] **Prerequisites for trainees** (Q64, unanswered) — what to bring.

Nothing on the site invents facts to fill these gaps. Where information is
missing it either says so plainly or the section is written so it reads
correctly without it.

---

## Replacing the placeholder images

Most of this section is now done — real photographs are wired in throughout
the site. What follows is how it works, for the handful of slots still open
and for anything added later.

A remaining placeholder is a `div` with class `ph`, not an `<img>`, so there
are no broken-image icons anywhere. Each one carries a `data-label` describing
exactly which photograph belongs there:

```html
<div class="ph ph--4x5" data-label="Photo — trainees working in the nursery"></div>
```

To use a real photograph, put the file in `assets/img/` and swap the div for an
image, keeping the aspect-ratio class on a wrapper if you want the layout to
hold its shape:

```html
<div class="photo-frame ph--4x5">
  <img src="assets/img/farm/nursery-trainees.jpg"
       alt="Trainees preparing corms in the macro-propagation nursery"
       loading="lazy">
</div>
```

Aspect-ratio helpers available: `ph--16x9`, `ph--3x2`, `ph--4x5`, `ph--1x1`,
`ph--tall`, `ph--wide`, plus `ph--flush` (no border/radius, for images that sit
flush inside a card) and `ph--round`.

**Always write a real `alt` description** — it matters for accessibility and for
Google Images, which is a genuine traffic source for a farm.

### What's still open

Every generic placeholder (plantation, coffee garden, nursery, livestock,
training sessions, farm events) now has a real photograph. What's still
blank, and why:

- **The three founder/co-founder portraits** (Dr. Innocent Arinaitwe, Betty
  Arinaitwe, Olla Allan) — group photos exist, but nobody in them is labelled,
  so a guess would risk misidentifying someone. Needs one individual, named
  photo per person.
- **Plant clinic / disease diagnosis**, **soil sampling or testing**, **a farm
  layout sketch or aerial view**, and **value addition / processing** — the
  photo batch supplied didn't include any of these four subjects, and nothing
  in stock photo libraries could stand in without either misrepresenting the
  farm or showing someone who isn't the farm's own staff. Real photos of any
  of these close the last gaps.

Full credits for the small number of licensed stock photos used elsewhere
(clearly marked, and never for the farm's own staff or events) are in
`assets/img/gallery/CREDITS.md` and `assets/img/farm/CREDITS.md`.

---

## Where the content came from

Every factual claim on the site traces to one of these:

1. **The information-gathering sheet** (`IBO_Website_Info_Gathering_Info.xlsx`,
   80 of 84 questions answered) — land breakdown, capacities, training format,
   fees, partner list, governance, registration numbers.
2. **The farm's own exhibition banners**, read from the supplied photographs —
   the company name `IBO MIXED FARM LTD`, the tagline *"Optimum Utilization of
   Land"*, the location line, the email address, and the SAY/SKY project skilling
   components (crop managers, plant doctors, pasture establishment and
   management, plant clinic operation).
3. **Public sources** — MAAIF confirmed IBO Mixed Farm's location in Bwizibwera,
   Mbarara City and its NAADS support; New Vision reported 121 youth trained
   under the AVSI SKY project (77 crop managers, 44 plant doctors).
4. **The service agreement** — the Director's name and title, and the agreed
   scope.

Where a number in the sheet needed interpretation it has been handled
conservatively. The 900-acre livestock area, for instance, sits outside IBO and
belongs to the family; the site refers to "the adjoining family holding" and
quotes the herd numbers without claiming the acreage as IBO's own.

---

## Design notes

The two reference sites the client pointed at — rondrisofarms.ca and
winterspringcsa.com — share a pattern: a warm cream page, a single deep accent
colour, generous photography, and short conversational copy that leads to one
obvious action. Both open with the family story before they sell anything.

That is the structure used here, mapped onto IBO's own brand colours (green,
gold/orange and black, taken from the logo) and onto IBO's stated priority: the
sheet is unambiguous that **booking a training is the single most important
action** on the site. So the training CTA appears in the sticky header on every
page, in the hero, in the top bar, in the mobile drawer, and in two full
sections of the home page.

Where it departs from the references: those two farms sell produce to consumers,
IBO sells expertise to farmers and institutions. So the numbers do more work
here — acreage, capacity, trainee counts, accreditation — because credibility is
what an NGO or a district farmers' association is looking for before they place
a cohort.

- **Type:** Fraunces (serif) for headings, Inter for body. Warm but not rustic.
- **Colour:** `--green-900` through `--green-500` for structure, `--gold-500` for
  action, cream and sand for the page. All tokens are at the top of `style.css`.
- **Motion:** a single fade-and-rise on scroll, disabled under
  `prefers-reduced-motion`.
- **Accessibility:** skip link, visible focus rings, labelled form fields,
  `aria-current` on the active nav item, real landmark elements, and no text on
  a background it cannot be read against.
- **Performance:** two CSS/JS files, no images, no framework. The whole site is
  a few hundred kilobytes.

Responsive from 320px up. Tested at 375px and 1280px.

---

## Scope check against the agreement

Clause 4.1 of BBC-IBO-WSM-2026-004 lists eight website deliverables:

| Deliverable | Status |
|---|---|
| Mobile-first responsive site, up to 7 core pages | Done — 7 pages |
| Enquiry/contact form, click-to-call, WhatsApp button | Done — 4 forms, click-to-call, floating WhatsApp on every page |
| Photo and video gallery | Photos done and filterable; video section awaiting the YouTube channel |
| Basic on-page SEO | Done — titles, descriptions, canonicals, Open Graph, JSON-LD, sitemap, robots.txt, semantic headings |
| Google Analytics + Search Console | Not done — needs accounts and the live domain |
| Verified Google Business Profile | Not done — needs the farm's phone number and verification |
| SSL + enquiry routing | Not done — host-level, at deployment |
| Hand-over session and user guide | This document is the written guide |

The last four are deployment-time tasks that need the domain, hosting and phone
number to exist first.

---

*Bbotica Company Limited — Code & Build.*
