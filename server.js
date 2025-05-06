const express = require('express');
const puppeteer = require('puppeteer-core');
const chrome = require('chrome-aws-lambda');

const app = express();
const port = process.env.PORT || 3000;

app.get('/get-video-url', async (req, res) => {
  const { websiteId, playerType } = req.query;

  // Glitch platformunda Chromium çalıştırmak için
  let browser;
  try {
    browser = await puppeteer.launch({
      executablePath: await chrome.executablePath || '/usr/bin/chromium-browser',
      headless: chrome.headless,
      args: chrome.args,
      defaultViewport: chrome.defaultViewport,
    });

    const page = await browser.newPage();
    
    // ATV canlı yayınına git
    await page.goto("https://www.atv.com.tr/canli-yayin", { waitUntil: 'networkidle0' });

    // Ağdan m3u8 linki yakalamak
    const videoUrl = await new Promise((resolve) => {
      page.on('response', async (response) => {
        const url = response.url();
        if (url.includes('.m3u8')) {
          resolve(url);
        }
      });
    });

    res.json({ videoUrl });

  } catch (error) {
    console.error('Error during puppeteer launch:', error);
    res.status(500).send('Something went wrong');
  } finally {
    if (browser) {
      await browser.close();
    }
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
