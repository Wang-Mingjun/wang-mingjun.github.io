// Optional browser QA. Install playwright and @axe-core/playwright outside the repo.
const { chromium } = require('playwright');
const { default: AxeBuilder } = require('@axe-core/playwright');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

(async () => {
  const output = process.argv[2] || '/tmp/mingjun-homepage-qa';
  const url = process.argv[3] || pathToFileURL(path.resolve(__dirname, '../index.html')).href;
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const reports = [];
  try {
    for (const width of [320, 375, 768, 1440]) {
      const context = await browser.newContext({ viewport: { width, height: 960 } });
      const page = await context.newPage();
      const failures = [];
      page.on('pageerror', error => failures.push(error.message));
      page.on('requestfailed', request => failures.push(request.url()));
      await page.goto(url, { waitUntil: 'networkidle' });
      await page.screenshot({ path: path.join(output, `home-${width}.png`) });
      const layout = await page.evaluate(() => {
        const portrait = document.querySelector('.portrait-card');
        return {
          overflow: document.documentElement.scrollWidth > innerWidth,
          images: [...document.images].every(img => img.complete && img.naturalWidth > 0),
          portraitRadius: getComputedStyle(portrait).borderRadius,
          portraitWidth: portrait.getBoundingClientRect().width,
          publicationBorders: [...document.querySelectorAll('.pub-card')].every(card => {
            const style = getComputedStyle(card);
            return style.borderLeftWidth === style.borderRightWidth && style.borderLeftColor === style.borderRightColor;
          }),
          textOverflow: [...document.querySelectorAll('h1, h2, h3, p, .skill-items, td, th')]
            .filter(el => el.scrollWidth > el.clientWidth + 1).map(el => el.textContent.slice(0, 100)),
        };
      });
      const accessibility = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
      await page.locator('.nav-links a[href="#publications"]').click();
      await page.waitForTimeout(700);
      const anchorTop = await page.locator('#publications').evaluate(el => el.getBoundingClientRect().top);
      const navBottom = await page.locator('.topbar').evaluate(el => el.getBoundingClientRect().bottom);
      await page.screenshot({ path: path.join(output, `publications-${width}.png`) });
      await page.locator('#skills').scrollIntoViewIfNeeded();
      await page.screenshot({ path: path.join(output, `skills-${width}.png`) });
      const report = { width, layout, failures, anchorClear: anchorTop >= navBottom - 1,
        violations: accessibility.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target) })) };
      reports.push(report);
      await context.close();
    }
  } finally {
    await browser.close();
  }
  fs.writeFileSync(path.join(output, 'layout-report.json'), JSON.stringify(reports, null, 2));
  console.log(JSON.stringify(reports, null, 2));
  if (reports.some(r => r.layout.overflow || !r.layout.images || !r.layout.publicationBorders || r.layout.textOverflow.length || r.failures.length || !r.anchorClear || r.violations.length)) {
    process.exitCode = 1;
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
