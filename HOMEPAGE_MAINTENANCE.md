# Mingjun Wang Homepage Maintenance Guide

This document explains how the homepage is organized, how each file is used, and how to update, preview, debug, and deploy the site.

## 1. Repository Purpose

This repository is the editable GitHub Pages source. Its preferred public address is:

```text
https://wang-mingjun.github.io/
```

The same content remains available at `https://xin-xi-xiao.github.io/`; its generated canonical link points search engines to the preferred address above.

The site is a pure static, single-page academic homepage. It is written in a jemdoc-like source file and rendered to plain HTML, so GitHub Pages can serve it directly without a build server.

## 2. Important Paths

```text
/data0/wangmingjun_homepage/
├── index.jemdoc              # Main editable homepage source
├── index.html                # Generated homepage served by GitHub Pages
├── assets/
│   ├── main.css              # All visual styling and responsive layout rules
│   ├── photo.jpg             # Processed portrait used in the hero area
│   ├── brand-mark-512.png    # Normalized high-resolution WM brand mark
│   ├── brand-mark-128.png    # Lightweight navigation brand mark
│   ├── favicon-48.png        # Google Search-sized round favicon
│   ├── favicon-32.png        # Browser-tab icon
│   ├── icon-192.png          # High-density browser/device icon
│   ├── apple-touch-icon.png  # iOS home-screen icon
│   ├── cuhk.png              # CUHK logo
│   ├── ict.svg               # ICT/CAS logo
│   ├── pku.png               # Peking University logo
│   └── cv.pdf                # Public CV downloaded from the homepage
├── favicon.png                # Stable round favicon URL for Google Search
├── tools/
│   └── render_jemdoc.py      # Renderer: converts index.jemdoc to index.html
├── README.md                 # Short repository overview
├── design_analysis.md        # Design rationale based on Bei Yu and Yao Lai pages
└── HOMEPAGE_MAINTENANCE.md   # This maintenance guide
```

## 3. What To Edit

Edit `index.jemdoc` for content:

- Hero name, title, tagline, bio, links
- About section
- News entries
- Research interest cards
- Education rows
- Selected Publications
- Research Experience
- Honors & Awards
- Leadership & Service
- Skills
- Contact and footer

Edit `assets/main.css` for appearance:

- Page width, fonts, colors, spacing
- Portrait size and shape
- Logo alignment
- Publication cards
- Awards table
- Mobile responsive behavior

Edit `tools/render_jemdoc.py` only when changing generated HTML structure, metadata, or how jemdoc blocks are converted.

Do not edit `index.html` by hand. It is generated from `index.jemdoc`.

## 4. Current Content Rules

The homepage intentionally includes only accepted or publicly verifiable academic content.

Keep:

- Accepted conference papers
- Accepted journal papers
- Publicly visible Early Access journal papers
- Confirmed awards, education, service, skills, and project experience

Exclude:

- Patents
- Under-review papers
- Manuscripts not yet accepted
- Duplicate awards
- Overly promotional claims not supported by the CV or public sources

## 5. Current Research Narrative

The homepage foregrounds:

```text
AI4EDA · 3D IC Design Automation · Circuit Representation Learning · Fault Simulation
```

The intended emphasis is:

1. AI4EDA
2. 3D IC design automation and industrial-grade 3D IC EDA design flows
3. Circuit representation learning and multi-modal circuit data
4. Fault simulation and functional safety

Fault simulation remains visible because it is an important foundation in the publication record and industry/research experience. The site now presents it as a strong supporting thread rather than the only central identity.

## 6. CV PDF Policy

The public CV is stored at the stable path:

```text
assets/cv.pdf
```

The CV links and buttons point to this path. Keep the filename unchanged when replacing the PDF.

To publish or update the CV:

```bash
cd /data0/wangmingjun_homepage
cp "/path/to/latest_cv.pdf" assets/cv.pdf
python3 tools/render_jemdoc.py index.jemdoc
git add -A
git commit -m "docs: update public cv"
git push -u origin main
```

Use the exact filename `cv.pdf` so the existing links continue to work.

If the browser still opens an older CV after deployment, add a cache version in `index.jemdoc`, for example:

```html
href="assets/cv.pdf?v=20260601"
```

Then rebuild and push.

## 7. Image and Logo Updates

Personal brand mark:

```text
assets/brand-mark-512.png
assets/brand-mark-128.png
assets/favicon-48.png
assets/favicon-32.png
assets/icon-192.png
assets/apple-touch-icon.png
favicon.png
```

