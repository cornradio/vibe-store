"""
AI Auto-Moderator for Vibe App Store.
Triggered by GitHub Actions when a new app-submission issue is opened.
"""

import os
import json
import re
import subprocess

# --- Config ---
ISSUE_BODY = os.environ["ISSUE_BODY"]
ISSUE_NUMBER = os.environ["ISSUE_NUMBER"]
REPO = os.environ["GITHUB_REPOSITORY"]

# --- AI Review ---
def ai_review():
    """Ask AI to judge whether this submission fits the vibe."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

    if not api_key:
        print("No API key configured, auto-approving.")
        return {"is_vibe": True, "reason": "AI reviewer is offline. Auto-approved. Welcome to the vibe."}

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)

        prompt = f"""You are the editor of a Vibe App Store. This store accepts ANY indie web app built through vibe coding -- tools, games, utilities, creative experiments, AI apps, dashboards, anything. The only requirement is that it's a real, working web app with some personality.

Review the following submission. Judge whether it's a genuine working web app or just spam/a broken placeholder.

Submission:
---
{ISSUE_BODY}
---

Reply in JSON only, no other text:
{{"is_vibe": true/false, "reason": "Your review comment in Chinese. Be encouraging. Reject only obvious spam, broken links, or non-apps."}}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"AI review failed: {e}. Auto-approving.")
        return {"is_vibe": True, "reason": "AI reviewer encountered an error. Auto-approved."}


# --- Field Extraction ---
def extract_field(section_name):
    """Extract content from an issue body section."""
    pattern = rf"### {re.escape(section_name)}.*?\n(.*?)(?=\n###|\Z)"
    match = re.search(pattern, ISSUE_BODY, re.DOTALL)
    if not match:
        return ""

    text = match.group(1).strip()
    # Remove HTML comments (template hints)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()
    return text


# --- GitHub CLI helpers ---
def gh_comment(body):
    subprocess.run(
        ["gh", "issue", "comment", ISSUE_NUMBER, "--body", body],
        check=True, capture_output=True
    )


def gh_add_label(label):
    subprocess.run(
        ["gh", "issue", "edit", ISSUE_NUMBER, "--add-label", label],
        check=True, capture_output=True
    )


def gh_close():
    subprocess.run(
        ["gh", "issue", "close", ISSUE_NUMBER],
        check=True, capture_output=True
    )


# --- Main ---
def main():
    result = ai_review()
    is_vibe = result.get("is_vibe", True)
    reason = result.get("reason", "")

    if is_vibe:
        # Extract fields
        name = extract_field("App Name")
        tagline = extract_field("Tagline")
        logo = extract_field("Logo URL")
        url = extract_field("App URL")
        tags_raw = extract_field("Vibe Tags")

        # If logo field is empty, grab the first image from anywhere in the issue
        if not logo or not logo.startswith("http"):
            # Try markdown image: ![alt](url)
            img_match = re.search(r"!\[.*?\]\((https?://[^\s\)]+)\)", ISSUE_BODY)
            if img_match:
                logo = img_match.group(1)
            else:
                # Try HTML img tag: <img src="url">
                img_match = re.search(r'<img[^>]+src=["\']?(https?://[^\s"\'>]+)', ISSUE_BODY)
                if img_match:
                    logo = img_match.group(1)

        # Parse tags
        tags = [t.strip() for t in tags_raw.split() if t.strip().startswith("#")]

        new_app = {
            "name": name or f"VibeApp-{ISSUE_NUMBER}",
            "tagline": tagline or "A mysterious app radiating unique vibes.",
            "logo": logo if logo and logo.startswith("http") else "",
            "url": url or "",
            "tags": tags or ["#vibe"],
            "source_issue": f"https://github.com/{REPO}/issues/{ISSUE_NUMBER}"
        }

        # Update data.json
        data_path = "data.json"
        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        if not isinstance(data, list):
            data = []

        # Deduplicate by URL
        if url:
            data = [item for item in data if item.get("url") != url]

        data.insert(0, new_app)

        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Comment and label
        gh_comment(f"**AI Review: Approved**\n\n> {reason}")
        gh_add_label("approved")
        print(f"Approved: {name}")

    else:
        # Reject
        gh_comment(f"**AI Review: Rejected**\n\n> {reason}\n\nThis store only accepts indie apps with vibe and soul. Thanks for your submission!")
        gh_close()
        print(f"Rejected issue #{ISSUE_NUMBER}")


if __name__ == "__main__":
    main()
