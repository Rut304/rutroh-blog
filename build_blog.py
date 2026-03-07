#!/usr/bin/env python3
"""Convert Markdown posts in _posts/ to HTML files in blog/"""
import os, re, glob
from datetime import datetime


def md_to_html(text):
    """Simple markdown to HTML converter for blog posts."""
    lines = text.split('\n')
    html_lines = []
    in_list = False
    list_type = None

    for line in lines:
        stripped = line.strip()

        # Blank line
        if not stripped:
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            html_lines.append('')
            continue

        # Headers
        if stripped.startswith('### '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            html_lines.append(f'<h3>{inline(stripped[4:])}</h3>')
            continue
        if stripped.startswith('## '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            html_lines.append(f'<h2>{inline(stripped[3:])}</h2>')
            continue
        if stripped.startswith('# '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            html_lines.append(f'<h1>{inline(stripped[2:])}</h1>')
            continue

        # Horizontal rule
        if stripped in ('---', '***', '___'):
            html_lines.append('<hr>')
            continue

        # Unordered list
        if re.match(r'^[-*]\s', stripped):
            if not in_list or list_type != 'ul':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            html_lines.append(f'<li>{inline(stripped[2:])}</li>')
            continue

        # Ordered list
        m = re.match(r'^(\d+)\.\s', stripped)
        if m:
            if not in_list or list_type != 'ol':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            html_lines.append(f'<li>{inline(stripped[len(m.group(0)):])}</li>')
            continue

        # Regular paragraph
        if in_list:
            html_lines.append(f'</{list_type}>')
            in_list = False
            list_type = None
        html_lines.append(f'<p>{inline(stripped)}</p>')

    if in_list:
        html_lines.append(f'</{list_type}>')

    return '\n'.join(html_lines)


def inline(text):
    """Convert inline markdown: bold, italic, links, code."""
    # Links: [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code: `text`
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text

TEMPLATE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITLE_PLACEHOLDER — RutRoh Blog</title>
    <link rel="icon" type="image/png" href="../assets/logo.png">
    <style>
        :root {
            --bg: #0a0a0f;
            --surface: #12121a;
            --border: #1e1e2e;
            --text: #e0e0e8;
            --text-muted: #8888a0;
            --accent: #6c5ce7;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.8;
        }
        a { color: var(--accent); text-decoration: none; }
        a:hover { text-decoration: underline; }
        nav {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 16px;
        }
        nav img { height: 28px; }
        nav a { color: var(--text-muted); font-size: 0.85rem; }
        .container {
            max-width: 700px;
            margin: 0 auto;
            padding: 40px 20px 80px;
        }
        h1 { font-size: 1.6rem; margin-bottom: 8px; }
        .date { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 32px; display: block; }
        h2 { font-size: 1.2rem; margin: 32px 0 12px; }
        h3 { font-size: 1.05rem; margin: 24px 0 8px; }
        p { margin-bottom: 16px; color: var(--text-muted); }
        strong { color: var(--text); }
        ol, ul { margin: 0 0 16px 24px; color: var(--text-muted); }
        li { margin-bottom: 6px; }
        hr { border: none; border-top: 1px solid var(--border); margin: 32px 0; }
        em { color: var(--text-muted); font-size: 0.85rem; }
    </style>
</head>
<body>
    <nav>
        <a href="/"><img src="../assets/rutroh_long_logo.png" alt="RutRoh"></a>
        <a href="/">Home</a>
        <a href="/blog/">Blog</a>
    </nav>
    <div class="container">
        <h1>TITLE_PLACEHOLDER</h1>
        <span class="date">DATE_PLACEHOLDER</span>
"""

TEMPLATE_FOOT = """    </div>
</body>
</html>"""

posts = sorted(glob.glob('_posts/*.md'))
all_posts = []

for path in posts:
    with open(path) as f:
        content = f.read()

    title = ''
    date_str = ''
    if content.startswith('---'):
        parts = content.split('---', 2)
        fm = parts[1]
        body = parts[2].strip()
        m = re.search(r'title:\s*"(.+?)"', fm)
        if m:
            title = m.group(1)
        m = re.search(r'date:\s*(.+)', fm)
        if m:
            raw = m.group(1).strip()
            try:
                dt = datetime.strptime(raw[:19], '%Y-%m-%d %H:%M:%S')
                date_str = dt.strftime('%B %d, %Y')
            except Exception:
                date_str = raw[:10]
    else:
        body = content.strip()
        for line in body.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip()
                body = body.replace(line, '', 1).strip()
                break
        date_str = 'March 1, 2026'

    fname = os.path.basename(path)
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', fname.replace('.md', ''))

    html_body = md_to_html(body)

    page = TEMPLATE_HEAD.replace('TITLE_PLACEHOLDER', title).replace('DATE_PLACEHOLDER', date_str)
    page += html_body + '\n' + TEMPLATE_FOOT

    outpath = f'blog/{slug}.html'
    with open(outpath, 'w') as f:
        f.write(page)

    print(f'Created: {outpath}')

    desc = ''
    for line in body.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('*') and not line.startswith('---'):
            desc = line[:150]
            if len(line) > 150:
                desc += '...'
            break

    all_posts.append({
        'slug': slug,
        'title': title or slug.replace('-', ' ').title(),
        'date_str': date_str,
        'desc': desc,
    })

print('\n--- All posts (oldest to newest) ---')
for p in all_posts:
    print(f"{p['slug']} | {p['title']} | {p['date_str']}")
