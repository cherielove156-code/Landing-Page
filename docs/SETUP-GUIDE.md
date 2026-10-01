# Setup Guide: Webinar Landing Page + Registration Form

This guide covers placing the page, replacing the placeholders, and connecting the custom form to HighLevel afterward. It does not cover building the email or SMS automations.

## 1. What is in this folder

| File | What it is |
|---|---|
| `highlevel-paste-ready.html` | The page and form as one block of scoped CSS, HTML, and a small script. Paste it into a HighLevel **Custom JS/HTML** element. This is the file to edit. |
| `preview.html` | A complete standalone page built from the file above. Open it in a browser to preview, or host it on a website outside HighLevel. It has a marked spot in `<head>` for the External Tracking script. |
| `build.mjs` | Regenerates `preview.html` after you edit the paste-ready file: `node build.mjs`. |
| `docs/LAUNCH-CHECKLIST.md` | Tests to run before you share the link. |

All CSS is scoped to `#rie-webinar`, so it will not restyle anything else on a HighLevel page. Nothing is saved in the browser, and the script sends no data anywhere on its own.

## 2. Replace the placeholders

Search `highlevel-paste-ready.html` for `REPLACE:`. Then run `node build.mjs` so `preview.html` matches.

| Placeholder | Where | Notes |
|---|---|---|
| Webinar title (done) | Hero `<h1>`, `<title>` in `build.mjs` | Confirmed: "You’re good at what you do. Now let’s build the business around it." In HighLevel, use it as the page title in the page SEO settings too. |
| `REPLACE: HERO PHOTO URL` | Hero `<img src="...">` | Already set to `images/cherie-bowen-hero.jpg`, which works in `preview.html`. **In HighLevel**, upload that file to Media Storage and paste its URL into `src`. |
| `REPLACE: ABOUT PHOTO URL` | About `<img src="...">` | Already set to `images/cherie-bowen-about.jpg`. **In HighLevel**, upload it and paste its URL the same way. |
| `REPLACE: PRIVACY POLICY URL` | Two `href="privacy-policy.html"` links | Draft page is in `legal/privacy-policy-paste-ready.html`. Fill in its highlighted details, publish it as its own HighLevel page, then put that page's URL in both links. |
| `REPLACE: TERMS URL` | Two `href="terms.html"` links | Same steps with `legal/terms-paste-ready.html`. The two legal pages also link to each other and back to the training page, so update those links too. |
| `REPLACE: SMS DISCLOSURES` | The two text-message consent paragraphs | Draft wording only. Have it reviewed, and make sure it matches your A2P 10DLC campaign registration. |
| `REPLACE: THANK-YOU PAGE URL` | `data-thank-you-url=""` on `#rie-webinar` | Optional. Used only in live mode. |
| `REPLACE: TESTIMONIAL IMAGE URLS` | "What my mentees say" section after "About" | Cropped message screenshots with no names showing (`images/testimonial-1.webp` to `-4.webp`). **In HighLevel**, upload them and paste each URL into `src`. Each image's `alt` text is a word-for-word transcription for screen readers. |
| Footer disclosure | Last footer paragraph | A suggested results disclaimer. Edit or remove it to match your own legal guidance. |

**Photos in HighLevel:** upload them to **Media Storage**, copy each file's URL, and paste it into `src`.

## 3. How the hosting choice affects the connection

> **Source note:** this environment's network policy blocked `help.gohighlevel.com`, so the HighLevel article ([Tracking External Forms with HighLevel](https://help.gohighlevel.com/support/solutions/articles/155000006092)) could not be opened directly. The points below come from search results quoting that article. Read the current article once before you connect, in case anything has changed.

What the article says External Tracking needs and does:

