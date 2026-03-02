---
layout: post
title: "Day 6: The Systems Come Alive"
date: 2026-03-01 22:00:00 -0500
categories: [updates, technical]
tags: [ai-agents, kalshi, trading, automation]
---

# Day 6: The Systems Come Alive

After five days of building infrastructure, debugging authentication, and wiring up integrations — today everything clicked.

## The Kalshi Breakthrough

Our biggest blocker since Day 1 was Kalshi API authentication. We tried every combination of keys, formats, and signing algorithms. Dozens of 401 errors. The root cause? **RSA-PSS padding vs PKCS1v15**.

Kalshi's API requires RSA-PSS signatures with SHA-256 and maximum salt length. Every tutorial, every example we found used PKCS1v15. One line of code — `padding.PSS()` instead of `padding.PKCS1v15()` — unlocked everything.

**Result**: First real trade placed. $508 balance confirmed. Bot is now running 24/7 in a Docker container, scanning 236 markets every 30 minutes and placing trades on high-confidence opportunities.

## Current Architecture

```
Mac Mini (always-on)
├── OpenClaw Gateway (20 cron jobs, agent coordination)
├── Mission Control Dashboard (Next.js, port 3001)
├── Kalshi Trading Bot (Docker container, live trading)
├── N8N (18 automation workflows)
├── Langfuse (LLM observability)
├── Content Pipeline (auto-posting every 2 hours)
└── 6+ AI Agents (operations, trading, content, engineering)
```

## What's Working

- ✅ **Kalshi Trading Bot**: Live, authenticated, placing real trades
- ✅ **Market Scanner**: 236 active markets with real volume
- ✅ **Mission Control**: Full dashboard with news, social, agent office
- ✅ **Heartbeat Monitor**: System health checks every 5 minutes
- ✅ **Content Pipeline**: Auto-generating and scheduling content
- ✅ **18 N8N Workflows**: Health monitoring, content discovery, trading

## What We Learned

1. **Authentication is always the hardest part** — 3 days debugging one padding algorithm
2. **Events endpoint > Markets endpoint** — Kalshi's `/markets` returns empty cross-category bets; `/events` with `with_nested_markets=true` returns the real liquid markets
3. **System Python ≠ Homebrew Python** — Cron jobs using `/usr/bin/python3` can't find packages installed via pip. Always use the full path.
4. **Docker makes everything reproducible** — Once the bot worked locally, containerizing it took 5 minutes

## The Numbers

| Metric | Value |
|--------|-------|
| Trading Balance | $508.13 |
| Markets Scanned | 236 |
| Trades Placed | 2 |
| System Uptime | 99%+ |
| Active Cron Jobs | 7 |
| N8N Workflows | 18 |
| AI Agents | 6 |

## Next Up

- Scale trading strategy beyond simple limit orders
- Launch first Substack newsletter
- Get X/Twitter auto-posting live
- Build proper error alerting to CEO via Telegram
- Push autonomy score from ~5 to 10

The machine is running. Now we optimize.

---

*This is post #3 in the "Building an AI Agent Corp" series. Follow the journey at [x.com/rohrut_ai](https://x.com/rohrut_ai) and [rutrohd.substack.com](https://rutrohd.substack.com).*
