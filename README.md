# Daily Fresher Job Search & Emailer (7 AM IST)

This tiny automation searches the web every morning for **fresher / entry-level tech roles** (software developer/engineer and related roles) across **big tech** and **startups**, then emails you the links.

It uses **Azure Bing Web Search** (API) to avoid scraping job sites directly.

---

## Quick Start (Local)

1. **Python 3.9+** is recommended.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a **.env** or set the following environment variables (example shown for Gmail SMTP):
   ```bash
   # Bing Search
   BING_SEARCH_ENDPOINT=https://api.bing.microsoft.com/v7.0/search
   BING_SEARCH_KEY=YOUR_AZURE_BING_KEY

   # Email (SMTP)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your@gmail.com
   SMTP_PASS=your_app_password   # use app password with 2FA enabled
   EMAIL_FROM=your@gmail.com
   EMAIL_TO=recipient@example.com

   # Optional
   STATE_PATH=job_state.json
   ```

4. Run a **dry run**:
   ```bash
   python daily_job_search.py --dry-run
   ```

5. Send an actual email:
   ```bash
   python daily_job_search.py
   ```

---

## Schedule at 7:00 AM IST (cron)

On a Linux machine with IST timezone set, add this cron entry:
```
0 7 * * * /usr/bin/env -S bash -lc 'cd /path/to/job_search_automation && /usr/bin/python3 daily_job_search.py >> cron.log 2>&1'
```

If your server runs in **UTC**, 7:00 AM IST is **01:30 UTC**. In that case:
```
30 1 * * * /usr/bin/env -S bash -lc 'cd /path/to/job_search_automation && /usr/bin/python3 daily_job_search.py >> cron.log 2>&1'
```

---

## GitHub Actions (runs daily at 7:00 AM IST)

Use the provided workflow at `.github/workflows/job-search.yml`. Add your secrets in the repo settings:
- `BING_SEARCH_ENDPOINT`
- `BING_SEARCH_KEY`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `EMAIL_FROM`, `EMAIL_TO`

---

## What it searches

- Role keywords: software developer/engineer (backend, frontend, full-stack), SDE, data/ML/QA/DevOps/SRE.
- Level keywords: fresher, new grad, entry-level, 0–1 years, junior.
- Company names: a curated list of big tech & Indian startups.
- ATS/careers domains prioritized: Greenhouse, Lever, Workday, Ashby, and official careers portals.

Results are **deduplicated** and only **new links** since the previous run are emailed.

---

## Notes

- This collects **links** (title + snippet) via web search; it does **not scrape** full job descriptions to respect TOS.
- Tune keyword lists inside `daily_job_search.py` as you like.
- The state of sent links is kept in `job_state.json` (configurable by `STATE_PATH`).