- A **lightweight script unique to your account**, copied from **Settings → External Tracking → Copy Script**. It goes before the closing `</head>` tag, loads on every page, and its tracking ID must not be changed.
- Forms must be **real HTML `<form>` elements rendered directly in the page (the DOM)**, with **visible inputs that have `name` attributes** and an **email field**.
- **Not supported:** forms inside **iframes**, pop-up widgets without real form elements, and third-party scripts that do not expose their inputs.
- On submission, a contact is **created or updated**, and earlier anonymous page views are linked to that contact.
- Workflows can use the **Form Submitted** trigger, with filters including **domain, page path, external form name, and UTM parameters**. The form's `id`/`name` is picked up as the form name.

This form meets those requirements. It is a real `<form>` with `id` and `name` set to `rie-webinar-registration`, every input is visible and named, the email field is `name="email"`, and it sits directly in the page DOM with no iframe.

### Option A: host the page outside HighLevel (the documented use case)

External Tracking is built for websites that are not hosted on HighLevel, such as WordPress, Shopify, Wix, Squarespace, or a static host like Netlify.

1. Use `preview.html` as the page, or paste the contents of `highlevel-paste-ready.html` into a custom HTML block on your site.
2. Paste your External Tracking script into the marked spot in `<head>`, or into your site builder's site-wide header code setting. Paste it once.
3. Run the launch checklist.

### Option B: host it on a HighLevel funnel or website page (Custom JS/HTML element)

This is what `highlevel-paste-ready.html` is formatted for. One caution: HighLevel documents External Tracking for **external** websites. A custom HTML form inside a HighLevel-hosted page is not the use case the article describes. Treat it as something to **prove with test submissions before you promote the page**, not something to assume.

1. Create the page in **Sites → Funnels** (or Websites). Add a **full-width section** with one row and one column, and set section, row, and column padding to 0 so the design runs edge to edge.
2. Add a **Custom JS/HTML** element to that column and paste the entire contents of `highlevel-paste-ready.html`. Save.
3. Paste your External Tracking script into the page's (or funnel's) **Tracking Code → Head** setting. Do not paste it inside the Custom JS/HTML element, and paste it only once.
4. Set the page title, description, and social image in the page's SEO/meta settings. The `<head>` tags in `preview.html` do not carry over into HighLevel.
5. Publish to a URL you have not shared yet. On the live URL, right-click the form and choose **Inspect**. Confirm the `<form id="rie-webinar-registration">` is **not** inside an `<iframe>`. The Custom JS/HTML element normally renders straight into the page, but check.
6. Run the launch checklist. If test submissions do not create contacts, use one of the supported alternatives below. Do not launch the page and hope.

### If External Tracking does not suit your setup: supported alternatives (not built yet)

These are documented here only. None of them is built in this task.

1. **A new native HighLevel form (simplest on a HighLevel page).** Build a new form in **Sites → Forms → Builder** with the same fields, names, dropdown options, and separate consent checkboxes, and place it with the funnel's Form element. Native forms create contacts and fire the **Form Submitted** trigger without External Tracking. The trade-off is less design control: you style it with HighLevel's form styling options plus custom CSS instead of this custom form.
2. **Inbound Webhook workflow trigger.** A workflow starting with **Inbound Webhook** gives you a URL that accepts posted form data. The form script would need a small change to send the fields to that URL, and the workflow would then **Create/Update Contact** from the payload. Note that the webhook URL is visible in the page source, so plan for spam. Check your plan includes this trigger.
3. **HighLevel API through your own server.** Most control, but it needs a backend and an API key kept on a server. Out of scope for now, and no credentials are needed for this design stage.

## 4. Connect the form in HighLevel (after the page is placed)

### 4a. Create custom fields first

**Settings → Custom Fields** (labels are suggestions; keep the values exactly as listed):

