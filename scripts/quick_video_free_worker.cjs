#!/usr/bin/env node
'use strict';
// OPS-007: Zero-API, zero-server browser worker for a *real* sample WEBM.
// Chromium mobile emulation is NOT a real Android device and cannot unlock Android QA.
const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');
const { chromium } = require('playwright');

const OUT = path.resolve('runtime/free-video-worker');
const PORT = 38219;
const HOST = 'http://127.0.0.1:' + PORT;
const PAGES_URL = 'https://mbcarbody-cmd.github.io/ai-business-factory/website/';
fs.mkdirSync(OUT, { recursive: true });

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
async function available(url) {
  for (let attempt = 0; attempt < 25; attempt++) {
    try { const r = await fetch(url, {signal: AbortSignal.timeout(1500)}); if (r.ok) return; }
    catch (_) {}
    await sleep(300);
  }
  throw new Error('Local product server did not start');
}
async function getPublicStatus(pageName) {
  try {
    const res = await fetch(PAGES_URL + pageName, { redirect: 'follow', signal: AbortSignal.timeout(12000) });
    return {page: pageName, status: res.status, live: res.ok};
  } catch (e) {
    return {page: pageName, status: 'connection error', live: false};
  }
}
function reportMarkdown(r) {
  const line = (label, val) => '- ' + label + ': ' + val + '\n';
  return '# Nemokamas video agentas — ' + r.createdAt + '\n\n'
    + line('Rezultatas', r.status)
    + line('Bandomasis WEBM', r.videoBytes ? r.videoBytes + ' baitų' : 'nesukurtas')
    + line('Video failas', r.videoFile || 'nėra')
    + line('Vykdymas', 'GitHub Actions / Playwright Chromium (mobiliojo ekrano emuliacija)')
    + line('Android įrenginio QA', 'NEPATVIRTINTA — tikras telefonas nebuvo testuotas')
    + line('Tikri klientai', 'neieškoti ir nepatvirtinti')
    + line('Gauti mokėjimai', '0 EUR patvirtinta šiame procese')
    + line('AI API', 'nenaudojamas; jokių API raktų')
    + '\n## Viešos svetainės patikrinimas\n\n'
    + (r.publicPages||[]).map(p=>line(p.page, String(p.status))).join('')
    + '\n## Kitas veiksmas\n\n'
    + (r.status === 'PASS' 
       ? 'Bandomasis video sugeneruotas tikrame naršyklės variklyje. Toliau būtinas realaus Android Chrome įrenginio pilnas produkto įkėlimo, renderio, atkūrimo ir atsisiuntimo QA. Tik po to galima svarstyti prekybą.\n'
       : 'Patikrinti nesėkmę GitHub Actions loguose ir pridedamame ekrano vaizde; jokio pardavimo, kol neveikia renderis.\n')
    + (r.error ? '\nKlaida: ' + r.error + '\n' : '');
}

