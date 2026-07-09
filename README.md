# Vibe App Store

An AI-curated, GitHub-powered indie web app store. No server, no database, just pure vibe.

Developers submit apps via GitHub Issues. AI reviews submissions automatically. Approved apps appear on the site instantly.

**[Live Demo](https://your-username.github.io/vibe-store/)**

## How to Submit an App

Anyone can submit a vibe app. It takes 30 seconds:

1. Click the **"+ Submit App"** button on the [store page](https://your-username.github.io/vibe-store/)
2. You'll be redirected to a GitHub Issue with a pre-filled template
3. Fill in your app's name, description, logo URL, live demo URL, and vibe tags
4. Submit the issue

That's it. An AI reviewer will evaluate your submission within minutes. If it fits the vibe, it goes live on the store automatically. You'll get a comment on your issue with the AI's review.

### What Gets Accepted

The store accepts indie web apps with soul. Think:

- AI companions and chat apps with personality
- Lo-fi music players, ambient sound generators
- Creative tools: pixel art, generative art, mood boards
- Healing and wellness apps: breathing, journaling, meditation
- Cyberpunk, retro, or uniquely styled utilities
- Anything with a strong vibe that a traditional app store would reject

### What Gets Rejected

- Generic business tools, dashboards, or CRUD apps
- Apps that are just landing pages with no functionality
- Submissions with broken or placeholder URLs

### Tips for a Good Submission

- **Logo**: Drag and drop an image directly into the GitHub issue -- GitHub will auto-upload it and give you a URL
- **App URL**: Deploy your app on GitHub Pages, Vercel, or Netlify (all free)
- **Tags**: Pick tags that describe your app's mood, not just its tech stack

## Setup (Store Owner)

If you want to run your own Vibe App Store:

### 1. Create the repo

```bash
# Clone or fork this repo
git clone https://github.com/your-username/vibe-store.git
cd vibe-store

# Push to your own GitHub repo
gh repo create vibe-store --public --source=. --push
```

### 2. Configure AI review

Go to your repo **Settings > Secrets and variables > Actions**, then add:

| Secret Name | Value | Required |
|---|---|---|
| `OPENAI_API_KEY` | Your LLM API key (OpenAI, DeepSeek, etc.) | Yes |
| `OPENAI_BASE_URL` | API base URL (skip for OpenAI, use `https://api.deepseek.com/v1` for DeepSeek) | Optional |

### 3. Enable write permissions

Go to **Settings > Actions > General**, scroll to **Workflow permissions**, select **Read and write permissions**, then save.

This allows the AI workflow to update `data.json` and label issues.

### 4. Deploy to GitHub Pages

Go to **Settings > Pages**, set **Branch** to `main` and folder to `/ (root)`, then save.

Your store will be live at `https://your-username.github.io/vibe-store/` within a few minutes.

### 5. Customize

Edit `data.json` to add initial apps manually, or submit them through the issue flow like everyone else.

Edit the AI review prompt in `scripts/review.py` to adjust the store's taste and personality.

## File Structure

```
vibe-store/
  index.html                       # Frontend (single-page, zero dependencies)
  data.json                        # App database (auto-updated by AI workflow)
  .github/
    ISSUE_TEMPLATE/
      submit-app.md                # Issue template for submissions
    workflows/
      ai-moderator.yml             # GitHub Action: AI review + auto-publish
  scripts/
    review.py                      # AI review logic
  README.md
```

## Compatible LLM Providers

The AI reviewer uses the OpenAI SDK format, so it works with any compatible provider:

- **OpenAI** (gpt-4o-mini recommended for cost/speed balance)
- **DeepSeek** (set `OPENAI_BASE_URL` to `https://api.deepseek.com/v1`)
- **ZhiPu / GLM** (set `OPENAI_BASE_URL` to `https://open.bigmodel.cn/api/paas/v4`)
- **Any OpenAI-compatible API**

If no API key is configured, submissions are auto-approved as a fallback.

## License

MIT
