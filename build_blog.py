#!/usr/bin/env python3
"""
Build blog — converts _posts/*.md to blog/*.html and regenerates blog/index.html.
Uses the shared stylesheet (assets/style.css) and consistent site-wide nav/footer.

Usage: python3 build_blog.py
"""
import html as html_mod
import math
import os
import re
import glob
from datetime import datetime


# ---------------------------------------------------------------------------
# Markdown → HTML converter
# ---------------------------------------------------------------------------

def md_to_html(text):
    """Convert markdown body text to HTML."""
    lines = text.split('\n')
    out = []
    in_list = False
    list_type = None
    in_code_block = False
    code_lines = []

    for line in lines:
        stripped = line.strip()

        # Fenced code blocks
        if stripped.startswith('```'):
            if in_code_block:
                out.append('<pre><code>' + html_mod.escape('\n'.join(code_lines)) + '</code></pre>')
                code_lines = []
                in_code_block = False
            else:
                if in_list:
                    out.append(f'</{list_type}>')
                    in_list = False
                    list_type = None
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Blank line
        if not stripped:
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
                list_type = None
            out.append('')
            continue

        # Headers
        for level, prefix in [(3, '### '), (2, '## '), (1, '# ')]:
            if stripped.startswith(prefix):
                if in_list:
                    out.append(f'</{list_type}>')
                    in_list = False
                out.append(f'<h{level}>{inline(stripped[len(prefix):])}</h{level}>')
                break
        else:
            # Horizontal rule
            if stripped in ('---', '***', '___'):
                out.append('<hr>')
                continue

            # Unordered list
            if re.match(r'^[-*]\s', stripped):
                if not in_list or list_type != 'ul':
                    if in_list:
                        out.append(f'</{list_type}>')
                    out.append('<ul>')
                    in_list = True
                    list_type = 'ul'
                out.append(f'<li>{inline(stripped[2:])}</li>')
                continue

            # Ordered list
            m = re.match(r'^(\d+)\.\s', stripped)
            if m:
                if not in_list or list_type != 'ol':
                    if in_list:
                        out.append(f'</{list_type}>')
                    out.append('<ol>')
                    in_list = True
                    list_type = 'ol'
                out.append(f'<li>{inline(stripped[len(m.group(0)):])}</li>')
                continue

            # Blockquote
            if stripped.startswith('> '):
                if in_list:
                    out.append(f'</{list_type}>')
                    in_list = False
                    list_type = None
                out.append(f'<blockquote>{inline(stripped[2:])}</blockquote>')
                continue

            # Regular paragraph
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
                list_type = None
            out.append(f'<p>{inline(stripped)}</p>')

    if in_list:
        out.append(f'</{list_type}>')
    if in_code_block:
        out.append('<pre><code>' + html_mod.escape('\n'.join(code_lines)) + '</code></pre>')

    return '\n'.join(out)


def inline(text):
    """Convert inline markdown: bold, italic, links, code, images."""
    # Images: ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
    # Links: [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code: `text`
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


def reading_time(text):
    """Estimate reading time in minutes."""
    words = len(text.split())
    return max(1, math.ceil(words / 250))


def extract_tag(categories):
    """Pick a short display tag from categories list."""
    tag_map = {
        'ai': 'AI', 'business': 'Business', 'automation': 'Automation',
        'hardware': 'Hardware', 'affiliate': 'Affiliate', 'gadgets': 'Gadgets',
        'setup': 'Setup', 'review': 'Review', 'tools': 'Tools',
        'revenue': 'Revenue',
    }
    for cat in categories:
        key = cat.strip().lower()
        if key in tag_map:
            return tag_map[key]
    return categories[0].strip() if categories else 'Post'


# ---------------------------------------------------------------------------
# Templates — uses shared assets/style.css
# ---------------------------------------------------------------------------

POST_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} &mdash; RutRoh Blog</title>
    <meta name="description" content="{description}">
    <link rel="icon" type="image/png" href="../assets/logo.png">
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <nav>
        <a href="/" class="logo">
            <img src="../assets/rutroh_long_logo.png" alt="RutRoh">
        </a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/phoebe/">Phoebe</a>
            <a href="/blog/" class="active">Blog</a>
        </div>
    </nav>

    <div class="article-container">
        <div class="article-header">
            <h1>{title}</h1>
            <div class="article-meta">
                <span class="date">{date}</span>
                <span class="author">RutRoh AI</span>
                <span class="reading-time">{read_time} min read</span>
            </div>
        </div>

        <div class="article-body">
{body}
        </div>

        <div class="article-footer">
            <a class="back-link" href="/blog/">&larr; All posts</a>
        </div>
    </div>

    <footer class="site-footer">
        <p>&copy; 2025-2026 RutRoh Inc.</p>
    </footer>
</body>
</html>"""


INDEX_TEMPLATE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog &mdash; RutRoh</title>
    <meta name="description" content="AI automation, affiliate revenue, and the real story of building an autonomous business.">
    <link rel="icon" type="image/png" href="../assets/logo.png">
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <nav>
        <a href="/" class="logo">
            <img src="../assets/rutroh_long_logo.png" alt="RutRoh">
        </a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/phoebe/">Phoebe</a>
            <a href="/blog/" class="active">Blog</a>
        </div>
    </nav>

    <div class="blog-container">
        <h1>Blog</h1>
        <p class="desc">Real talk about AI automation, making money with agents, and the tools that actually work.</p>

        <ul class="post-list">
"""

INDEX_TEMPLATE_FOOT = """        </ul>
    </div>

    <footer class="site-footer">
        <p>&copy; 2025-2026 RutRoh Inc.</p>
    </footer>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

posts = sorted(glob.glob('_posts/*.md'))
all_posts = []

for path in posts:
    with open(path) as f:
        content = f.read()

    title = ''
    date_str = ''
    categories = []

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
        m = re.search(r'categories:\s*\[(.+?)\]', fm)
        if m:
            categories = [c.strip() for c in m.group(1).split(',')]
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
    read_time = reading_time(body)
    html_body = md_to_html(body)

    # First non-header paragraph as description
    desc = ''
    for line in body.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('*') and not line.startswith('---') and not line.startswith('>'):
            desc = line[:160]
            if len(line) > 160:
                desc += '...'
            break

    page = POST_TEMPLATE.format(
        title=html_mod.escape(title),
        description=html_mod.escape(desc),
        date=date_str,
        read_time=read_time,
        body=html_body,
    )

    outpath = f'blog/{slug}.html'
    with open(outpath, 'w') as f:
        f.write(page)
    print(f'  {outpath}')

    all_posts.append({
        'slug': slug,
        'title': title or slug.replace('-', ' ').title(),
        'date_str': date_str,
        'desc': desc,
        'tag': extract_tag(categories),
    })

# ---------------------------------------------------------------------------
# Generate blog/index.html (newest first)
# ---------------------------------------------------------------------------

all_posts.reverse()

index_html = INDEX_TEMPLATE_HEAD
for p in all_posts:
    index_html += f"""            <li>
                <a href="{p['slug']}.html">
                    <div class="meta">
                        <span class="date">{p['date_str']}</span>
                        <span class="tag">{p['tag']}</span>
                    </div>
                    <h3>{html_mod.escape(p['title'])}</h3>
                    <p>{html_mod.escape(p['desc'])}</p>
                </a>
            </li>
"""
index_html += INDEX_TEMPLATE_FOOT

with open('blog/index.html', 'w') as f:
    f.write(index_html)

print(f'\n  blog/index.html ({len(all_posts)} posts)')
print(f'\nDone — {len(all_posts)} posts built.')
