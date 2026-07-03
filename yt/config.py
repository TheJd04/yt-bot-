"""
============================================================
 EVERYTHING IN THIS FILE IS SAFE TO EDIT.
 This is the only file you should need to touch day-to-day.
============================================================
"""

# ----------------------------------------------------------
# THE BOT'S VOICE
# ----------------------------------------------------------
# This gets sent to Claude before every comment. Rewrite it so it
# sounds like your brother, not like a generic customer support bot.
# Mention his channel topic, his sense of humor, things he'd never say.
PERSONA = """
You are replying to YouTube comments on behalf of a creator's channel.
The channel is about [FILL IN: e.g. "retro video game restoration"].

Voice & tone:
- Sound like a real person who makes this content, not a corporate bot.
- Friendly, appreciative, a little playful. Short and casual, like a
  real creator dashing off a quick reply between edits.
- 1-2 sentences max. Never write a paragraph.
- Use at most one emoji, and only if it fits naturally.

Hard rules:
- Never claim to be an AI, and never claim to be human either -- just
  reply naturally and don't bring it up.
- Never promise future videos, collabs, giveaways, or sponsorships.
- Never share personal contact info, links, or ask viewers to go
  "check my bio" / "DM me" / etc.
- If the comment asks something you can't possibly know (personal
  opinions only the creator would have, unreleased plans, etc.),
  write a short, warm, non-committal reply instead of guessing.
"""

# ----------------------------------------------------------
# INSTANT ANSWERS (skips Claude entirely for common questions)
# ----------------------------------------------------------
# If a comment contains the key (case-insensitive) as a substring,
# the matching reply is used as-is -- free, instant, and 100% consistent.
# Great for the questions you get on every single video.
# Leave the dict empty ({}) to disable this and always use Claude.
FAQ_RESPONSES = {
    # "what camera do you use": "Sony A7IV with a 24-70mm, thanks for asking!",
    # "where are you from": "Based in [city] -- glad you're here!",
}

# ----------------------------------------------------------
# WHICH CLAUDE MODEL GENERATES REPLIES
# ----------------------------------------------------------
# claude-haiku-4-5-20251001 -> fastest & cheapest, great for short replies
# claude-sonnet-5           -> more thoughtful/nuanced, costs more
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# ----------------------------------------------------------
# SAFETY SWITCHES
# ----------------------------------------------------------
# DRAFT_MODE = True:  the bot NEVER posts anything to YouTube. Instead it
#              writes every proposed reply to draft_replies.txt so you can
#              read them first. Start here. Always.
# DRAFT_MODE = False: the bot posts replies live, immediately, no review.
DRAFT_MODE = True

# Hard ceiling on how many replies get posted (or drafted) in one run.
# Keeps a single run from replying to your entire comment history at once,
# and helps you stay well under YouTube's API quota (see README).
MAX_REPLIES_PER_RUN = 20

# ----------------------------------------------------------
# WHAT TO SKIP
# ----------------------------------------------------------
# Comments containing any of these (case-insensitive) are skipped
# entirely -- no reply, no draft. Good for filtering obvious spam/links.
SKIP_KEYWORDS = [
    "http://",
    "https://",
    "www.",
    "check out my channel",
    "sub for sub",
    "subscribe to my",
]

# Comments shorter than this (characters) are skipped. Filters out
# "first!", "lol", "😂😂😂", etc. that don't really need a reply.
MIN_COMMENT_LENGTH = 6

# Only consider comments on videos published in the last N days.
# Set to None to consider comments on every video, regardless of age.
ONLY_RECENT_VIDEO_DAYS = None

# How many pages of the 50 most-recent channel comments to pull per run.
# 1 page = 50 comments. Raise this if the channel is very active and you
# run the bot infrequently; lower it to save API quota.
MAX_PAGES_PER_RUN = 3
