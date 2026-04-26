#!/usr/bin/env python3
"""
generate.py — Static site generator for robrui.github.io.

Processes Markdown drafts in drafts/ and generates HTML in posts/NAME/index.html.
Also auto-updates blog/index.html with new entries.

Usage:
    python3 generate.py          # Process all drafts
    python3 generate.py --watch  # Watch for changes (requires watchdog)

Dependencies:
    pip install markdown
"""

import argparse
import os
import re
import glob
import json
from datetime import datetime

try:
    import markdown
    HAS_MD = True
except ImportError:
    HAS_MD = False

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
DRAFTS_DIR = os.path.join(SITE_ROOT, "drafts")
POSTS_DIR = os.path.join(SITE_ROOT, "posts")
BLOG_FILE = os.path.join(SITE_ROOT, "blog", "index.html")
ASSETS_DIR = os.path.join(SITE_ROOT, "assets")

BLOG_TEMPLATE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog — Robert Ruidisch</title>
  <meta name="description" content="Deep-dive articles on open-source contributions by Robert Ruidisch.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/style.css">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='28' font-size='28'>🐙</text></svg>">
</head>
<body>
<nav>
  <div class="container">
    <a href="../" class="logo"><span>r</span>obrui</a>
    <div class="nav-links">
      <a href="../">Home</a>
      <a href="../projects/">Contributions</a>
      <a href="./" class="active">Blog</a>
    </div>
  </div>
</nav>
<section class="hero" style="padding-bottom: 32px;">
  <div class="container-wide container">
    <h1>Deep-Dive <span>Blog</span></h1>
    <p class="subtitle">Behind every PR is a story — the science, the debugging, the fix.</p>
  </div>
</section>
<section class="section" style="padding-top: 0;">
  <div class="container-wide container">
    <ul class="blog-list">
"""

BLOG_TEMPLATE_TAIL = """    </ul>
  </div>
</section>
<footer>
  <div class="container">
    <div class="social-links">
      <a href="https://github.com/robrui">GitHub</a>
      <a href="https://www.linkedin.com/in/robert-ruidisch/">LinkedIn</a>
      <a href="mailto:robert.ruidisch@gmail.com">Email</a>
    </div>
    <p>© 2025 Robert Ruidisch</p>
  </div>
</footer>
</body>
</html>
"""


def parse_frontmatter(text):
    """Parse YAML-like front matter from markdown."""
    meta = {
        "title": "Untitled",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": [],
        "pr": "",
        "excerpt": "",
        "thumbnail": "",
        "read_time": 10,
    }
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip().lower()
                    value = value.strip().strip('"\'')
                    if key == "tags":
                        meta["tags"] = [t.strip() for t in value.split(",")]
                    elif key == "read_time":
                        meta["read_time"] = int(value)
                    else:
                        meta[key] = value
            return meta, parts[2].strip()
    return meta, text


def md_to_html(md_text):
    """Convert markdown to HTML."""
    if HAS_MD:
        return markdown.markdown(md_text, extensions=["fenced_code", "codehilite", "tables"])
    else:
        # Basic fallback
        return "<p>" + md_text.replace("\n\n", "</p><p>") + "</p>"


def generate_post(draft_file):
    """Generate a single post from a markdown draft."""
    with open(draft_file, "r") as f:
        text = f.read()

    meta, body_md = parse_frontmatter(text)
    slug = os.path.splitext(os.path.basename(draft_file))[0]
    post_dir = os.path.join(POSTS_DIR, slug)
    os.makedirs(post_dir, exist_ok=True)

    body_html = md_to_html(body_md)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta['title']} — Robert Ruidisch</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/style.css">
  <script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},options:{{enableMenu:false}}}};</script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script>hljs.highlightAll();</script>
</head>
<body>
<nav>
  <div class="container">
    <a href="../../" class="logo"><span>r</span>obrui</a>
    <div class="nav-links">
      <a href="../../">Home</a>
      <a href="../../projects/">Contributions</a>
      <a href="../../blog/">Blog</a>
    </div>
  </div>
</nav>
<article>
<header class="post-header">
  <div class="container-narrow container">
    <div class="post-label">📝 Deep-Dive</div>
    <h1>{meta['title']}</h1>
    <div class="post-meta">
      <span>{meta['pr']}</span>
      &nbsp;·&nbsp; <span>{meta['date']}</span>
      &nbsp;·&nbsp; <span>~{meta['read_time']} min read</span>
    </div>
  </div>
</header>
<div class="post-content">
  <div class="container-narrow container">
    {body_html}
    <hr style="margin: 48px 0; border: none; border-top: 1px solid var(--border);">
    <p style="text-align: center; color: var(--muted); font-size: 0.9rem;">
      <em>Found this useful?</em> · <a href="https://github.com/robrui">Follow on GitHub</a>
    </p>
  </div>
</div>
</article>
<footer>
  <div class="container">
    <div class="social-links">
      <a href="https://github.com/robrui">GitHub</a>
      <a href="https://www.linkedin.com/in/robert-ruidisch/">LinkedIn</a>
      <a href="mailto:robert.ruidisch@gmail.com">Email</a>
    </div>
    <p>© 2025 Robert Ruidisch</p>
  </div>
</footer>
</body>
</html>"""

    out_path = os.path.join(post_dir, "index.html")
    with open(out_path, "w") as f:
        f.write(html)

    return meta, slug


