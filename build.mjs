// Builds preview.html (a complete standalone page) from highlevel-paste-ready.html.
// Usage: node build.mjs
// Edit highlevel-paste-ready.html, then run this so both files stay identical.

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const component = readFileSync(join(here, 'highlevel-paste-ready.html'), 'utf8').trim();

const page = `<!doctype html>
<!--
  GENERATED FILE. Do not edit by hand.
  Edit highlevel-paste-ready.html, then run: node build.mjs

  Standalone page: use it to preview the design, or host it on a website
  outside HighLevel (where External Tracking is designed to work).
-->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="format-detection" content="telephone=no">
  <meta name="theme-color" content="#FBF7F1">

  <!-- REPLACE: WEBINAR TITLE (browser tab and link previews) -->
  <title>Free Live Training for Beauty Professionals | Rie Artistry</title>
  <meta name="description" content="You’re good at what you do. Now let’s build the business around it. A free live training with Cherie Bowen of Rie Artistry, Sunday, October 18, 2026 at 7 PM Eastern.">

  <!-- Link preview when the page is shared in Instagram DMs and other apps. -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="You’re good at what you do. Now let’s build the business around it.">
  <meta property="og:description" content="Sunday, October 18, 2026 at 7 PM Eastern. Hosted by Cherie Bowen of Rie Artistry.">
  <!-- REPLACE: SHARE IMAGE URL (1200 x 630 works best), then uncomment. -->
  <!-- <meta property="og:image" content="https://YOUR-IMAGE-URL.jpg"> -->

  <!-- Keeps the preview out of search results. Remove this line when the page goes live. -->
  <meta name="robots" content="noindex, nofollow">

  <!-- ==============================================================
       REPLACE: HIGHLEVEL EXTERNAL TRACKING SCRIPT
       In HighLevel: Settings > External Tracking > Copy Script.
       Paste it on the line below, exactly as copied. Do not change
       its tracking ID. Paste it only once.
       ============================================================== -->

  <!-- ============ END HIGHLEVEL EXTERNAL TRACKING SCRIPT ============ -->

  <style>
    html { -webkit-text-size-adjust: 100%; }
    html, body { margin: 0; padding: 0; background: #FBF7F1; }
    html { scroll-behavior: smooth; }
    @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
  </style>
</head>
<body>
<main>
${component}
</main>
</body>
</html>
`;

writeFileSync(join(here, 'preview.html'), page);
console.log('Wrote preview.html');
