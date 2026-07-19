import json
import os

# Files
REPORT_JSON = "report.json"
TEMPLATE = "reports/email_template.html"
OUTPUT = "reports/mail.html"

# Check files
if not os.path.exists(REPORT_JSON):
    raise FileNotFoundError(f"{REPORT_JSON} not found.")

if not os.path.exists(TEMPLATE):
    raise FileNotFoundError(f"{TEMPLATE} not found.")

# Read report
with open(REPORT_JSON, "r", encoding="utf-8") as f:
    report = json.load(f)

summary = report.get("summary", {})

total = summary.get("collected", summary.get("total", 0))
passed = summary.get("passed", 0)
failed = summary.get("failed", 0)
skipped = summary.get("skipped", 0)

status_text = "PASSED" if failed == 0 else "FAILED"
status_icon = "✅" if failed == 0 else "❌"

# Read HTML template
with open(TEMPLATE, "r", encoding="utf-8") as f:
    html = f.read()

# Replace placeholders
replacements = {
    "{{TOTAL}}": str(total),
    "{{PASSED}}": str(passed),
    "{{FAILED}}": str(failed),
    "{{SKIPPED}}": str(skipped),
    "{{STATUS_TEXT}}": status_text,
    "{{STATUS_ICON}}": status_icon,

    "{{REPOSITORY}}": os.getenv("GITHUB_REPOSITORY", ""),
    "{{BRANCH}}": os.getenv("GITHUB_REF_NAME", ""),
    "{{COMMIT}}": os.getenv("GITHUB_SHA", "")[:7],
    "{{ACTOR}}": os.getenv("GITHUB_ACTOR", ""),
    "{{ENVIRONMENT}}": "QA",
    "{{BROWSER}}": "Chromium",
    "{{DURATION}}": "-",
    "{{DATE}}": "",
    "{{FAILED_ROWS}}": "<tr><td colspan='2'>See GitHub logs for failed test details.</td></tr>",
}

for key, value in replacements.items():
    html = html.replace(key, value)

# Write output
os.makedirs("reports", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated {OUTPUT}")
