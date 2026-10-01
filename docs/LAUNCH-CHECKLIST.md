# Launch Checklist

Run this with the page in **preview mode** on an unshared URL. Use your own email and phone, plus a few `+test` email aliases (for example `you+test1@gmail.com`). Delete every test contact before launch.

## 1. Page and placeholders

- [x] Webinar title confirmed: it is the opening message, already in the hero and page title.
- [ ] Both photos load on the live page (in HighLevel, their `src` points to your Media Storage URLs, not `images/...`).
- [x] Privacy Policy and Terms drafts written (`legal/`).
- [ ] **Blocker:** fill in the highlighted details (business name, email, mailing address, state), have the drafts reviewed, and publish both pages.
- [ ] Both legal page links (under the form and in the footer) open your live Privacy Policy and Terms pages.
- [ ] Date and time read **Sunday, October 18, 2026 · 7 PM Eastern** everywhere.
- [x] Mentees are comfortable with their messages being shown (names are hidden).
- [ ] All four testimonial screenshots load on the live page.
- [ ] Page title, description, and share image are set (HighLevel page SEO settings, or `<head>` in `preview.html`).
- [ ] Looks right and has no sideways scrolling in: **Instagram in-app browser on iPhone**, **Instagram in-app browser on Android**, Safari, Chrome. (Test by sending the link to yourself in an Instagram DM and opening it there.)
- [ ] Every "Save My Free Spot" button scrolls to the form.

## 2. Form behavior

- [ ] Submitting empty shows a message under each of the 4 required fields and moves focus to First name.
- [ ] A bad email (`name@site`) and a short phone (`555-1234`) each show a helpful message.
- [ ] "Select your industry" is not accepted as an answer.
- [ ] Choosing **Other** shows "Tell us what you do." and it is required. Switching back hides it.
- [ ] All three consent boxes start **unchecked**, and the form submits with none of them checked.
- [ ] In preview mode, a valid submit shows "Preview only. You are not registered." and never a success message.

## 3. Contact capture (tracking script installed)

- [ ] External Tracking script is pasted **once**, in the head tracking code (not inside the Custom JS/HTML element).
- [ ] Inspect the live page: `<form id="rie-webinar-registration">` is **not inside an `<iframe>`**.
- [ ] Loading the page registers a page view in External Tracking analytics.
- [ ] A valid test submission **creates a contact** in HighLevel.
- [ ] Submitting again with the **same email** updates that contact instead of creating a duplicate.
- [ ] The contact's submission details show the form name **`rie-webinar-registration`**.
- [ ] An **invalid** attempt (any required field missing) creates **nothing**.
- [ ] If contacts do not appear on a HighLevel-hosted page, stop and switch to a supported alternative from the setup guide (section 3). Do not launch until capture works.

## 4. Field mapping

| Test | Expected in HighLevel | Pass |
|---|---|---|
| First name `Test` | First Name = `Test` | [ ] |
| Email | Email field filled, lowercase as typed | [ ] |
| Phone `(555) 123-4567` | Phone filled and shown in a normal format | [ ] |
| Industry `Lash artist` | Beauty Industry = `Lash artist` | [ ] |
| Industry `Esthetician or skincare professional` | Exact text, nothing cut off | [ ] |
| Industry `Other` + "Brow lamination" | Beauty Industry = `Other`, Beauty Industry Other = `Brow lamination` | [ ] |
| Industry `Hairstylist` after first choosing Other | Beauty Industry Other is **empty** | [ ] |

## 5. Consent values

Submit one test contact per row. Every box not listed must be **empty** (not `Yes`).

| Test contact | Boxes checked | Webinar SMS Reminders | Promotional SMS | Email Marketing | Pass |
|---|---|---|---|---|---|
| test1 | none | empty | empty | empty | [ ] |
| test2 | reminders only | `Yes` | empty | empty | [ ] |
| test3 | promotional only | empty | `Yes` | empty | [ ] |
| test4 | email only | empty | empty | `Yes` | [ ] |
| test5 | all three | `Yes` | `Yes` | `Yes` | [ ] |

- [ ] Re-submitting an existing contact with a box **unchecked** does not wrongly keep or add consent. Decide how to handle someone who opted in before and now leaves it unchecked, and note it for your automations.
- [ ] Final SMS disclosure wording is approved and matches your **A2P 10DLC** brand and campaign registration (sender name, message types, frequency, STOP/HELP).
- [ ] Your Privacy Policy covers SMS and does not allow sharing mobile numbers or opt-in data with third parties for marketing.
- [ ] Save a screenshot of the form and disclosure text with the launch date, as a record of what people agreed to.

## 6. Workflow trigger

- [ ] Trigger is **Form Submitted**, filtered to external form name `rie-webinar-registration` (plus domain/page path).
- [ ] Each test submission enters the workflow **exactly once**.
- [ ] A submission from any other form or page does **not** enter it.
- [ ] Reminder-text steps run only when Webinar SMS Reminders Consent = `Yes`.
- [ ] Promotional-text steps run only when Promotional SMS Consent = `Yes`.
- [ ] Ongoing marketing emails run only when Email Marketing Consent = `Yes`.
- [ ] Webinar emails (how to join) go to every registrant.

## 7. Go live

- [ ] Set `data-mode="live"` on `#rie-webinar`.
- [ ] Set `data-thank-you-url` if you are using a thank-you page, and confirm it loads.
- [ ] (`preview.html` only) Remove the `noindex` robots line.
- [ ] Re-paste the updated code into HighLevel (or redeploy), then hard-refresh. The striped preview banner is gone.
- [ ] One final live submission creates a contact, enters the workflow once, and lands on the thank-you page or confirmation.
- [ ] Delete all test contacts, and remove them from any workflows they entered.
- [ ] Now share the link (Instagram bio, stories, DMs).