async function main() {
  const r = {
    createdAt: new Date().toISOString(), status: 'FAIL',
    videoBytes: 0, publicPages: [], videoFile: null, error: null,
    androidQaApproved: false, confirmedRevenueEur: 0, modelApiCalls: 0
  };
  let browser, server, page;
  try {
    server = spawn('python3', ['-m','http.server', String(PORT), '--bind','127.0.0.1'], { stdio: 'ignore' });
    await available(HOST + '/website/video-maker.html');
    browser = await chromium.launch({ headless: true, args: ['--autoplay-policy=no-user-gesture-required'] });
    const context = await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1,acceptDownloads:true});
    page = await context.newPage();
    const jsErrors = [];
    page.on('pageerror', err => jsErrors.push(String(err)));
    await page.goto(HOST + '/website/video-maker.html', {waitUntil:'domcontentloaded'});
    await page.waitForFunction(() => typeof renderVideo === 'function', null, {timeout:15000});
    const fixture = await page.evaluate(() => {
      const c = document.createElement('canvas'); c.width = 900; c.height = 1200;
      const g = c.getContext('2d'); let seed = 2468;
      const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
      g.fillStyle = '#263447'; g.fillRect(0,0,c.width,c.height);
      for (let i=0;i<2700;i++){
        g.fillStyle = 'hsl(' + (180+Math.floor(rnd()*115)) + ' 50% ' + (20+Math.floor(rnd()*55)) + '%)';
        g.fillRect(rnd()*900,rnd()*1200,8+rnd()*30,8+rnd()*30);
      }
      g.fillStyle = '#eee'; g.font = 'bold 76px sans-serif'; g.fillText('VIDEO DEMO', 90, 550);
      return c.toDataURL('image/png').split(',')[1];
    });
    await page.locator('#photos').setInputFiles({name:'synthetic-test-photo.png', mimeType:'image/png', buffer:Buffer.from(fixture, 'base64')});
    await page.waitForFunction(() => state.media.length === 1, null, {timeout:15000});
    await page.locator('#brand').fill('DEMO');
    await page.locator('#headline').fill('Tikras video renderio bandymas');
    await page.locator('#subline').fill('Patikrinimas be mokamo AI API');
    await page.locator('#cta').fill('Peržiūrėti');
    await page.locator('#soundtrack').selectOption('none');
    await page.locator('#duration').selectOption('6');
    await page.locator('#render').click();
    await page.locator('#result').waitFor({state:'visible', timeout:55000});
    await page.locator('#download').waitFor({state:'visible',timeout:4000});
    await page.evaluate(() => document.querySelector('#video').load());
    await page.waitForFunction(() => document.querySelector('#video').readyState >= 2, null, {timeout:15000});
    const proof = await page.evaluate(() => JSON.parse(localStorage.getItem('studioVideoLastRenderProof')||'null'));
    if (!proof || proof.bytes < 270000 || proof.mediaCount !== 1 || proof.durationSeconds !== 6) {
      throw new Error('WebM proof is missing or failed video size / photo / duration gate');
    }
    const pending = page.waitForEvent('download',{timeout:12000});
    await page.locator('#download').click();
    const download = await pending;
    const demo = path.join(OUT,'synthetic-demo.webm');
    await download.saveAs(demo);
    const bytes = fs.statSync(demo).size;
    if (bytes < 270000) throw new Error('WEBM file too small: '+bytes);
    if (fs.readFileSync(demo).subarray(0,4).toString('hex') !== '1a45dfa3') {
      throw new Error('Downloaded file has no EBML/WebM header');
    }
    if (jsErrors.length) throw new Error('Javascript errors: '+jsErrors.slice(0,2).join('; '));
    r.status = 'PASS'; r.videoBytes = bytes; r.videoFile = 'synthetic-demo.webm';
    r.browserProof = proof;
    await page.screenshot({path:path.join(OUT,'render-screenshot.png'),fullPage:true});
  } catch(e) {
    r.error = String(e && e.message || e);
    if (page) {
      try { await page.screenshot({path:path.join(OUT,'failure-screenshot.png'),fullPage:true}); } catch (_) {}
    }
  } finally {
    try {if (browser) await browser.close();} catch (_) {}
    try {if (server) server.kill();} catch (_) {}
  }
  r.publicPages = await Promise.all(['video-maker.html','video-maker-android-qa.html','quick-video-paid-order.html'].map(getPublicStatus));
  fs.writeFileSync(path.join(OUT,'proof.json'), JSON.stringify(r,null,2)+'\n','utf8');
  fs.writeFileSync(path.join(OUT,'REPORT.md'), reportMarkdown(r),'utf8');
  console.log(JSON.stringify({status:r.status,videoBytes:r.videoBytes,publicPages:r.publicPages,error:r.error},null,2));
  if (r.status !== 'PASS') process.exitCode = 1;
}
main().catch(error => { console.error(error); process.exitCode = 1; });