| Form input `name` | HighLevel field | Suggested type | Values the form sends |
|---|---|---|---|
| `first_name` | First Name (standard) | n/a | text |
| `email` | Email (standard) | n/a | email |
| `phone` | Phone (standard) | n/a | as typed, e.g. `(555) 123-4567` |
| `beauty_industry` | Beauty Industry (custom) | Dropdown (single) or Single line | `Lash artist`, `Brow artist`, `Hairstylist`, `Makeup artist`, `Nail technician`, `Esthetician or skincare professional`, `Permanent makeup artist`, `Other` |
| `beauty_industry_other` | Beauty Industry Other (custom) | Single line | text; sent only when `Other` is chosen |
| `sms_webinar_reminders` | Webinar SMS Reminders Consent (custom) | Single line, or Checkbox with option `Yes` | `Yes` when checked; **not sent at all** when unchecked |
| `sms_promotional` | Promotional SMS Consent (custom) | Single line, or Checkbox with option `Yes` | `Yes` when checked; not sent when unchecked |
| `email_marketing` | Email Marketing Consent (custom) | Single line, or Checkbox with option `Yes` | `Yes` when checked; not sent when unchecked |

If you use a Dropdown for Beauty Industry, the option text must match the values above character for character.

Unchecked boxes send nothing, which is standard HTML behavior. In your workflows, treat **"is not `Yes`" (empty)** as **no consent**.

### 4b. Install the tracking script

Use Option A or B above. The page view should show in External Tracking analytics shortly after you load the page.

### 4c. Send one test submission and map fields

Submit the form once with test data. Open the new contact and look at the form submission details. External Tracking maps fields automatically. For any value that shows in the submission but not in your custom field, use the field-mapping options HighLevel shows for External Tracking. If none are offered, add an **Update Contact Field** step in the workflow to copy it.

### 4d. Workflow trigger (registration entry point)

**Automation → Workflows → New workflow → Add trigger: Form Submitted**, then add filters:

- External form name = `rie-webinar-registration`
- Domain and/or page path = your landing page, so a future form elsewhere cannot trigger it

Then plan your branches. You will build these later, not now:

- **Every registrant:** webinar emails (confirmation and how to join).
- **Only if** Webinar SMS Reminders Consent = `Yes`: webinar reminder texts.
- **Only if** Promotional SMS Consent = `Yes`: marketing texts.
- **Only if** Email Marketing Consent = `Yes`: ongoing marketing emails.

## 5. Preview mode and going live

The `#rie-webinar` element carries the settings:

```html
<div id="rie-webinar" data-mode="preview" data-thank-you-url="" data-redirect-delay-ms="1500">
```

- **`data-mode="preview"` (default).** A striped banner shows at the top, and a "Preview mode" note sits under the button. A valid submit shows "Preview only. You are not registered." It is never a success message. If the tracking script is installed, a test contact may still appear in HighLevel. That is how you test mapping, so delete test contacts afterward.
- **`data-mode="live"`.** Switch only after the checklist passes. The banner and note are removed. After a valid submit the button shows "Saving your spot…". After `data-redirect-delay-ms`, the visitor goes to `data-thank-you-url`, or sees an on-page confirmation if that is empty.
- **`data-redirect-delay-ms`.** Gives the tracking script time to send the submission before the page changes. Keep 1500 unless testing shows you need more.

On `preview.html` only, also remove the `<meta name="robots" content="noindex, nofollow">` line when you go live.

### Why the submit handling will not block HighLevel

- Validation uses the browser's built-in form validation. Incomplete forms never fire a `submit` event, so External Tracking never sees half-finished entries.
- Valid forms fire a normal `submit` event that bubbles. The script never calls `stopPropagation`.
- The script calls `preventDefault` only to stop the browser from reloading the page with the form data in it. AJAX form plugins use the same pattern. Confirm capture with the checklist anyway.

## 6. Making edits later

1. Edit `highlevel-paste-ready.html`.
2. Run `node build.mjs` to refresh `preview.html`.
3. In HighLevel, replace the Custom JS/HTML element's contents with the updated file.

**Do not rename** the form `id`/`name` or any input `name` after you connect. Mapping and the workflow filter depend on them.
