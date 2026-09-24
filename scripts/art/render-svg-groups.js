/**
 * Renderiza cada grupo de primer nivel de un fondo SVG (sky, far, mid…) por separado,
 * con fondo transparente, más la composición completa ("flat").
 * Uso: NODE_PATH=$(npm root -g) node scripts/art/render-svg-groups.js fondo.svg carpeta/ 2 3
 * Necesita playwright (lo usa render_layers.py).
 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const [, , file, outDir, ...scales] = process.argv;
  const svg = fs.readFileSync(file, "utf8");
  const browser = await chromium.launch();
  for (const scale of scales.map(Number)) {
    const page = await browser.newPage({ viewport: { width: 390, height: 560 }, deviceScaleFactor: scale });
    await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    const ids = await page.evaluate(() => [...document.querySelector("svg").children].filter((c) => c.tagName === "g").map((g) => g.id));
    const shoot = async (name) => page.locator("svg").screenshot({ path: path.join(outDir, `${name}@${scale}x.png`), omitBackground: true });
    await shoot("flat");
    for (const id of ids) {
      await page.evaluate((only) => {
        for (const g of document.querySelector("svg").children) if (g.tagName === "g") g.style.display = g.id === only ? "" : "none";
      }, id);
      await shoot(id);
    }
    await page.close();
    fs.writeFileSync(path.join(outDir, "groups.json"), JSON.stringify(ids));
  }
  await browser.close();
})();