The 512 px file is the normalized square master. The 128 px file is displayed beside the name in the sticky navigation. The round `favicon.png` is the stable Google Search and browser identity, while the 48/32/180/192 px variants serve individual browser and device surfaces. Keep the visible navigation mark at approximately 28 px so it supports the name without competing with the portrait. When replacing the artwork, regenerate all variants from the same square crop, keep the root `favicon.png` path unchanged, update the cache version for the smaller variants in `tools/render_jemdoc.py`, and rebuild `index.html`.

Portrait:

```text
assets/photo.jpg
```

The current portrait is displayed as a compact rounded rectangle, not a circle. The CSS class is:

```css
.portrait-card
```

Affiliation logos:

```text
assets/cuhk.png
assets/ict.svg
assets/pku.png
```

The hero-area logos are wrapped in equal-size `.logo-frame` boxes so that CUHK, ICT/CAS, and PKU align visually even if the source image canvases differ.

If replacing a logo, keep the filename unchanged or update both `index.jemdoc` and any relevant documentation.

## 8. Publication Updates

Each publication card is in `index.jemdoc` inside:

```html
<section id="publications">
```

Each paper should include:

- Venue badge, such as `ICML 2025` or `IEEE TCAD 2025`
- Type badge: `Conference` or `Journal`
- Title
- Authors, with `<strong>Mingjun Wang</strong>`
- Metadata line starting with `Conference paper · ...` or `Journal article · ...`
- Short factual description
- Public links when available

For co-first-author papers, use:

```html
<span class="award-badge">Co-first †</span>
```

and keep the note:

```text
† Equal contribution.
```

Recommended publication ordering:

1. Year descending
2. Within the same year, first-author/co-first AI4EDA and 3D IC papers first
3. Journal papers remain clearly visible, especially IEEE TCAD
4. Fault simulation and functional-safety papers remain included as the foundation thread

## 9. Award Updates

Awards are in `index.jemdoc` inside:

```html
<section id="awards">
```

Use the table columns:

```text
Award | Venue / Organization | Year
```

Recommended ordering:

1. Year descending
2. Within the same year, public EDA/AI competition awards first
3. Scholarships and institutional awards after competition awards
4. Avoid duplicates

The EDA² Integrated Circuit Elite Challenge 2023 award should appear only once.

## 10. Research Experience Ordering

Research Experience is ordered to support the current academic identity:

1. AI4EDA, multi-modal circuit data, and 3D IC EDA flow automation
2. Fault Simulation Research at ICT/CAS
3. Industrial Experience at CASTEST
4. PKU undergraduate thesis

The required fixed date corrections are:

```text
Fault Simulation Research: Jul. 2023 — Mar. 2025
Industrial Experience:     Sep. 2021 — Jan. 2025
```

## 11. Build

Render the homepage:

```bash
cd /data0/wangmingjun_homepage
python3 tools/render_jemdoc.py index.jemdoc
```

Expected output:

```text
generated index.html
```

## 12. Local Preview

Start a local static server:

```bash
cd /data0/wangmingjun_homepage
python3 -m http.server 8000
```

Open:

```text
http://127.0.0.1:8000/
```

Check at least:

- Desktop width
- Tablet width
- Mobile width around 375px
- Hero portrait shape and logo alignment
- Navigation anchors
- Publication labels: Conference / Journal
- CV link behavior
- Research Experience dates

Stop the server with `Ctrl+C`.

## 13. Debug Checklist

If content changes do not appear:

1. Rebuild with `python3 tools/render_jemdoc.py index.jemdoc`.
2. Hard refresh the browser.
3. If CSS or images are cached, update the query string in `index.jemdoc`, for example:

```text
assets/main.css?v=20260528e
assets/photo.jpg?v=20260528e
```

If the portrait becomes circular again:

1. Check `assets/main.css`.
2. Confirm `.portrait-card` has `border-radius: var(--radius-card) !important;`.
3. Confirm there is no old inline style such as `border-radius:50%`.
4. Rebuild `index.html`.

If logos look inconsistent:

1. Check the hero logo HTML uses `.logo-frame`.
2. Check `.logo-frame` has fixed width and height.
3. Check `.logo-frame img` uses `max-width` and `max-height`, not custom per-logo widths.

If GitHub Pages does not update:

1. Confirm changes are committed and pushed to `main`.
2. Wait one or two minutes for GitHub Pages to rebuild.
3. Open the browser in a private window or hard refresh.
4. Check repository settings: Pages should serve from the root of the `main` branch.

## 14. Deployment

After editing:

```bash
cd /data0/wangmingjun_homepage
python3 tools/render_jemdoc.py index.jemdoc
git status
git add -A
git commit -m "fix: refine homepage layout and research narrative"
git push -u origin main
```

After pushing, visit the preferred public address:

