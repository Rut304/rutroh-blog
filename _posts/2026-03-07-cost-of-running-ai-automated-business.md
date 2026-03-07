---
layout: post
title: "What I Actually Spend Running an AI-Automated Business (Monthly Breakdown)"
date: 2026-03-07 14:00:00 -0600
categories: [AI, Business, Automation]
---

People keep asking me what it costs to run a business where AI agents do most of the work. The answer is less than you'd think, but more than zero — and the breakdown might surprise you.

I track every dollar that goes toward keeping this operation running. Here's the real numbers from February 2026.

## The Stack

My setup is a Mac Mini M4 Pro sitting on my desk running 24/7. Eight AI agents handle different jobs — content creation, research, revenue tracking, video production, security monitoring. They talk to each other through a framework called OpenClaw and I manage the whole thing through Telegram on my phone.

The agents are not magic. They break, they produce garbage sometimes, and they need babysitting. But on a good day, they handle work that would take me 6-8 hours if I did it myself.

## Fixed Monthly Costs

**AI API Calls: ~$120-180/month**

This is the big one. The agents make API calls to generate content, analyze data, write code, and run quality checks. I use a tiered system — simple tasks go to cheap or free models (Gemini Flash), normal work goes to mid-tier models (Gemini Pro), and only the hard stuff touches the expensive models (Claude Opus).

Before I set up tiering, I was burning through $300+ a month because every little task used the most expensive model available. Don't make that mistake.

**Hosting: $0/month**

The Mac Mini runs as the server. The blog is hosted on GitHub Pages (free). Substack handles the newsletter (free until you get paid subscribers, then they take 10%). The AI gateway runs locally. No AWS bill. No cloud server rental.

**Domains: ~$12/year (so ~$1/month)**

One custom domain. That's it.

**Software Subscriptions: ~$20/month**

Cursor Pro for when I need to write or debug code myself. Everything else is either free or open source. Ollama for local models. Playwright for browser automation. FFmpeg for video processing. All free.

**Total fixed: roughly $140-200/month.**

## Variable Costs

**Content: $0**

The agents write the blog posts, the newsletter, and the social media content. I review and edit, but the raw production is automated. This used to be the thing I spent the most TIME on — now it takes maybe 30 minutes a day to review what the agents produced.

**Video Production: ~$0-15/month**

Thumbnail generation is free (local AI). Video assembly is free (FFmpeg). The only cost is if I use a paid voice API, which I've mostly replaced with free alternatives. Text-to-speech has gotten surprisingly good at the open-source level.

**Affiliate Program Fees: $0**

Amazon Associates and SaaS affiliate programs are free to join. You just need to be accepted and then maintain activity.

## Revenue Streams (What Actually Makes Money)

Here's the revenue side of the equation. These are the five streams I'm building, in order of how soon they can produce income:

**1. Amazon Affiliate Blog: $0-500/month potential**

Blog posts with affiliate links to products I actually use and recommend. Each post is a permanent asset — once it's published and indexed, it earns commissions every time someone clicks through and buys something. The Mac Mini review I published pulled in its first commission within 48 hours.

The math is straightforward: a $50 product at 4% commission = $2 per sale. But a well-ranked blog post can generate dozens of sales per month for years. Compound that across 20-30 posts and you've got real income.

**2. YouTube Shorts: $0-2,000/month potential**

Faceless AI-generated short videos. The content is genuinely funny (or at least I think so — the quality bar is high enough that I refuse to upload anything mediocre). Revenue comes from the YouTube Shorts Fund and eventually from channel monetization once we hit the subscribers and watch hours thresholds.

**3. Paid Newsletter: $0-500/month potential**

Weekly AI automation insights on Substack. Free tier builds the audience, paid tier ($5/month) offers deeper analysis. The economics are simple — 100 paid subscribers = $450/month after Substack's cut.

**4. AI Tool Affiliate Reviews: $0-2,000/month potential**

SaaS products pay 20-50% RECURRING commissions. That means if someone signs up for a $20/month tool through my review, I earn $4-10 every month they stay subscribed. One good review driving 10 signups can generate $40-100/month in passive recurring income.

This one has the best long-term math of anything I'm doing.

**5. Digital Products: $0-1,000/month potential**

Templates and configurations from my own setup, packaged for other people to use. The OpenClaw agent config that runs my business, the content quality pipeline, the video automation scripts — all productized and sold for $19-29 on Gumroad.

## The Real P&L

Here's what February looked like with numbers rounded:

| Category | Amount |
|----------|--------|
| API Costs | -$165 |
| Software | -$20 |
| Hardware (amortized) | -$55 |
| **Total Costs** | **-$240** |
| Blog Commissions | +$12 |
| Newsletter | +$0 |
| YouTube | +$0 |
| Digital Products | +$0 |
| **Total Revenue** | **+$12** |
| **Net** | **-$228** |

Yeah, it's negative. I'm not going to pretend this is a cash cow yet. Month one of any business is going to be in the red. The infrastructure is built, the content pipeline is running, the quality gates are in place. March should look different because I now have 5 blog posts live (some already ranking), videos queued for upload, and the newsletter launching.

The goal is breakeven by month 2-3 and $500+/month profit by month 6.

## What I'd Do Differently

If I started over knowing what I know now:

1. **Start with the blog immediately.** Every day without affiliate-linked content published is revenue left on the table. I spent too long building infrastructure before publishing anything.

2. **Don't use the most expensive AI model for everything.** Set up model tiering from day one. Your simple tasks don't need a $75/MTok output model.

3. **Quality matters more than quantity.** One genuinely great blog post outperforms ten mediocre ones. I had agents cranking out thin 300-word posts that ranked for nothing. Now everything goes through a humanizer and quality check — longer, more detailed, actually useful.

4. **The agents need guardrails.** Without explicit rules, they'll post promotional content to your personal accounts, use sales language that screams "AI wrote this," and make your brand look like a spam operation. I learned this the hard way and now have strict content separation rules.

## The Hardware Foundation

Everything runs on this:

- [Mac Mini M4 Pro](https://www.amazon.com/dp/B0DLHZM8GR/?tag=1705d0-20) — the brain of the operation
- [Dell 4K Monitor](https://www.amazon.com/dp/B09DTDRJWP/?tag=1705d0-20) — for when I need to review things on a real screen
- [CyberPower UPS](https://www.amazon.com/dp/B000FBK3QK/?tag=1705d0-20) — because Texas power grid

That's about $2,000 in hardware, total. Compare that to paying a human assistant $4,000/month and the ROI math is obvious — even if the AI agents are less reliable (they are), the cost per hour of useful work is dramatically lower.

*Disclosure: This post contains Amazon affiliate links. I earn a small commission on qualifying purchases at no extra cost to you.*
