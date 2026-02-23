# Max Habra - Personal Website

This repository hosts **maxhabra.github.io**, a static personal website and resume.

## What is in this repo

- `index.html`: main site content
- `assets/main.css`: styling
- `assets/js/index.js`: client-side behavior
- `assets/data/github-activity.json`: generated GitHub activity data used on the site
- `images/`: profile and favicon assets
- `resume-en/` and `resume-fr/`: source and PDF resumes
- `scripts/update_github_activity.py`: script used by the GitHub Action

## Quick local preview

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080`.

## Updating site content

- Edit content in `index.html`
- Update styles in `assets/main.css`
- Update behavior in `assets/js/index.js`
- Replace static files in `images/` or resume folders as needed

## GitHub Action: Daily GitHub activity update

Workflow file: `.github/workflows/update-github-activity.yml`

This workflow runs daily (`5 5 * * *`) and updates `assets/data/github-activity.json`.

### One-time GitHub setup

1. In your GitHub repo, go to `Settings` -> `Actions` -> `General`.
2. Under workflow permissions, select `Read and write permissions`.
3. Go to `Settings` -> `Secrets and variables` -> `Actions`.
4. Add a repository secret named `GH_ACTIVITY_TOKEN`.

### Token requirements

Create a classic GitHub Personal Access Token and use it as `GH_ACTIVITY_TOKEN`.

Required scope:
- `read:user`

Optional scope:
- `repo` (only if you want private repo activity included)

### Manual run

1. Open the repo on GitHub.
2. Go to `Actions` -> `Update GitHub Activity`.
3. Click `Run workflow`.

## License

See `LICENSE`.
