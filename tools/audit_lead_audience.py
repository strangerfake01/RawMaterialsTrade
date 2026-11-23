#!/usr/bin/env python3
"""Assert B2B buyer and manufacturer enquiry intents stay distinct and consent-gated.

Read-only public HTML/JS audit; does not submit forms or send analytics.
"""
from pathlib import Path
from html.parser import HTMLParser
import re

ROOT=Path(__file__).resolve().parents[1]
FORM_ROUTES={
  "index.html":"buyer",
  "hu.html":"buyer",
  "de-at.html":"buyer",
  "sales-representation-distribution-partner-central-europe.html":"supplier_partnership",
  "hu-ertekesitesi-kepviselet-disztribucios-partner.html":"supplier_partnership",
  "de-at-vertriebspartner-distribution-chemierohstoffe.html":"supplier_partnership",
}
errors=[]
for filename,role in FORM_ROUTES.items():
    text=(ROOT/filename).read_text(encoding="utf-8")
    expected=r'<input\b[^>]*name="request_type"[^>]*value="'+role+r'"[^>]*>'
    if len(re.findall(expected,text))!=1:
        errors.append(f"{filename}: missing/ambiguous bounded request_type {role}")
    if text.count('id="inquiryForm"')!=1:
        errors.append(f"{filename}: missing unique RFQ form")
    if not text.count('name="cf-turnstile-response"') and not text.count('id="turnstileContainer"'):
        errors.append(f"{filename}: no Turnstile control")
js=(ROOT/"assets/js/site.v20261108.js").read_text(encoding="utf-8")
for required in (
   "window.__rmtAnalyticsConsentGranted&&typeof window.gtag==='function'",
   "form.querySelector('input[name=\"request_type\"]')?.value==='supplier_partnership'",
   "form_name:leadType==='supplier_partnership'?'manufacturer_partnership':'b2b_inquiry'",
   "lead_type:leadType",
   "window.gtag('event','generate_lead'",
):
    if required not in js:
        errors.append("Public analytics lacks consent/lead split guard: "+required)
# Parse the exact static generate_lead payload rather than matching "name"
# inside the safe analytics key "form_name".
lead_event=re.search(r"window\.gtag\('event','generate_lead',\{([^}]+)\}\)",js,re.S)
if not lead_event:
    errors.append("Missing explicit successful generate_lead event")
else:
    keys=re.findall(r"(?:^|,)\s*([A-Za-z_][A-Za-z0-9_]*)\s*:",lead_event.group(1))
    allowed={"form_name","form_language","lead_type"}
    if set(keys)!=allowed or len(keys)!=len(allowed):
        errors.append(f"GA lead payload must have only {sorted(allowed)}; got {keys}")
print("Buyer/manufacturer RFQ distinction:",len(FORM_ROUTES),"localized forms; errors=",len(errors))
for e in errors:print("ERROR:",e)
raise SystemExit(bool(errors))
