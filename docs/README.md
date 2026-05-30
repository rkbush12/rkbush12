# DataminBI — consulting website

The source for **<https://dataminbi.com>**: a fast, dependency-free static site
for a data / BI consulting practice (Kenny Bush). No build step, no frameworks —
just HTML, CSS, and a few lines of vanilla JavaScript, so it deploys anywhere
and loads instantly.

## Files

```
docs/
├── index.html        # The single-page site (hero, services, approach, about, contact)
├── styles.css        # Styles — palette matches the "Aurora Sales" Power BI theme
├── main.js           # Mobile nav toggle + footer year
├── 404.html          # Friendly not-found page
├── CNAME             # Custom domain for GitHub Pages (dataminbi.com)
├── robots.txt        # Crawler directives
├── sitemap.xml       # Sitemap for search engines
└── assets/
    ├── logo.svg      # Brand mark
    └── favicon.svg   # Browser tab icon
```

## Go live with GitHub Pages (this repo, `/docs`)

This site is ready to serve straight from the `/docs` folder:

1. Merge this branch into **`main`** (Pages serves from a real branch, not a
   `claude/...` working branch).
2. In the repo: **Settings → Pages → Build and deployment**
   → Source: **Deploy from a branch** → Branch: **`main`** / **`/docs`** → Save.
3. Under **Custom domain**, enter `dataminbi.com` (the `CNAME` file already sets
   this) and enable **Enforce HTTPS** once the certificate is issued.

### DNS for `dataminbi.com`

At your domain registrar, point the domain at GitHub Pages:

- **Apex** (`dataminbi.com`) — four `A` records:
  `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- **`www`** subdomain — a `CNAME` record pointing to `rkbush12.github.io`

DNS changes can take up to ~24 hours to propagate.

## Recommended upgrade: a dedicated repo

This site currently lives inside your profile/coursework repo. For the most
credible setup, host it from a **dedicated public repo** (e.g. `dataminbi` or
`rkbush12.github.io`):

1. Create the new repo on GitHub.
2. Copy the **contents of this `docs/` folder** into the new repo's root
   (or its own `/docs`).
3. Enable Pages there and move the `dataminbi.com` custom domain over.

Because the site is plain static files, it's fully portable — nothing here is
tied to this repo.

## Before you publish — fill in the placeholders

Search `index.html` for these and replace them:

| Placeholder | Where | Replace with |
| ----------- | ----- | ------------ |
| `YOUR_FORM_ID` | contact `<form action>` | Your [Formspree](https://formspree.io) endpoint |
| `calendly.com/your-handle/intro-call` | "Book a call" link | Your real scheduling URL |
| `linkedin.com/in/your-handle` | contact + footer | Your LinkedIn profile |
| `rk.bush@outlook.com` | email button | Optionally a domain address like `hello@dataminbi.com` |

## Local preview

```bash
cd docs
python3 -m http.server 8000
# then open http://localhost:8000
```
