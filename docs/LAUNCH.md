# Launch checklist — Lanka Freediving

Steps to connect **lankafreediving.com** (GoDaddy) to the Sleeve site on Vercel and go live.

## 1. Vercel domain

1. Open [Vercel Dashboard](https://vercel.com) → your **lanka-freediving** project → **Settings** → **Domains**.
2. Add `lankafreediving.com` and `www.lankafreediving.com`.
3. Set **lankafreediving.com** as the primary domain.

## 2. GoDaddy DNS (website)

Choose one approach:

### Option A — Vercel nameservers (simplest)

In GoDaddy → Domain → **Nameservers** → Custom:

- `ns1.vercel-dns.com`
- `ns2.vercel-dns.com`

Vercel manages all DNS records.

### Option B — Keep GoDaddy DNS

Add these records (do not remove existing MX records when adding Zoho):

| Type  | Name | Value                |
| ----- | ---- | -------------------- |
| A     | @    | `76.76.21.21`        |
| CNAME | www  | `cname.vercel-dns.com` |

## 3. Zoho Mail — hello@lankafreediving.com

1. Sign up at [Zoho Mail](https://www.zoho.com/mail/) → **Mail Lite** (free, 1 user).
2. Add domain `lankafreediving.com`, create mailbox **hello@**.
3. In GoDaddy DNS, add Zoho **MX** and **TXT** records (Zoho shows exact values).
4. Send a test email to hello@ and reply from hello@.
5. Optional: forward hello@ → your Gmail in Zoho settings.

MX records and website A/CNAME records work together — no conflict.

## 4. Resend (contact form)

1. Create account at [Resend](https://resend.com).
2. Add domain `lankafreediving.com` and add the DNS records Resend provides (SPF/DKIM).
3. In Vercel → **Settings** → **Environment Variables**:

| Variable            | Value                              |
| ------------------- | ---------------------------------- |
| `RESEND_API_KEY`    | Your Resend API key                |
| `CONTACT_TO_EMAIL`  | `hello@lankafreediving.com`        |
| `CONTACT_FROM_EMAIL`| `Lanka Freediving <hello@lankafreediving.com>` |

4. Redeploy, then submit a test message on `/contact/`.

Until Resend is configured, the form returns a friendly error — WhatsApp still works.

## 5. WhatsApp number

Edit [`explore/a-record-sleeve/site-config.js`](explore/a-record-sleeve/site-config.js):

```js
whatsapp: "94XXXXXXXXX",  // country code + number, no + or spaces
```

Redeploy after updating.

## 6. Search engines

### Google Search Console

1. [search.google.com/search-console](https://search.google.com/search-console)
2. Add property `lankafreediving.com` (DNS TXT or HTML verify).
3. Submit sitemap: `https://lankafreediving.com/sitemap.xml`

### Bing Webmaster Tools

1. [bing.com/webmasters](https://www.bing.com/webmasters)
2. Import from Google Search Console or verify manually.
3. Submit the same sitemap.

## 7. Google Business Profile

1. Create profile: category **Freediving instructor** or **Diving school**.
2. Service area: Unawatuna / Galle (no home address required).
3. Hours: November–April season.
4. Website: `https://lankafreediving.com`
5. Add photos from the site assets.

## 8. Analytics

Plausible is included on all public Sleeve pages (`data-domain="lankafreediving.com"`).

1. Sign up at [plausible.io](https://plausible.io).
2. Add site `lankafreediving.com` — the script is already on the site.

## 9. Molchanovs & social

- Update your Molchanovs school listing URL to `https://lankafreediving.com`
- Instagram bio → `lankafreediving.com` (not vercel.app)

## 10. Post-launch smoke test

- [ ] `https://lankafreediving.com/` loads Sleeve homepage
- [ ] `/guides/` and one guide article load
- [ ] `/robots.txt`, `/sitemap.xml`, `/llms.txt` accessible
- [ ] Contact form delivers to hello@
- [ ] WhatsApp button opens correct chat
- [ ] `/studio/` still unlisted (noindex)
