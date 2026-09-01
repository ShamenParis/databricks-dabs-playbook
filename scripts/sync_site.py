#!/usr/bin/env python3
"""
Databricks DABs Playbook — Automated Site Generator

This script scans the repository for learning modules and enterprise scenarios,
parses their README files and metadata, and automatically generates/updates the
Jekyll site files inside the `site/` directory.

Run this script anytime you add a new module or scenario:
    python scripts/sync_site.py
"""

import os
import re
import glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_DIR = os.path.join(REPO_ROOT, "site")
GITHUB_REPO_URL = "https://github.com/ShamenParis/databricks-dabs-playbook"


def parse_root_readme():
    """Parse the root README.md to extract module metadata (descriptions & tech stacks)."""
    readme_path = os.path.join(REPO_ROOT, "README.md")
    if not os.path.exists(readme_path):
        return {}, {}

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    learning_meta = {}
    scenario_meta = {}

    # Parse Learning Index table: | [01. Introduction to DABs](./learning/01-introduction-to-dab) | Description | Tech Stack |
    learning_table_matches = re.findall(
        r"\|\s*\[([^\]]+)\]\(\./learning/([^)]+)\)\s*\|\s*([^|]+)\|\s*([^|]+)\|", content
    )
    for title, folder, desc, tech in learning_table_matches:
        tags = [t.strip() for t in tech.strip().split(",") if t.strip()]
        learning_meta[folder.strip()] = {
            "title": title.strip(),
            "desc": desc.strip(),
            "tags": tags
        }

    # Parse Scenario Index table: | [01. Automate...](./scenarios/01-automate...) | Description | Tech Stack |
    scenario_table_matches = re.findall(
        r"\|\s*\[([^\]]+)\]\(\./scenarios/([^)]+)\)\s*\|\s*([^|]+)\|\s*([^|]+)\|", content
    )
    for title, folder, desc, tech in scenario_table_matches:
        tags = [t.strip() for t in tech.strip().split(",") if t.strip()]
        scenario_meta[folder.strip()] = {
            "title": title.strip(),
            "desc": desc.strip(),
            "tags": tags
        }

    return learning_meta, scenario_meta


def transform_image_paths(content, module_folder):
    """Replace relative image/doc links with site.baseurl Jekyll tags."""
    # Fix typo double extension
    content = content.replace("01-architecture-diagram.png.png", "01-architecture-diagram.png")

    # Replace relative paths to docs/learning/
    content = re.sub(
        r"\!\[(.*?)\]\(\.\./\.\./docs/learning/([^)]+)\)",
        r"![\1]({{ site.baseurl }}/images/learning/\2)",
        content
    )
    content = re.sub(
        r"\!\[(.*?)\]\(\.\./\.\./docs/learning/00-initial-setup/([^)]+)\)",
        r"![\1]({{ site.baseurl }}/images/learning/00-initial-setup/\2)",
        content
    )

    # Replace relative prerequisites links
    content = re.sub(
        r"\[Prerequisites and Local Setup\]\(\.\./\.\./docs/learning/00-initial-setup/README\.md\)",
        r"> Complete the [Prerequisites and Local Setup]({{ site.baseurl }}/prerequisites) before continuing.",
        content
    )

    # Replace downloads links to github raw
    content = re.sub(
        r"\[([^\]]+)\]\(\.\./\.\./docs/downloads/([^)]+)\)",
        rf"[\1]({GITHUB_REPO_URL}/raw/main/docs/downloads/\2)",
        content
    )

    # Escape raw liquid tags if present (e.g. {{tasks.task_a.values.target_table}})
    content = re.sub(r"(\{\{\s*tasks\.[^}]+\}\})", r"{% raw %}\1{% endraw %}", content)

    return content