def rebuild_blog_index(entries):
    """Rebuild blog/index.html from sorted entries."""
    entries.sort(key=lambda e: e["date"], reverse=True)

    items = []
    for e in entries:
        thumbnail = e.get("thumbnail", "")
        thumb_html = f'<a href="../posts/{e["slug"]}/" class="blog-thumb"><img src="../{thumbnail}" loading="lazy"></a>' if thumbnail else ""

        tags_html = "".join(f'<span class="tag">{t}</span>' for t in e.get("tags", []))

        pr_link = f'<a href="https://github.com/{e["pr"]}" style="color:var(--accent);text-decoration:none;">{e["pr"]}</a>' if e.get("pr") else ""

        items.append(f"""      <li class="blog-entry">
        {thumb_html}
        <div class="blog-info">
          <h3><a href="../posts/{e["slug"]}/">{e["title"]}</a></h3>
          <div class="blog-meta">
            <span>📅 {e["date"]}</span>
            <span>⏱ ~{e["read_time"]} min</span>
            {f'<span>🔧 {pr_link}</span>' if pr_link else ''}
          </div>
          <p class="blog-excerpt">{e.get("excerpt", "")}</p>
          <div class="blog-tags">{tags_html}</div>
        </div>
      </li>""")

    with open(BLOG_FILE, "w") as f:
        f.write(BLOG_TEMPLATE_HEAD)
        f.write("\n".join(items) + "\n")
        f.write(BLOG_TEMPLATE_TAIL)


def process_all():
    """Process all drafts."""
    if not os.path.exists(DRAFTS_DIR):
        print("No drafts/ directory found.")
        return

    draft_files = sorted(glob.glob(os.path.join(DRAFTS_DIR, "*.md")))
    entries = []

    for df in draft_files:
        meta, slug = generate_post(df)
        meta["slug"] = slug
        entries.append(meta)
        print(f"  ✓ {slug}")

    if entries:
        rebuild_blog_index(entries)
        print(f"\nBlog index updated with {len(entries)} entries.")
    else:
        print("No drafts to process.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML from Markdown drafts")
    parser.add_argument("--watch", action="store_true", help="Watch for file changes")
    args = parser.parse_args()

    if args.watch:
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler

            class DraftHandler(FileSystemEventHandler):
                def on_modified(self, event):
                    if event.src_path.endswith(".md"):
                        print(f"Change detected: {event.src_path}")
                        process_all()

            observer = Observer()
            os.makedirs(DRAFTS_DIR, exist_ok=True)
            observer.schedule(DraftHandler(), DRAFTS_DIR, recursive=False)
            observer.start()
            print(f"Watching {DRAFTS_DIR} for changes... (Ctrl+C to stop)")
            try:
                observer.join()
            except KeyboardInterrupt:
                observer.stop()
            observer.join()
        except ImportError:
            print("watchdog not installed. Run: pip install watchdog")
            process_all()
    else:
        process_all()
