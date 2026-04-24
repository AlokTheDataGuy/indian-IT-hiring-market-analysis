"""
Companies to track.

CRITICAL: `ats_url` must point to the ACTUAL job board, not the company's
homepage. Most startups host careers on Greenhouse, Lever, or Ashby.

How to find the right URL manually:
  1. Visit the company's careers page in your browser.
  2. Click any job listing.
  3. Observe the URL. You'll usually land on:
       - jobs.lever.co/<company>
       - boards.greenhouse.io/<company>
       - <company>.ashbyhq.com
       - jobs.ashbyhq.com/<company>
  4. Use the listing-index URL (not a specific job URL).

Leave `ats_url` as None if you can't find one — you'll need to scrape the
company's own careers page, which often means JS rendering.
"""

COMPANIES = [
    # Fintech
    {"name": "razorpay",       "ats_platform": "lever",      "ats_url": "jobs.lever.co/razorpay"},
    {"name": "cred",           "ats_platform": "lever",      "ats_url": "jobs.lever.co/cred"},
    {"name": "groww",          "ats_platform": "lever",      "ats_url": "jobs.lever.co/groww"},
    {"name": "phonepe",        "ats_platform": "phonepe",    "ats_url": "phonepe.com/careers"},
    {"name": "zerodha",        "ats_platform": "zerodha",    "ats_url": "zerodha.com/careers"},
    {"name": "cashfree",       "ats_platform": "lever",      "ats_url": "jobs.lever.co/cashfree"},

    # Commerce & logistics
    {"name": "meesho",         "ats_platform": "lever",      "ats_url": "jobs.lever.co/meesho"},
    {"name": "zepto",          "ats_platform": "lever",      "ats_url": "jobs.lever.co/zepto"},
    {"name": "flipkart",       "ats_platform": "flipkart",   "ats_url": "flipkartcareers.com"},
    {"name": "swiggy",         "ats_platform": "swiggy",     "ats_url": "careers.swiggy.com"},
    {"name": "zomato",         "ats_platform": "zomato",     "ats_url": "zomato.com/careers"},
    {"name": "nykaa",          "ats_platform": "nykaa",      "ats_url": "nykaa.com/careers"},
    {"name": "urbancompany",   "ats_platform": "lever",      "ats_url": "jobs.lever.co/urbancompany"},
    {"name": "ola",            "ats_platform": "ola",        "ats_url": "olacabs.com/careers"},
    {"name": "rupeek",         "ats_platform": "lever",      "ats_url": "jobs.lever.co/rupeek"},

    # SaaS & dev tools
    {"name": "postman",        "ats_platform": "greenhouse", "ats_url": "boards.greenhouse.io/postman"},
    {"name": "freshworks",     "ats_platform": "freshworks", "ats_url": "freshworks.com/company/careers"},
    {"name": "zoho",           "ats_platform": "zoho",       "ats_url": "zoho.com/careers"},
    {"name": "chargebee",      "ats_platform": "lever",      "ats_url": "jobs.lever.co/chargebee"},
    {"name": "hasura",         "ats_platform": "greenhouse", "ats_url": "boards.greenhouse.io/hasura"},
    {"name": "atlan",          "ats_platform": "lever",      "ats_url": "jobs.lever.co/atlan"},

    # Edtech
    {"name": "unacademy",      "ats_platform": "lever",      "ats_url": "jobs.lever.co/unacademy"},
    {"name": "byjus",          "ats_platform": "byjus",      "ats_url": "byjus.com/careers"},
    {"name": "physicswallah",  "ats_platform": "lever",      "ats_url": "jobs.lever.co/physicswallah"},
    {"name": "vedantu",        "ats_platform": "vedantu",    "ats_url": "vedantu.com/careers"},

    # Others
    {"name": "paytm",          "ats_platform": "paytm",      "ats_url": "paytm.com/careers"},
    {"name": "khatabook",      "ats_platform": "lever",      "ats_url": "jobs.lever.co/khatabook"},
    {"name": "dukaan",         "ats_platform": "dukaan",     "ats_url": "mydukaan.io/careers"},
    {"name": "invideo",        "ats_platform": "lever",      "ats_url": "jobs.lever.co/invideo"},
]

# NOTE: The ats_url values above are my best guesses based on common patterns.
# Before running the full pipeline, verify each one manually by visiting the
# URL in your browser. Some will be wrong; update this file as you verify.
