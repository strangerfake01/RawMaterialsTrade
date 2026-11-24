#!/usr/bin/env python3
"""Assert B2B buyer and manufacturer enquiry intents stay distinct and consent-gated.

Read-only public HTML/JS audit; does not submit forms or send analytics.
"""
from pathlib import Path
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
    if role=="supplier_partnership":
        form=re.search(r'<form\b(?=[^>]*\bid="inquiryForm")[^>]*>',text)
        base=re.search(r'\bdata-success-basic-msg="([^"]+)"',form.group(0)) if form else None
        confirmed=re.search(r'\bdata-success-msg="([^"]+)"',form.group(0)) if form else None
        if not base or not confirmed or confirmed[1]==base[1] or not confirmed[1].startswith(base[1]+" "):
            errors.append(f"{filename}: success and acknowledgement feedback must be distinct")
js=(ROOT/"assets/js/site.v20261108.js").read_text(encoding="utf-8")
for required in (
   "window.__rmtAnalyticsConsentGranted&&typeof window.gtag==='function'",
   "const leadType=requestType==='supplier_partnership'?'supplier_partnership':'buyer'",
   "const dimensions=()=>rfqAnalyticsDimensions(form.querySelector('input[name=\"request_type\"]')?.value,getLang())",
   "form_name:leadType==='supplier_partnership'?'manufacturer_partnership':'b2b_inquiry'",
   "lead_type:leadType",
   "window.gtag('event','generate_lead',rfqAnalyticsDimensions(data.get('request_type'),lang))",
   "if(!started)started=send('form_start',dimensions())",
   "send('form_submit_attempt',dimensions())",
):
    if required not in js:
        errors.append("Public analytics lacks consent/lead split guard: "+required)
# All three form events share bounded role dimensions. Verify the source-level
# allowlist rather than matching "name" inside the safe key "form_name".
lead_event=re.search(r"function rfqAnalyticsDimensions\(requestType,lang\)\{\s*const leadType=[^\n]+\s*return \{([^}]+)\}",js,re.S)
if not lead_event:
    errors.append("Missing shared, bounded RFQ analytics dimensions")
else:
    keys=re.findall(r"(?:^|,)\s*([A-Za-z_][A-Za-z0-9_]*)\s*:",lead_event.group(1))
    allowed={"form_name","form_language","lead_type"}
    if set(keys)!=allowed or len(keys)!=len(allowed):
        errors.append(f"GA lead payload must have only {sorted(allowed)}; got {keys}")
print("Buyer/manufacturer RFQ distinction:",len(FORM_ROUTES),"localized forms; errors=",len(errors))
for e in errors:print("ERROR:",e)
raise SystemExit(bool(errors))
