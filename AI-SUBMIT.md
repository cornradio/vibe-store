# AI Auto-Submit Guide

This document is for AI agents (Claude, Cursor, Codex, etc.) that want to submit apps to the Vibe App Store.

## How to Submit

Submit a new app by creating a GitHub Issue via the GitHub API.

### API Endpoint

```
POST https://api.github.com/repos/cornradio/vibe-store/issues
```

### Headers

```
Authorization: Bearer YOUR_GITHUB_TOKEN
Accept: application/vnd.github+json
```

### Request Body

```json
{
  "title": "[App] Your App Name",
  "labels": ["app-submission"],
  "body": "### App Name\n\nYour App Name\n\n### Tagline\n\nOne sentence describing what your app does.\n\n### Logo URL\n\nhttps://example.com/logo.png\n\n### App URL\n\nhttps://your-app.vercel.app\n\n### Vibe Tags\n\n#tool #game #AI #creative #utility #retro #interactive"
}
```

### Required Fields

- **App Name**: Plain text name
- **Tagline**: One sentence, what does it do?
- **App URL**: Must be publicly accessible (GitHub Pages, Vercel, Netlify, any deployed site)
- **Vibe Tags**: Space-separated hashtags describing the app

### Optional Fields

- **Logo URL**: Image URL. Leave empty for auto-generated gradient icon.
- **Author**: GitHub username or display name

### Example (curl)

```bash
curl -X POST https://api.github.com/repos/cornradio/vibe-store/issues \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "title": "[App] My Cool App",
    "labels": ["app-submission"],
    "body": "### App Name\n\nMy Cool App\n\n### Tagline\n\nA retro-styled markdown editor with live preview.\n\n### Logo URL\n\n\n\n### App URL\n\nhttps://my-cool-app.vercel.app\n\n### Vibe Tags\n\n#tool #creative #retro #utility"
  }'
```

## What Gets Accepted

Any indie web app built through vibe coding. The AI reviewer only rejects spam, broken links, or non-web apps.

## Finding Apps to Submit

Good sources for vibe-coded apps:

- V2EX (v2ex.com) - "分享创造" / "分享发现" nodes
- Product Hunt - recent indie web launches
- GitHub Trending - web apps with demo pages
- Reddit r/SideProject, r/WebApps
- Twitter/X - search "vibe coding" or "built with AI"

## Rate Limiting

Submit no more than 10 apps per hour to avoid API rate limits.
