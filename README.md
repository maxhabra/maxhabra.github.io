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
├── .github/
│   └── workflows/
│       └── update-github-activity.yml
├── index.html
├── assets/
│   ├── data/
│   │   └── github-activity.json
│   ├── main.css
│   ├── favicon.ico
│   └── js/
│       └── index.js
├── images/
│   ├── profile.jpg
│   └── favicon.ico
├── scripts/
│   └── update_github_activity.py
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

## Daily GitHub Activity Automation

This site includes a header badge that reads from `assets/data/github-activity.json`.
That JSON is refreshed daily by GitHub Actions.

### One-time setup in GitHub

1. Push this repository to GitHub.
2. Open the repo in GitHub, then go to `Settings` -> `Actions` -> `General`.
3. Under workflow permissions, select `Read and write permissions`.
4. Click `Save`.
5. Go to `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`.
6. Create a secret named `GH_ACTIVITY_TOKEN`.

### Token creation

Use a classic Personal Access Token (PAT):

1. GitHub avatar -> `Settings` -> `Developer settings` -> `Personal access tokens` -> `Tokens (classic)`.
2. Create a token with:
   - `read:user` (required)
   - `repo` (required if you want private repo activity included)
3. Copy the token once and store it as `GH_ACTIVITY_TOKEN` secret in this repo.

### Schedule and timing

- Workflow file: `.github/workflows/update-github-activity.yml`
- Current schedule: `5 5 * * *` (05:05 UTC daily)
- This is approximately midnight US Eastern during standard time.
- If you want another timezone target, change the cron expression.

### Manual run

You can trigger it manually from:

- GitHub repo -> `Actions` -> `Update GitHub Activity` -> `Run workflow`

### Local test

From the repo root:

```bash
cd maxhabra.github.io
python3 scripts/update_github_activity.py
cat assets/data/github-activity.json
```

## License

See `LICENSE`.
