# YouTube Comment Auto-Reply Bot

Reads the recent comments on your brother's channel and drafts (or posts)
replies written by Claude, in a voice you define. Everything customizable
lives in one file, `config.py`.

**Files in this project:**

| File | What it's for |
|---|---|
| `bot.py` | The actual logic. You shouldn't need to touch this. |
| `config.py` | **Edit this one.** Persona, rules, safety switches. |
| `.env.example` | Template for your Anthropic API key. |
| `requirements.txt` | Python packages the bot needs. |

Budget about 20-25 minutes for first-time setup, most of it in Google Cloud Console.

---

## Before you start

- Python 3.9+ installed on your machine
- The Google account that owns the YouTube channel (this'll probably need to be your brother, at least for a minute — see Step 4)
- An Anthropic API key (Step 2 below)

---

## Step 1 — Google Cloud project + YouTube API access

This is the fiddly part, but it's one-time.

1. Go to **console.cloud.google.com** and create a new project (top-left project dropdown → New Project).
2. **Enable the API**: in the search bar, find "YouTube Data API v3" → click **Enable**.
3. **Configure the consent screen**: go to *APIs & Services → OAuth consent screen*.
   - User type: **External**
   - Fill in the required fields (app name, your email) — you can put anything reasonable, this is only ever seen by you and your brother
   - Under **Scopes**, add: `https://www.googleapis.com/auth/youtube.force-ssl`
   - Under **Test users**, add your brother's Google account (the one that owns the channel)
4. **Create credentials**: go to *APIs & Services → Credentials → Create Credentials → OAuth client ID*.
   - Application type: **Desktop app** (important — Web application won't work with this bot)
   - Download the resulting JSON file, rename it to `client_secret.json`, and put it in this project folder

> **Important — do this before automating anything:** Google expires the login after just **7 days** for apps left in "Testing" status. That's fine while you're setting up, but it'll silently break a scheduled bot every week. Once you're happy with how it's working (after Step 5), go back to *OAuth consent screen* and click **Publish App** to move it to "In production." Since the app isn't Google-verified, you (and your brother) will see an "unverified app" warning during login — click **Advanced → Go to [your app name]** to continue. That's expected and safe; it's your own app. This is the standard, supported way to run a personal-use OAuth app long-term without going through Google's full review process, which exists for apps with many outside users, not this.

---

## Step 2 — Anthropic API key

1. Sign up or log in at **console.anthropic.com**
2. Add a payment method under *Settings → Billing* (API usage is pay-as-you-go, billed by tokens — see Costs below, it's cheap for this use case)
3. Go to *Settings → API Keys → Create Key*, copy it immediately (it's only shown once)

---

## Step 3 — Install

```bash
cd youtube-comment-bot
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and paste in your Anthropic key:

```
ANTHROPIC_API_KEY=sk-ant-your-real-key-here
```

---

## Step 4 — First run and authorization

```bash
python bot.py
```

A browser tab will open asking to log in — **this needs to be done by whoever's Google account owns the channel**, so grab your brother for a minute here. After granting access, a `token.json` file is created and future runs won't need this step again (until the 7-day thing in Step 1, if you skip publishing to production).

The bot ships with `DRAFT_MODE = True`, so this first run won't post anything — it'll write proposed replies to `draft_replies.txt` instead.

---

## Step 5 — Read the drafts, then tune `config.py`

Open `draft_replies.txt` and see what Claude would have said. Then open `config.py` and adjust:

- **`PERSONA`** — the most important one. Rewrite it in your brother's actual voice: his topic, his humor, things he'd never say. The default is a generic placeholder.
- **`FAQ_RESPONSES`** — instant, free, always-consistent answers for questions that show up on every video (equipment, location, etc.), bypassing Claude entirely.
- **`SKIP_KEYWORDS`** / **`MIN_COMMENT_LENGTH`** — what gets ignored.
- **`MAX_REPLIES_PER_RUN`** — safety ceiling per run.
- **`CLAUDE_MODEL`** — the default (`claude-haiku-4-5-20251001`) is fast and cheap; swap to `claude-sonnet-5` for more nuanced replies at a higher cost.

Re-run `python bot.py` as many times as you want while in draft mode — it's free-ish (just Claude API calls, no YouTube writes) and nothing goes live.

---

## Step 6 — Go live

Once the drafts consistently sound right, open `config.py` and set:

```python
DRAFT_MODE = False
```

Runs from now on post replies for real. Consider dropping `MAX_REPLIES_PER_RUN` to something small (like 5) for the first live run or two, just to watch it work before trusting it fully.

---

## Step 7 — Automate it (optional)

Right now you have to run `python bot.py` manually. To have it check automatically:

**Mac/Linux (cron)** — run `crontab -e` and add a line to check hourly:
```
0 * * * * cd /full/path/to/youtube-comment-bot && /usr/bin/python3 bot.py >> log.txt 2>&1
```

**Windows** — use Task Scheduler to run `python bot.py` on an hourly trigger, with "Start in" set to this folder.

Want it running even when your computer's off? That's doable with a free GitHub Actions scheduled workflow instead — just ask and I'll set that version up.

---

## Costs

**YouTube Data API** — free, but quota-limited: 10,000 units/day by default. Listing comments costs ~1 unit/call; posting a reply costs 50 units. That's roughly **150-200 replies/day** comfortably within the free daily quota. You can request a higher quota from Google at no charge if you outgrow it.

**Anthropic API** — pay-as-you-go. `claude-haiku-4-5-20251001` (the default) is $1 per million input tokens / $5 per million output tokens. A typical short reply runs a small fraction of a cent, so even a very active channel replying to hundreds of comments a month should land well under a few dollars. Exact current pricing: see console.anthropic.com's pricing page, since rates can change.

---

## Good practices (and staying on YouTube's good side)

YouTube's spam policy targets comments that are generic, repetitive, templated, or trying to drive traffic off-platform — not thoughtful automated replies. To stay clearly on the right side of that:

- Keep `DRAFT_MODE` on until you trust the persona
- Write a `PERSONA` that produces genuinely varied, specific replies — not "Thanks for watching!" on repeat
- Don't set `MAX_REPLIES_PER_RUN` sky-high; a steady trickle looks (and is) more human than a burst of 100 replies at once
- Skip anything that could sound like it's making promises on your brother's behalf — the default persona already guards against this, keep that guardrail if you customize it

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `invalid_grant` / login keeps expiring weekly | You're still in "Testing" publishing status — see the callout in Step 1 |
| `403 quotaExceeded` | Hit the daily YouTube API cap; resets at midnight Pacific time, or request more quota (free) from Google |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again, make sure you're using the same Python you're running the bot with |
| `FileNotFoundError: client_secret.json` | You haven't downloaded/renamed/placed the OAuth credentials file from Step 1 yet |
| Bot doesn't see a brand-new comment | It can take YouTube a few minutes to index new comments through the API — try again shortly |

---

Questions, want the GitHub Actions version, or want help writing the persona to actually sound like your brother? Just ask.
