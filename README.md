markdown
# 🔍 Daily Fresher Job Search & Emailer (7:00 AM IST)

This is a lightweight automation I built to help freshers stay proactive in their job search. Every morning at **7:00 AM IST**, it scans the web for **entry-level tech roles**—like software developer, SDE, ML, QA, DevOps, etc.—across **top tech companies** and **startups**, and sends the latest job links straight to your inbox.

It uses the **Azure Bing Web Search API**, so it doesn’t scrape job sites directly and stays compliant with platform policies.

---

## ⚙️ Quick Start (Local Setup)

> Recommended: Python 3.9+

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```
Step 2: Configure environment variables (via .env or system settings)

Example setup for Gmail SMTP: 

To run this project smoothly, you’ll need to set up a .env file or manually configure the required environment variables. These include your email credentials and API key for Bing Search.

Here’s what you need to add in .env:
```
# Bing Search API
BING_SEARCH_ENDPOINT=https://api.bing.microsoft.com/v7.0/search
BING_SEARCH_KEY=YOUR_AZURE_BING_KEY   # Get this from your Azure portal

# Email Setup (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASS=your_app_password           # Use Gmail app password if 2FA is enabled
EMAIL_FROM=your@gmail.com
EMAIL_TO=recipient@example.com        # Where you want the job links to be sent

# Optional
STATE_PATH=job_state.json             # Tracks which job links have already been sent
```
Without this setup, the script won’t be able to send emails or fetch job listings. So either create a .env file with these details or set them directly in your system environment.

Step 3: Dry run (no email sent)
```
bash
python daily_job_search.py --dry-run
```
Step 4: Send actual email
```
bash
python daily_job_search.py
```
⏰ Automate with Cron (Linux)
If your system timezone is IST:
```
bash
0 7 * * * /usr/bin/env -S bash -lc 'cd /path/to/job_search_automation && /usr/bin/python3 daily_job_search.py >> cron.log 2>&1'
```
If your server runs in UTC (7:00 AM IST = 01:30 UTC):
```
bash
30 1 * * * /usr/bin/env -S bash -lc 'cd /path/to/job_search_automation && /usr/bin/python3 daily_job_search.py >> cron.log 2>&1'
```
🧪 GitHub Actions (Auto-run Daily)
Use the workflow at .github/workflows/job-search.yml. Add these secrets in your repo settings:
```
BING_SEARCH_ENDPOINT

BING_SEARCH_KEY

SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS

EMAIL_FROM, EMAIL_TO
```
🔎 What It Searches
Roles: Software Developer, SDE, Backend, Frontend, Full Stack, QA, ML, DevOps, SRE

Levels: Fresher, Entry-Level, New Grad, 0–1 Years, Junior

Companies: Curated list of big tech & Indian startups

Sources: Prioritizes ATS platforms like Greenhouse, Lever, Workday, Ashby, and official careers portals

Only new job links since the last run are emailed—no duplicates.

📝 Notes
This tool collects job titles + snippets via web search (no scraping)

You can customize keyword lists inside daily_job_search.py

Sent links are tracked in job_state.json (configurable via STATE_PATH)

👨‍💻 About Me
I'm Konda Prashanth, a B.Tech graduate in Data Science from MLR Institute of Technology. I specialize in Python, Java, C++, and core CS concepts like DSA, DBMS, and OOPs. Currently focused on DSA (Java), Full Stack Development, and System Design for product-based roles.

This project reflects my mindset: clarity, automation, and impact—helping freshers stay informed and job-ready every single day.

📬 Connect With Me:

-📧 Email: kondadattathri@gmail.com

-💼 LinkedIn: [prashanth-kpy](linkedin.com/in/prashanth-kpy)