```text
https://wang-mingjun.github.io/
```

## 14.1 Google Search Console

The canonical address to add as a URL-prefix property is:

```text
https://wang-mingjun.github.io/
```

The root-level file `googleeb48c6bcf48b80a4.html` is a Google **HTML file** verification file, not an HTML-tag verification snippet. Keep its filename and one-line content exactly unchanged. After it is committed and the mirror deployment finishes, verify that this URL opens as plain text:

```text
https://wang-mingjun.github.io/googleeb48c6bcf48b80a4.html
```

In Search Console, choose **HTML file** for this supplied file. If you instead choose **HTML tag**, Google will give you a different `<meta name="google-site-verification" ...>` value; add that exact tag to `tools/render_jemdoc.py` before the canonical link, rebuild, and deploy.

After verification, use **URL inspection** for `https://wang-mingjun.github.io/` and select **Request indexing**. The repository also publishes `robots.txt` and `sitemap.xml`, both of which identify the same canonical URL. Requesting indexing asks Google to crawl the page; it does not guarantee an immediate ranking or inclusion.

## 15. Recommended Update Workflow

For normal content updates:

```bash
cd /data0/wangmingjun_homepage
git pull --ff-only
edit index.jemdoc
python3 tools/render_jemdoc.py index.jemdoc
python3 -m http.server 8000
git status
git add -A
git commit -m "docs: update homepage content"
git push -u origin main
```

For style-only updates:

```bash
edit assets/main.css
python3 tools/render_jemdoc.py index.jemdoc
git add -A
git commit -m "style: refine homepage layout"
git push -u origin main
```

For CV updates:

```bash
cp "/path/to/latest_cv.pdf" assets/cv.pdf
python3 tools/render_jemdoc.py index.jemdoc
git add -A
git commit -m "docs: update public cv"
git push -u origin main
```

## 16. Final Quality Checklist

Before pushing, confirm:

- `index.html` is regenerated.
- Portrait is rectangular and compact.
- Hero logos are visually aligned.
- AI4EDA and 3D IC design automation are prominent.
- Industrial-grade 3D IC EDA flow appears in the research narrative.
- Fault simulation remains visible.
- ICT/CAS education lists Prof. Xiaowei Li and Prof. Huawei Li.
- Publications have Conference or Journal labels.
- No patents or under-review papers are included.
- Awards contain no duplicate EDA² 2023 item.
- Research Experience dates are correct.
- The latest public CV is placed at `assets/cv.pdf` and its cache version is updated in `index.jemdoc`.
- `git status` is clean after commit.

## 17. Alternate Address and Domain Migration

### 17.1 How a `github.io` address is assigned

A GitHub user or organization homepage must be owned by an account whose name matches the repository and hostname. For example:

```text
GitHub owner: MingjunWang
Repository:   MingjunWang.github.io
Website:      https://mingjunwang.github.io/
```

Creating a repository named `mingjunwang.github.io` under `xin-xi-xiao` would not claim that hostname. It would only create a project site under the `xin-xi-xiao.github.io` namespace.

As checked on 2026-07-14, `MingjunWang` is already an existing GitHub personal account, while `https://mingjunwang.github.io/` returns 404 because that account has no public `MingjunWang.github.io` repository. If this account belongs to the site owner, sign in to it and create the public repository `MingjunWang.github.io`. If it belongs to someone else, GitHub will not allow another user or organization to claim the same case-insensitive name.

### 17.2 Recommended option: one canonical custom domain

For a durable academic identity, use one personally owned domain as the canonical address and keep GitHub Pages as the hosting platform. The recommended name is:

```text
https://mingjunwang.com/
```

It is the full English name, contains no hyphen or affiliation, is easy to cite in papers and slides, and remains suitable after graduation or a change of institution. An authoritative RDAP lookup returned no registration record for `mingjunwang.com` on 2026-07-14. This is a point-in-time technical check, not a reservation: availability and price must still be confirmed at a registrar and the domain should be purchased before any repository or DNS change.

Other RDAP results from the same check:

| Domain | Result on 2026-07-14 | Assessment |
| --- | --- | --- |
| `mingjunwang.com` | No registration record found | Best choice; verify and register first |
| `mingjunwang.me` | No registration record found | Good personal-site fallback |
| `mingjunwang.dev` | No registration record found | Technical, but less neutral than `.com` |
| `mingjunwang.io` | No registration record found | Usually more expensive; less personal |
| `mingjunwang.ai` | No registration record found | Relevant today, but ties the identity to one field |
| `mjwang.com` | Registered | Not available through normal registration |
| `mingjun.wang` | Registered | Not available through normal registration |

