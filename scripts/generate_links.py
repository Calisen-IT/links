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

    # remove existing folder to avoid stale files
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    os.makedirs(output_path, exist_ok=True)

    with open(os.path.join(output_path, "index.html"), "w") as f:
        f.write(HTML_TEMPLATE.format(url=url))

    generated_links.append((short, url))

    print(f"Generated: {short} → {url}")

# optional: generate index page
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
    body {{
      font-family: 'Roboto', sans-serif;
      margin: 0;
      padding: 2rem;
      background: #fefbff;
    }}

    .container {{
      max-width: 800px;
      margin: auto;
    }}

    .link-card {{
      margin: 0.5rem 0;
      padding: 1rem;
      border-radius: 12px;
      background: white;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
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