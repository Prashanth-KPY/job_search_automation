#!/usr/bin/env python3
"""
Daily Job Search & Emailer (7 AM IST) using SerpAPI
- Finds fresher/entry-level tech roles
- Prioritizes Hyderabad jobs, but includes other India roles
- Deduplicates results and emails only new links since last run
- Sends nicely formatted HTML email summary
"""

import os
import json
import html
import smtplib
import argparse
import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

STATE_PATH = os.environ.get("STATE_PATH", "job_state.json")
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")

BIG_TECH_COMPANIES = [
    "Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "NVIDIA",
    "Adobe", "Salesforce", "Uber", "Airbnb", "Stripe", "Dropbox", "Snowflake",
    "Oracle", "Cisco", "VMware", "PayPal", "Intel"
]

INDIA_STARTUPS = [
    "Flipkart", "Swiggy", "Zomato", "Ola", "Oyo", "Freshworks", "PhonePe",
    "Razorpay", "CRED", "Meesho", "Udaan", "BYJU'S", "Unacademy", "Zerodha",
    "Tata 1mg", "Spinny", "Zepto", "Dream11", "Groww", "InMobi"
]

ROLE_KEYWORDS = [
    "software engineer", "software developer", "SDE", "SDE 1", "backend engineer",
    "frontend engineer", "full stack developer", "data engineer", "ML engineer",
    "devops engineer", "site reliability engineer", "qa engineer", "test engineer"
]

LEVEL_KEYWORDS = [
    "fresher", "new grad", "new graduate", "graduate", "entry level", "0-1 years", "junior"
]

def load_state():
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def serpapi_search(query, num=20):
    if not SERPAPI_KEY:
        raise RuntimeError("SERPAPI_KEY missing in .env")
    params = {
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "num": num,
        "api_key": SERPAPI_KEY
    }
    try:
        r = requests.get("https://serpapi.com/search", params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"[WARN] SerpAPI request failed: {e}")
        return []

    jobs = data.get("jobs_results", [])
    results = []
    for job in jobs:
        results.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "via": job.get("via"),
            "date": job.get("detected_extensions", {}).get("posted_at"),
            "link": job.get("apply_options", [{}])[0].get("link", job.get("related_links", [{}])[0].get("link"))
        })
    return results

def build_queries(region_hint="Hyderabad, India"):
    queries = []
    roles = " OR ".join([f'"{r}"' for r in ROLE_KEYWORDS])
    levels = " OR ".join([f'"{l}"' for l in LEVEL_KEYWORDS])
    queries.append(f"({roles}) AND ({levels}) AND ({region_hint})")  # general India/Hyderabad
    for comp in BIG_TECH_COMPANIES + INDIA_STARTUPS:
        queries.append(f'"{comp}" AND ({roles}) AND ({levels}) AND ({region_hint})')
    return queries

def prioritize(job):
    score = 100
    link = job.get("link", "").lower()
    location = (job.get("location") or "").lower()
    if "hyderabad" in location or "hyderabad" in link:
        score -= 50  # prioritize Hyderabad jobs
    return score

def filter_new_items(hits, state):
    sent = set(state.get("sent_urls", []))
    return [h for h in hits if h.get("link") and h["link"] not in sent]

def render_email_html(fresh_hits):
    today = dt.datetime.now().strftime("%A, %d %B %Y")
    rows = [
        f"<tr><td><a href='{html.escape(h['link'])}'>{html.escape(h.get('title') or '')}</a></td>"
        f"<td>{html.escape(h.get('company') or '')}</td>"
        f"<td>{html.escape(h.get('location') or '')}</td>"
        f"<td>{html.escape(h.get('via') or '')}</td>"
        f"<td>{html.escape(h.get('date') or '')}</td></tr>"
        for h in fresh_hits
    ]
    table = "<tr><th>Title</th><th>Company</th><th>Location</th><th>Via</th><th>Date</th></tr>" + "".join(rows)
    return f"""
    <html>
    <body>
      <h2>Fresher Tech Roles — Daily Job Search (Hyderabad Priority)</h2>
      <p>Date: <b>{today}</b></p>
      <p>Filters: <i>Fresher / Entry Level</i> • <i>Software/Tech Roles</i> • <i>Big Tech & Startups</i> • <i>Hyderabad Focus</i></p>
      <table border="1" cellpadding="6" cellspacing="0">{table}</table>
      <p style="margin-top:10px;font-size:12px;color:#666">
        Generated automatically using SerpAPI.
      </p>
    </body>
    </html>
    """

def send_email(subject, html_body):
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    pwd  = os.environ.get("SMTP_PASS")
    email_from = os.environ.get("EMAIL_FROM")
    email_to = os.environ.get("EMAIL_TO")

    if not all([host, port, user, pwd, email_from, email_to]):
        raise RuntimeError("One or more SMTP settings missing in .env")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = email_from
    msg["To"] = email_to
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, pwd)
        server.sendmail(email_from, [email_to], msg.as_string())

def main():
    parser = argparse.ArgumentParser(description="Daily fresher job search & emailer")
    parser.add_argument("--per-query", type=int, default=12)
    parser.add_argument("--max-send", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    state = load_state()
    all_hits = []

    for q in build_queries():
        hits = serpapi_search(q, num=args.per_query)
        for h in hits:
            h["score"] = prioritize(h)
        all_hits.extend(hits)

    all_hits.sort(key=lambda x: x.get("score", 100))
    fresh = filter_new_items(all_hits, state)

    if not fresh:
        print("No new results today.")
        return

    fresh = fresh[:args.max_send]
    subject = f"[Daily Jobs] {len(fresh)} new fresher tech roles links (Hyderabad Priority)"
    html_body = render_email_html(fresh)

    if args.dry_run:
        print(subject)
        print(f"Prepared {len(fresh)} new links (dry-run; not sending).")
    else:
        send_email(subject, html_body)
        sent_urls = state.get("sent_urls", [])
        sent_urls.extend([h["link"] for h in fresh])
        state["sent_urls"] = list(dict.fromkeys(sent_urls))[-5000:]
        save_state(state)
        print(f"Sent {len(fresh)} links via email.")

if __name__ == "__main__":
    main()