The intended final URL behavior is:

```text
https://mingjunwang.com/       canonical homepage
https://www.mingjunwang.com/   redirects to the canonical homepage
https://xin-xi-xiao.github.io/ redirects to the canonical homepage
```

After buying the domain:

1. In GitHub account settings, open **Pages** and verify the domain with the TXT record GitHub provides.
2. In `xin-xi-xiao/xin-xi-xiao.github.io`, open **Settings > Pages** and enter the custom domain.
3. Configure these DNS records at the registrar:

```text
Type    Name    Value
A       @       185.199.108.153
A       @       185.199.109.153
A       @       185.199.110.153
A       @       185.199.111.153
CNAME   www     xin-xi-xiao.github.io
```

The four addresses above are GitHub's documented Pages IPv4 records as checked on 2026-07-14. Recheck the official GitHub documentation before applying them in the future. Do not use a wildcard DNS record.

4. Keep the verification TXT record and enable **Enforce HTTPS** after the certificate is ready.
5. If Pages publishes from a branch, retain the generated root-level `CNAME` file in Git.
6. Rebuild metadata with the final canonical URL, commit, and push:

```bash
cd /data0/wangmingjun_homepage
HOMEPAGE_URL=https://mingjunwang.com/ python3 tools/render_jemdoc.py index.jemdoc
git add index.html CNAME
git commit -m "feat: use custom homepage domain"
git push -u origin main
```

Only run this after the domain is owned, verified, and saved in the repository's Pages settings. Once configured, GitHub Pages redirects the default `github.io` address to the custom domain, so there is only one public canonical copy to maintain.

### 17.3 Alternative: migrate to `mingjunwang.github.io`

Use this route only if the existing `MingjunWang` GitHub account belongs to the site owner and access has been recovered.

1. Sign in to `MingjunWang` and create a public repository named `MingjunWang.github.io`.
2. Add `xin-xi-xiao` as a collaborator, or configure a separate SSH key/token for `MingjunWang`.
3. Add the repository as a temporary remote and test access:

```bash
cd /data0/wangmingjun_homepage
git remote add new-home https://github.com/MingjunWang/MingjunWang.github.io.git
git ls-remote new-home
```

4. Rebuild the metadata for the new primary address and push:

```bash
HOMEPAGE_URL=https://mingjunwang.github.io/ python3 tools/render_jemdoc.py index.jemdoc
git add index.html
git commit -m "feat: migrate canonical homepage address"
git push new-home main
```

5. Verify the new Pages deployment before changing the old site. After verification, replace the old site with a simple permanent redirect to the new address, or keep the old content temporarily with its canonical link pointing to `https://mingjunwang.github.io/`.
6. Choose one repository as the only editable source. Do not independently edit two full copies, because they will drift over time.

### 17.4 Name-only `github.io` alternatives

GitHub user and organization names are case-insensitive. The following namespace check was performed through GitHub's public API on 2026-07-14:

| Desired address | Required owner | Result |
| --- | --- | --- |
| `mingjunwang.github.io` | `MingjunWang` | Occupied by an existing personal account; usable only if it belongs to the site owner |
| `mjwang.github.io` | `mjwang` | Occupied |
| `mj-wang.github.io` | `mj-wang` | Occupied |
| `mingjun-wang.github.io` | `mingjun-wang` | Occupied |
| `wangmingjun.github.io` | `wangmingjun` | Occupied |
| `wang-mingjun.github.io` | `wang-mingjun` | No public account found at check time |
| `mingjun-w.github.io` | `mingjun-w` | No public account found at check time |
| `m-j-wang.github.io` | `m-j-wang` | No public account found at check time |

An API 404 means that no public account was found at that moment; it does not reserve the name and does not guarantee that GitHub will accept it during organization creation. The final check occurs in GitHub's **New organization** form.

If a free `github.io` address is required, the preferred available-looking option is `wang-mingjun.github.io` because it preserves the full name and avoids field or institution suffixes. Create an organization named `wang-mingjun` while signed in as `xin-xi-xiao`, then create its public repository `wang-mingjun.github.io`. The source repository now includes an optional one-way synchronization workflow; follow `HOMEPAGE_MIRROR_SETUP.md` to configure it without changing the existing Pages site.

### 17.5 Renderer URL control

`tools/render_jemdoc.py` reads the optional `HOMEPAGE_URL` environment variable and uses it for:

- `<link rel="canonical">`
- `og:url`
- the absolute `og:image` URL

Without the variable, it safely defaults to:

```text
https://wang-mingjun.github.io/
```

Only HTTPS absolute URLs are accepted. This prevents an accidental malformed canonical address from being published.
