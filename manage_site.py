import os
import re
import json
from datetime import datetime

# --- Configuration ---
HOME_FILE = "index.md"
PROJECTS_JSON = "projects.json"
DATE_FORMAT = "%d/%m/%y"  # dd/mm/yy


def slugify(text):
    return text.lower().replace(" ", "_").replace("-", "_").strip("_")


def get_today():
    return datetime.now().strftime(DATE_FORMAT)


def status_class(status):
    return f"status-{status.lower()}"


def load_projects():
    if os.path.exists(PROJECTS_JSON):
        with open(PROJECTS_JSON, "r") as f:
            return json.load(f)
    return []


def save_projects(projects):
    with open(PROJECTS_JSON, "w") as f:
        json.dump(projects, f, indent=2)


def build_card(title, folder_name, blurb, start_date, last_edited, status):
    status_lower = status.lower()
    css_class = f"status-{status_lower}"
    status_label = status.capitalize()
    img_path = f"./{folder_name}/images/listImage.png"
    link = f"./{folder_name}"
    return (
        f'\n<div class="project-card">\n'
        f'  <a href="{link}" class="project-image-wrap">\n'
        f'    <img src="{img_path}" alt="{title}" onerror="this.closest(\'.project-image-wrap\').style.display=\'none\'">\n'
        f'  </a>\n'
        f'  <div class="project-meta">\n'
        f'    <h1><a href="{link}">{title}</a></h1>\n'
        f'    <p class="project-dates"><strong>Start Date:</strong> {start_date} &nbsp;·&nbsp; '
        f'<strong>Last Edited:</strong> {last_edited} &nbsp;·&nbsp; '
        f'<strong>Status:</strong> <span class="{css_class}">{status_label}</span></p>\n'
        f'    <p class="project-blurb">{blurb}</p>\n'
        f'  </div>\n'
        f'</div>\n'
    )


def update_home_page(title, folder_name, blurb, is_new=True, status="ongoing"):
    with open(HOME_FILE, "r") as f:
        content = f.read()

    today = get_today()
    link = f"./{folder_name}"

    if is_new:
        new_card = build_card(title, folder_name, blurb, today, today, status)
        # Insert at the top of the project list (after front matter if any)
        if content.startswith("---"):
            # Find end of front matter
            second_dashes = content.find("---", 3)
            if second_dashes != -1:
                insert_pos = second_dashes + 3
                content = content[:insert_pos] + "\n" + new_card + content[insert_pos:]
            else:
                content = new_card + content
        else:
            content = new_card + content
    else:
        # Update Last Edited date in existing card
        pattern = (
            rf'(<strong>Start Date:</strong>\s*[\d/]+\s*&nbsp;·&nbsp;\s*'
            rf'<strong>Last Edited:</strong>\s*)[\w\s/]+'
            rf'(\s*&nbsp;·&nbsp;\s*<strong>Status:</strong>)'
        )
        # Simpler targeted replacement: find the card for this project
        # Look for the link to this project and update Last Edited in its card
        card_pattern = (
            rf'(href="{re.escape(link)}/?[^>]*>.*?'
            rf'<strong>Last Edited:</strong>\s*)[\w\s/]+'
            rf'(\s*&nbsp;·&nbsp;)'
        )
        new_content = re.sub(
            card_pattern,
            rf'\g<1>{today}\g<2>',
            content,
            flags=re.DOTALL
        )
        if new_content == content:
            # Fallback: simpler pattern
            simple_pattern = (
                rf'(href="{re.escape(link)}/?.*?Last Edited:</strong>\s*)([^<&]+)'
            )
            new_content = re.sub(
                simple_pattern,
                rf'\g<1>{today} ',
                content,
                flags=re.DOTALL
            )
        content = new_content

    with open(HOME_FILE, "w") as f:
        f.write(content)


def update_projects_json(title, folder_name, blurb, is_new=True, status="ongoing"):
    projects = load_projects()
    today = get_today()

    if is_new:
        projects.insert(0, {
            "name": title,
            "folder": folder_name,
            "startDate": today,
            "lastEdited": today,
            "status": status,
            "blurb": blurb
        })
    else:
        for p in projects:
            if p["folder"] == folder_name:
                p["lastEdited"] = today
                break

    save_projects(projects)