def sync_learning_modules(root_learning_meta):
    """Generate site/learning/*.md files for all learning modules."""
    learning_dir = os.path.join(REPO_ROOT, "learning")
    out_dir = os.path.join(SITE_DIR, "learning")
    os.makedirs(out_dir, exist_ok=True)

    modules = []
    subdirs = sorted([d for d in os.listdir(learning_dir) if os.path.isdir(os.path.join(learning_dir, d))])

    for i, folder in enumerate(subdirs, start=1):
        readme_path = os.path.join(learning_dir, folder, "README.md")
        if not os.path.exists(readme_path):
            continue

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        meta = root_learning_meta.get(folder, {})
        title = meta.get("title", folder.replace("-", " ").title())
        desc = meta.get("desc", "")
        tags = meta.get("tags", ["DABs", "YAML", "Python"])

        # Extract title from README first line if possible
        first_line = content.split("\n")[0]
        match_h1 = re.match(r"^#\s*(\d+:\s*)?(.*)", first_line)
        header_title = match_h1.group(2).strip() if match_h1 else title

        transformed = transform_image_paths(content, folder)

        # Remove the first H1 line since we will render it cleanly below front matter
        lines = transformed.split("\n")
        if lines and lines[0].startswith("# "):
            lines = lines[1:]
        body = "\n".join(lines).strip()

        source_url = f"{GITHUB_REPO_URL}/tree/main/learning/{folder}"
        page_md = f"""---
layout: default
title: "{title}"
parent: Learning Modules
nav_order: {i}
permalink: /learning/{folder}
---

# {first_line.replace('# ', '')}

<a href="{source_url}" class="btn-source" target="_blank">📂 View Source Code</a>

---

{body}
"""
        out_file = os.path.join(out_dir, f"{folder}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(page_md)

        modules.append({
            "num": f"{i:02d}",
            "folder": folder,
            "title": title,
            "header_title": header_title,
            "desc": desc,
            "tags": tags,
            "permalink": f"/learning/{folder}"
        })

    return modules


def sync_scenarios(root_scenario_meta):
    """Generate site/scenarios/*.md files for all scenario modules."""
    scenarios_dir = os.path.join(REPO_ROOT, "scenarios")
    out_dir = os.path.join(SITE_DIR, "scenarios")
    os.makedirs(out_dir, exist_ok=True)

    scenarios = []
    subdirs = sorted([d for d in os.listdir(scenarios_dir) if os.path.isdir(os.path.join(scenarios_dir, d))])

    for i, folder in enumerate(subdirs, start=1):
        readme_path = os.path.join(scenarios_dir, folder, "README.md")
        if not os.path.exists(readme_path):
            continue

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        meta = root_scenario_meta.get(folder, {})
        title = meta.get("title", folder.replace("-", " ").title())
        desc = meta.get("desc", "")
        tags = meta.get("tags", ["DABs", "YAML", "Python"])

        # Image path fixes for scenario 02
        if folder == "02-enterprise-databricks-orchestration":
            content = re.sub(
                r"\!\[(.*?)\]\(\./docs/([^)]+)\)",
                r"![\1]({{ site.baseurl }}/scenario-02-images/\2)",
                content
            )

        source_url = f"{GITHUB_REPO_URL}/tree/main/scenarios/{folder}"
        # Inject View Source Code button after first heading
        lines = content.split("\n")
        h1 = lines[0] if lines else f"# {title}"
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

        page_md = f"""---
layout: default
title: "{title}"
parent: Enterprise Scenarios
nav_order: {i}
permalink: /scenarios/{folder}
---

{h1}

<a href="{source_url}" class="btn-source" target="_blank">📂 View Source Code</a>

---

{body}
"""
        out_file = os.path.join(out_dir, f"{folder}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(page_md)

        scenarios.append({
            "num": f"{i:02d}",
            "folder": folder,
            "title": title,
            "desc": desc,
            "tags": tags,
            "permalink": f"/scenarios/{folder}"
        })

    return scenarios


def count_resource_types():
    """Dynamically count supported resource types from Jinja2 templates in Scenario 01."""
    templates_dir = os.path.join(
        REPO_ROOT, "scenarios", "01-automate-databricks-resources-creation", "src", "templates"
    )
    if os.path.exists(templates_dir):
        templates = [f for f in os.listdir(templates_dir) if f.endswith("_template.jinja2")]
        return len(templates)
    return 7


def generate_homepage(modules, scenarios):
    """Generate site/index.md with dynamic cards and updated stats counters."""
    num_resource_types = count_resource_types()

    cards_learning = []
    for m in modules:
        tags_html = "".join([f'<span class="tag">{t}</span>' for t in m["tags"]])
        cards_learning.append(f"""<a href="{{{{ site.baseurl }}}}{m['permalink']}" class="module-card">
  <div class="card-number">Module {m['num']}</div>
  <div class="card-title">{m['title']}</div>
  <div class="card-desc">{m['desc']}</div>
  <div class="card-tags">{tags_html}</div>
</a>""")

    cards_scenarios = []
    for s in scenarios:
        tags_html = "".join([f'<span class="tag">{t}</span>' for t in s["tags"]])
        cards_scenarios.append(f"""<a href="{{{{ site.baseurl }}}}{s['permalink']}" class="module-card">
  <div class="card-number">Scenario {s['num']}</div>
  <div class="card-title">{s['title']}</div>
  <div class="card-desc">{s['desc']}</div>
  <div class="card-tags">{tags_html}</div>
</a>""")

    index_md = f"""---
layout: default
title: Home
nav_order: 1
permalink: /
---

<div class="hero-section">
  <h1 class="hero-title">Databricks DABs Playbook</h1>
  <p class="hero-subtitle">Production-ready Declarative Automation Bundle templates — scenario-based learning, visual architectures, and copy-paste-ready code.</p>
</div>

<div class="stats-bar">
  <div class="stat">
    <div class="stat-number">{len(modules)}</div>
    <div class="stat-label">Learning Modules</div>
  </div>
  <div class="stat">
    <div class="stat-number">{len(scenarios)}</div>
    <div class="stat-label">Enterprise Scenarios</div>
  </div>
  <div class="stat">
    <div class="stat-number">{num_resource_types}+</div>
    <div class="stat-label">Resource Types</div>
  </div>
</div>

## What's Inside

- **Visual Architectures:** Diagram-first approach for every scenario.
- **Production Code:** Copy-paste-ready `databricks.yml` and project files.
- **Cost Optimisation:** Built-in best practices for compute configurations.

---

<div class="section-header">
  <h2>Learning Modules</h2>
</div>

Start from zero and build your way up to advanced DAB orchestration patterns.

<div class="module-grid">

{chr(10).join(cards_learning)}

</div>

---

<div class="section-header">
  <h2>Enterprise Scenarios</h2>
</div>

Production-grade, real-world deployment patterns.

<div class="module-grid">

{chr(10).join(cards_scenarios)}

</div>

---

<div class="author-section">
  <img src="{{{{ site.baseurl }}}}/images/learning/00-initial-setup/mvp_logo.svg" alt="Shamen Paris" class="author-logo">
  <div class="author-info">
    <div class="author-name">Shamen Paris</div>
    <div class="author-title">Databricks MVP | Data & AI Consultant</div>
    <div class="author-links">
      <a href="https://medium.com/@shamen1209">Medium Articles</a>
      <a href="https://www.youtube.com/@shamnix_data_and_ai">YouTube Channel</a>
    </div>
  </div>
</div>
"""
    out_file = os.path.join(SITE_DIR, "index.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(index_md)


def generate_learning_index(modules):
    """Generate site/learning/index.md."""
    rows = []
    for m in modules:
        tags_str = ", ".join(m["tags"])
        rows.append(
            f"| {m['num']} | [{m['title']}]({{{{ site.baseurl }}}}{m['permalink']}) | {m['desc']} | {tags_str} |"
        )

    content = f"""---
layout: default
title: Learning Modules
nav_order: 3
has_children: true
has_toc: false
permalink: /learning/
---

# Learning Modules

Structured learning modules for Databricks Asset Bundles (DABs). Each module builds on the previous one, starting from a basic "Hello World" deployment and progressing to advanced workflow orchestration patterns.

> **Before you begin**, make sure you've completed the [Prerequisites and Local Setup]({{{{ site.baseurl }}}}/prerequisites).

---

| # | Module | Description | Tech Stack |
| :--- | :--- | :--- | :--- |
{chr(10).join(rows)}
"""
    out_file = os.path.join(SITE_DIR, "learning", "index.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)


def generate_scenarios_index(scenarios):
    """Generate site/scenarios/index.md."""
    rows = []
    for s in scenarios:
        tags_str = ", ".join(s["tags"])
        rows.append(
            f"| {s['num']} | [{s['title']}]({{{{ site.baseurl }}}}{s['permalink']}) | {s['desc']} | {tags_str} |"
        )

    content = f"""---
layout: default
title: Enterprise Scenarios
nav_order: 4
has_children: true
has_toc: false
permalink: /scenarios/
---

# Enterprise Scenarios

Real-world deployment scenarios built with Databricks Asset Bundles (DABs). Each scenario is self-contained and production-grade.

---

| # | Scenario | Description | Tech Stack |
| :--- | :--- | :--- | :--- |
{chr(10).join(rows)}

---

More scenarios coming soon covering:

- **Governance and Security:** Unity Catalog, Data Sharing, and securing production workloads.
- **Orchestration:** Databricks Jobs and advanced Workflows.
- **Data Engineering and ML:** Delta Live Tables (DLT) and MLOps on Databricks.
- **Automation:** CI/CD pipelines tailored for Databricks environments.
"""
    out_file = os.path.join(SITE_DIR, "scenarios", "index.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)


def sync_images():
    """Copy all image and media assets into site/ to ensure robust cross-platform rendering."""
    import shutil

    # 1. Sync docs/ -> site/images/
    docs_src = os.path.join(REPO_ROOT, "docs")
    images_dst = os.path.join(SITE_DIR, "images")
    if os.path.exists(docs_src):
        if os.path.islink(images_dst):
            os.unlink(images_dst)
        elif os.path.exists(images_dst):
            shutil.rmtree(images_dst)
        shutil.copytree(docs_src, images_dst)

    # 2. Sync scenario 02 docs -> site/scenario-02-images/
    scen02_src = os.path.join(REPO_ROOT, "scenarios", "02-enterprise-databricks-orchestration", "docs")
    scen02_dst = os.path.join(SITE_DIR, "scenario-02-images")
    if os.path.exists(scen02_src):
        if os.path.islink(scen02_dst):
            os.unlink(scen02_dst)
        elif os.path.exists(scen02_dst):
            shutil.rmtree(scen02_dst)
        shutil.copytree(scen02_src, scen02_dst)

    # Remove any leftover .md files in site/images to prevent Jekyll from creating duplicate pages
    for root_path, _, files in os.walk(images_dst):
        for f in files:
            if f.endswith(".md"):
                os.remove(os.path.join(root_path, f))

    print("✅ Synced all image and media assets to site/images/ and site/scenario-02-images/")



def main():
    print("🚀 Auto-syncing site content from repository code & READMEs...")
    learning_meta, scenario_meta = parse_root_readme()

    sync_images()

    modules = sync_learning_modules(learning_meta)
    print(f"✅ Generated {len(modules)} learning module pages in site/learning/")

    scenarios = sync_scenarios(scenario_meta)
    print(f"✅ Generated {len(scenarios)} scenario pages in site/scenarios/")

    generate_homepage(modules, scenarios)
    print("✅ Updated site/index.md (Homepage with dynamic cards & stats)")

    generate_learning_index(modules)
    print("✅ Updated site/learning/index.md")

    generate_scenarios_index(scenarios)
    print("✅ Updated site/scenarios/index.md")

    print("\n🎉 Site sync complete!")



if __name__ == "__main__":
    main()
