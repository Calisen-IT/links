import os
import yaml
import shutil

LINKS_DIR = "links"
OUTPUT_DIR = "."

RESERVED = {".github", "scripts", "links", ".git"}

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="0; url={url}" />
    <script>window.location.href = "{url}";</script>
    <title>Redirecting...</title>
  </head>
  <body>
    <p>Redirecting to <a href="{url}">{url}</a></p>
  </body>
</html>
"""

generated_links = []

for file in os.listdir(LINKS_DIR):
    if not file.endswith(".yml"):
        continue

    with open(os.path.join(LINKS_DIR, file)) as f:
        data = yaml.safe_load(f)

    short = data.get("short")
    url = data.get("url")

    if not short or not url:
        raise Exception(f"Invalid file: {file}")

    if short in RESERVED:
        raise Exception(f"'{short}' is a reserved name")

    output_path = os.path.join(OUTPUT_DIR, short)

    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    os.makedirs(output_path, exist_ok=True)

    with open(os.path.join(output_path, "index.html"), "w") as f:
        f.write(HTML_TEMPLATE.format(url=url))

    generated_links.append((short, url))

    print(f"Generated: {short} → {url}")

# ============================
# Fully escaped INDEX_TEMPLATE
# (literal CSS/JS braces doubled per Python format rules) :contentReference[oaicite:1]{index=1}
# ============================

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Short Links</title>

  <script type="module">
    import 'https://esm.run/@material/web/all.js';
  </script>

  <!-- Fonts and Material Icons -->
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />

  <style>
    :root {{
      color-scheme: light dark;

      --md-sys-color-primary: #6750a4;
      --md-sys-color-on-primary: #ffffff;

      --md-sys-color-background: #fefbff;
      --md-sys-color-on-background: #1c1b1f;

      --md-sys-color-surface: #ffffff;
      --md-sys-color-on-surface: #1c1b1f;

      --snackbar-bg: rgba(0,0,0,0.85);
      --snackbar-text: #fff;
    }}

    @media (prefers-color-scheme: dark) {{
      :root {{
        --md-sys-color-background: #1c1b1f;
        --md-sys-color-on-background: #e6e1e5;

        --md-sys-color-surface: #2b2930;
        --md-sys-color-on-surface: #e6e1e5;

        --snackbar-bg: rgba(255,255,255,0.12);
        --snackbar-text: #e6e1e5;
      }}
    }}

    body {{
      font-family: 'Roboto', sans-serif;
      margin: 0;
      padding: 1rem;
      background: var(--md-sys-color-background);
      color: var(--md-sys-color-on-background);
    }}

    .container {{
      max-width: 800px;
      margin: auto;
    }}

    h1 {{
      margin-bottom: 1rem;
    }}

    .search {{
      margin-bottom: 1rem;
    }}

    input {{
      width: 100%;
      box-sizing: border-box;
      padding: 0.75rem;
      border-radius: 12px;
      border: none;
      outline: none;
      background: var(--md-sys-color-surface);
      color: var(--md-sys-color-on-surface);
      font-size: 1rem;
    }}

    .link-card {{
      margin: 0.5rem 0;
      padding: 0.75rem 1rem;
      border-radius: 16px;
      background: var(--md-sys-color-surface);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}

    .left {{
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      flex: 1;
    }}

    .actions {{
      display: flex;
      gap: 0.5rem;
      align-items: center;
    }}

    md-filled-button {{
      --md-filled-button-container-color: var(--md-sys-color-primary);
      --md-filled-button-label-text-color: var(--md-sys-color-on-primary);
      --md-filled-button-container-height: 40px;
    }}

    md-filled-tonal-icon-button {{
      --md-filled-tonal-icon-button-container-height: 40px;
      border-radius: 12px;
      background-color: var(--md-sys-color-primary);
      color: var(--md-sys-color-on-primary);
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    md-filled-tonal-icon-button md-icon {{
      color: var(--md-sys-color-on-primary);
    }}

    md-filled-tonal-icon-button:hover {{
      background-color: #533d8a;
    }}

    @media (prefers-color-scheme: dark) {{
      .link-card {{
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
      }}
    }}

    @media (max-width: 480px) {{
      .link-card {{
        flex-direction: column;
        align-items: stretch;
      }}

      .actions {{
        width: 100%;
        justify-content: space-between;
      }}

      md-filled-button {{
        flex: 1;
      }}
    }}

    /* Snackbar */
    #snackbar {{
      visibility: hidden;
      min-width: 240px;
      background-color: var(--snackbar-bg);
      color: var(--snackbar-text);
      text-align: center;
      border-radius: 8px;
      padding: 0.75rem 1rem;
      position: fixed;
      left: 50%;
      bottom: 24px;
      transform: translateX(-50%);
      font-size: 1rem;
      z-index: 9999;
    }}

    #snackbar.show {{
      visibility: visible;
      animation: fadein 0.25s, fadeout 0.25s 2s;
    }}

    @keyframes fadein {{
      from {{
        bottom: 0;
        opacity: 0;
      }}
      to {{
        bottom: 24px;
        opacity: 1;
      }}
    }}

    @keyframes fadeout {{
      from {{
        bottom: 24px;
        opacity: 1;
      }}
      to {{
        bottom: 0;
        opacity: 0;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Short Links</h1>

    <div class="search">
      <input id="search" placeholder="Search links..." />
    </div>

    <div id="list">
      {links}
    </div>
  </div>

  <div id="snackbar">Copied!</div>

  <script>
    const search = document.getElementById('search');
    search.addEventListener('input', () => {{
      const q = search.value.toLowerCase();
      document.querySelectorAll('.link-card').forEach(el => {{
        const text = el.dataset.name;
        el.style.display = text.includes(q) ? '' : 'none';
      }});
    }});

    function showSnackbar() {{
      const sb = document.getElementById('snackbar');
      sb.classList.add('show');
      setTimeout(() => sb.classList.remove('show'), 2300);
    }}

    function copyLink(path) {{
      const url = window.location.origin + '/' + path;
      navigator.clipboard.writeText(url).then(() => {{
        showSnackbar();
      }});
    }}
  </script>
</body>
</html>
"""

link_items = ""
for short, url in sorted(generated_links):
    link_items += f'''
    <div class="link-card" data-name="{short.lower()}">
      <div class="left">{short}</div>
      <div class="actions">
        <a href="/{short}">
          <md-filled-button>Open</md-filled-button>
        </a>
        <md-filled-tonal-icon-button aria-label="Copy link" onclick="copyLink('{short}')">
          <md-icon>content_copy</md-icon>
        </md-filled-tonal-icon-button>
      </div>
    </div>
    '''

with open("index.html", "w") as f:
    f.write(INDEX_TEMPLATE.format(links=link_items))