def update_project_status(folder_name, new_status):
    projects = load_projects()
    for p in projects:
        if p["folder"] == folder_name:
            p["status"] = new_status.lower()
            if new_status.lower() == "finished":
                p["lastEdited"] = get_today()
            break
    save_projects(projects)
    print(f"[Success] Status updated to '{new_status}' for {folder_name}")


def new_project():
    title = input("Project Title: ")
    blurb = input("Short Blurb: ")
    print("Status options: ongoing / finished / abandoned")
    status = input("Status [ongoing]: ").strip() or "ongoing"
    folder_name = slugify(title)

    # 1. Create directory structure
    os.makedirs(folder_name, exist_ok=True)
    os.makedirs(os.path.join(folder_name, "images"), exist_ok=True)

    # 2. Create index.md in project folder
    proj_index = os.path.join(folder_name, "index.md")
    with open(proj_index, "w") as f:
        f.write(f"# {title}\n---\n\n")
        f.write(f"## {get_today()}\n")
        f.write("Project started today!\n")

    # 3. Update homepage and projects.json
    update_home_page(title, folder_name, blurb, is_new=True, status=status)
    update_projects_json(title, folder_name, blurb, is_new=True, status=status)
    print(f"\n[Success] Project created: {os.path.abspath(proj_index)}")
    print(f"[Reminder] Add ./images/listImage.png to {folder_name}/images/ for the article thumbnail.")


def amend_project():
    dirs = [
        d
        for d in os.listdir(".")
        if os.path.isdir(d) and not d.startswith((".", "_", "assets", "CV"))
    ]
    print("\nWhich project are you working on?")
    for i, d in enumerate(dirs):
        print(f"{i}: {d}")

    choice = int(input("Select index: "))
    folder_name = dirs[choice]
    proj_index = os.path.join(folder_name, "index.md")

    with open(proj_index, "r") as f:
        first_line = f.readline()
        title = first_line.replace("#", "").strip()

    # 1. Append new date header
    with open(proj_index, "a") as f:
        f.write(f"\n## {get_today()}\n\n")

    # 2. Update homepage and projects.json
    update_home_page(title, folder_name, "", is_new=False)
    update_projects_json(title, folder_name, "", is_new=False)
    print(f"\n[Success] Header added: {os.path.abspath(proj_index)}")


def set_status():
    projects = load_projects()
    print("\nWhich project do you want to update status for?")
    for i, p in enumerate(projects):
        print(f"{i}: {p['name']} (currently: {p.get('status', 'ongoing')})")

    choice = int(input("Select index: "))
    folder_name = projects[choice]["folder"]

    print("Status options: ongoing / finished / abandoned")
    new_status = input("New status: ").strip().lower()

    if new_status not in ("ongoing", "finished", "abandoned"):
        print("Invalid status. Choose from: ongoing, finished, abandoned")
        return

    update_project_status(folder_name, new_status)

    # Also update the status span in index.md
    with open(HOME_FILE, "r") as f:
        content = f.read()

    link = f"./{folder_name}"
    css_map = {"ongoing": "status-ongoing", "finished": "status-finished", "abandoned": "status-abandoned"}
    label_map = {"ongoing": "Ongoing", "finished": "Finished", "abandoned": "Abandoned"}
    new_css = css_map[new_status]
    new_label = label_map[new_status]

    # Replace status span for this project's card
    pattern = (
        rf'(href="{re.escape(link)}/?.*?<span class="status-\w+">)\w+(<\/span>)'
    )
    new_content = re.sub(
        pattern,
        rf'<span class="{new_css}">{new_label}\2',
        content,
        flags=re.DOTALL
    )
    with open(HOME_FILE, "w") as f:
        f.write(new_content)

    print(f"[Success] Updated status in index.md to '{new_label}'")


if __name__ == "__main__":
    print("Choose an action:")
    print("  [1] New Project")
    print("  [2] Amend Project (update Last Edited)")
    print("  [3] Set Project Status")
    mode = input("Choice: ")
    if mode == "1":
        new_project()
    elif mode == "2":
        amend_project()
    elif mode == "3":
        set_status()
    else:
        print("Invalid choice.")
