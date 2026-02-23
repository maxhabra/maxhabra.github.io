# Max Habra - Personal Website

Professional personal website and online resume for **Max Habra**, focused on security, cloud architecture, and DevSecOps leadership.

## Overview

This repository contains a static portfolio/resume site used to present:

- Professional summary and certifications
- Technical skills and areas of expertise
- Work experience and highlights
- Talks and selected professional activities
- Contact and social links

The site is lightweight, fast to load, and easy to maintain as a single-page profile.

## Tech Stack

- `HTML5` (`index.html`)
- `CSS3` (`assets/main.css`)
- `JavaScript` (`assets/js/index.js`)
- Static assets in `images/` and `assets/`

No build step is required.

## Project Structure

```text
.
├── index.html
├── assets/
│   ├── main.css
│   ├── favicon.ico
│   └── js/
│       └── index.js
├── images/
│   ├── profile.jpg
│   └── favicon.ico
└── README.md
```

## Run Locally

From the repository root:

```bash
cd maxhabra.github.io
python3 -m http.server 8080
```

Then open:

- `http://localhost:8080`

## Deployment

This project is suitable for static hosting (for example GitHub Pages).  
If this repo is used as a GitHub Pages site, push to the configured deployment branch and GitHub will publish the updated page.

## Maintenance Notes

- Update profile content directly in `index.html`
- Keep styling changes in `assets/main.css`
- Keep behavior changes in `assets/js/index.js`
- Optimize images before committing to keep page load times low

## License

See `LICENSE`.
