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

# ✅ Material 3 + auto dark mode index
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Short Links</title>

  <script type="module">
    import 'https://esm.run/@material/web/all.js';
  </script>

  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">

  <style>
    :root {{
      color-scheme: light dark;

      --md-sys-color-primary: #6750a4;
      --md-sys-color-on-primary: #ffffff;

      --md-sys-color-background: #fefbff;
      --md-sys-color-on-background: #1c1b1f;

      --md-sys-color-surface: #ffffff;
      --md-sys-color-on-surface: #1c1b1f;
    }}

    @media (prefers-color-scheme: dark) {{
      :root {{
        --md-sys-color-primary: #d0bcff;
        --md-sys-color-on-primary: #381e72;

        --md-sys-color-background: #1c1b1f;
        --md-sys-color-on-background: #e6e1e5;

        --md-sys-color-surface: #2b2930;
        --md-sys-color-on-surface: #e6e1e5;
      }}
    }}

    body {{
      font-family: 'Roboto', sans-serif;
      margin: 0;
      padding: 2rem;
      background: var(--md-sys-color-background);
      color: var(--md-sys-color-on-background);
    }}

    .container {{
      max-width: 800px;
      margin: auto;
    }}

    .link-card {{
      margin: 0.5rem 0;
      padding: 1rem;
      border-radius: 12px;
      background: var(--md-sys-color-surface);
      color: var(--md-sys-color-on-surface);

      display: flex;
      justify-content: space-between;
      align-items: center;

      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}

    @media (prefers-color-scheme: dark) {{
      .link-card {{
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
      }}
    }}

    a {{
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Short Links</h1>
    {links}
  </div>
</body>
</html>
"""

link_items = ""
for short, url in sorted(generated_links):
    link_items += f'''
    <div class="link-card">
      <span>{short}</span>
      <a href="/{short}">
        <md-filled-button>Open</md-filled-button>
      </a>
    </div>
    '''

with open("index.html", "w") as f:
    f.write(INDEX_TEMPLATE.format(links=link_items))