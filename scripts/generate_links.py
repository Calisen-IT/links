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
with open("index.html", "w") as f:
    f.write("<h1>Short Links</h1><ul>")
    for short, url in sorted(generated_links):
        f.write(f'<li><a href="/{short}">{short}</a> → {url}</li>')
    f.write("</ul>")