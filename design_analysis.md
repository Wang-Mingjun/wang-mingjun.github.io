# Design Analysis

This note records the reference-page analysis used to redesign Mingjun Wang's academic homepage.

## Bei Yu Homepage

| Design Element | Observation |
|---|---|
| Navigation | Traditional jemdoc side navigation, organized by identity and research categories. Links are compact, text-first, and highly scannable. |
| Hero layout | Photo and profile text are placed side by side in a table-like layout. The profile block prioritizes title, department, university, degrees, social links, and CV. |
| Section titles | Blue academic headings with simple horizontal separation. The visual system is restrained and information-driven. |
| About text | Dense academic prose with many contextual links. Paragraphs use a readable line height and compact spacing. |
| News / updates | The site favors dated, factual update lists. Content is precise, chronological, and easy to skim. |
| Awards / records | Information is best represented as compact tabular or list structures rather than decorative cards. |
| Color palette | Navy/blue links and headings, black text, white background, light gray separators. |
| Typography | Jemdoc-style academic typography, with compact body text and restrained headings. |

## Yao Lai Homepage

| Design Element | Observation |
|---|---|
| Navigation | Minimal sticky top navigation with a very small set of links. It uses subtle shadow/border and modern spacing. |
| Hero layout | A modern card-like profile area with text on the left and image on the right. Affiliation logo and CV/contact links are prominent but not oversized. |
| Education / honors | Uses compact rows with institution logos, degree text, and right-aligned dates. |
| Publication cards | Publications are card-based, with a left thumbnail/venue block and a right content area containing venue badge, title, authors, status badges, description, and links. |
| Typography | Modern sans-serif, body around 15-16px, compact headings around 18-20px, strong use of metadata styling. |
| Whitespace | Card spacing and section spacing create breathing room without wasting the page. |
| Color palette | Clean white background, deep blue links, small colorful venue badges, light gray borders. |

## Fusion Strategy

Mingjun Wang's homepage should combine Bei Yu's rigorous academic organization with Yao Lai's modern visual hierarchy. The redesign therefore uses:

- A compact sticky top navigation.
- A profile header with a compact rounded-rectangle portrait, visually balanced affiliation-logo frames, CV and scholar links.
- Bei Yu-style chronological News and awards table.
- Yao Lai-style education rows and publication cards.
- A narrow 960px container, 15px body text, and 22px section headings.
- No decorative numbering, no oversized typography, and no patent or under-review content.

## Second-Pass Refinement

- The profile image is displayed as a rounded-rectangle portrait rather than a circular crop. The supplied certificate-style photo is already tightly framed, so a circle enlarges the face too much and removes useful context.
- Publications are ordered by year first, then by author contribution and relevance to the research narrative. First-author and co-first AI4EDA papers lead the 2026 group, while the IEEE TCAD Early Access paper remains clearly visible in the same year group.
- Awards are ordered by year and then by public research/competition signal before scholarships. The duplicate EDA2/EDA² 2023 award from the CV is represented once.
- Each publication card explicitly marks whether the entry is a journal article or a conference paper, because the selected list mixes TCAD journal papers with conference papers.
- The CSS file is versioned in the generated HTML to avoid old GitHub Pages/browser caches preserving the previous circular portrait rule.
- The hero, research cards, publication ordering, and research-experience order now foreground AI4EDA and 3D IC design automation as the primary research identity. Industrial-grade 3D IC EDA design flow is included as a recurring but not overbearing theme, while circuit representation learning and fault simulation remain explicit, visible research threads.

## July 2026 Refinement

- Publications are grouped by year to make the expanded record easier to scan without splitting the single-page structure.
- Within each year, first-author papers appear first, followed by co-first-author work and other collaborations. All publication cards use the same border treatment so author contribution is conveyed by ordering and bolded names rather than decorative lines.
- Newly accepted ICCAD 2026 papers use a small accepted-status badge; unavailable paper links are intentionally omitted until public records exist.
- Hover feedback, tabular date numerals, reduced-motion support, canonical metadata, and social-preview metadata improve polish and accessibility without changing the academic character.
