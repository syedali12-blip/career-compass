# Deploying Career Compass to Vercel

## Why there are two copies of static files

Vercel ignores Flask's built-in static file serving (`app.static_folder`)
and instead serves anything in a top-level `public/` directory directly
through its CDN. Since every template already uses Flask's normal
`{{ url_for('static', filename='...') }}` (which generates `/static/...`
URLs), the simplest fix — without touching every template — is to mirror
the `static/` folder into `public/static/`, so `/static/...` URLs resolve
correctly no matter which server is handling the request:

- **Running locally** (`python app.py`): Flask serves from `static/` as normal.
- **Deployed on Vercel**: Vercel's CDN serves the same files from
  `public/static/`, bypassing Flask entirely for those requests (faster
  anyway — static files don't need to go through your Python function).

**If you add or change any file in `static/`, copy it into `public/static/`
too** (same relative path), or the deployed site will serve a stale/missing
version. A quick way to resync before deploying:

```bash
rm -rf public/static
mkdir -p public/static
cp -r static/* public/static/
```

## Deployment steps

1. Push this project to a GitHub/GitLab/Bitbucket repo.
2. Go to vercel.com -> Add New -> Project -> import that repo.
   Vercel auto-detects Flask from `requirements.txt` and `app.py` at the
   root — no `vercel.json` needed for the basic deploy.
3. In Project Settings -> Environment Variables, add:
   - `ONET_API_KEY`
   - `GEMINI_API_KEY`
   - `USE_GEMINI` = `true`
   Apply to Production, Preview, and Development, then redeploy.
4. Done — your Flask app runs as a single Vercel Function on Fluid compute
   (Hobby plan: up to 300s per request, which is comfortably enough for the
   O*NET -> Gemini -> PDF pipeline in this app, even with the model
   fallback chain in ai_engine.py).

## Notes

- `reportlab` and `matplotlib` (used for PDF generation) work fine in this
  environment — `pdf_generator.py` already builds everything in-memory via
  `io.BytesIO()` and uses matplotlib's non-GUI `Agg` backend, so there's no
  disk-write issue that serverless platforms usually cause.
- "Saved Options" (`static/js/saved.js`) uses the browser's `localStorage`,
  which is entirely client-side and unaffected by hosting platform.
