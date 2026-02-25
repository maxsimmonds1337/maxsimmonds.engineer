import os
import re
from datetime import datetime

# --- Configuration ---
HOME_FILE = "index.md"
DATE_FORMAT = "%d/%m/%y"  # dd/mm/yyyy as requested


def slugify(text):
    return text.lower().replace(" ", "_").replace("-", "_").strip("_")


def get_today():
    return datetime.now().strftime(DATE_FORMAT)


def update_home_page(title, folder_name, blurb, is_new=True):
    with open(HOME_FILE, "r") as f:
        lines = f.readlines()

    today = get_today()
    link = f"./{folder_name}"

    if is_new:
        # We start with the content, then END with a separator
        new_entry = [
            f"\n# [{title}]({link})\n\n",
            f"**Start Date:** {today}\n\n",
            f"**Last Edited:** {today}\n\n",
            f"{blurb}\n",
            "\n---\n",
        ]

        inserted = False
        for i, line in enumerate(lines):
            if "---" in line:
                lines[i + 1 : i + 1] = new_entry
                inserted = True
                break
        if not inserted:
            lines.extend(new_entry)
    else:
        # Update existing entry "Last Edited" date
        content = "".join(lines)

        # Split over two lines using parentheses (Implicit Concatenation)
        pattern = (
            rf"(# \[{re.escape(title)}\]\({re.escape(link)}/?\).*?"
            r"\*\*Last Edited:\*\*\s*)[\d/]+"
        )

        content = re.sub(pattern, rf"\g<1>{today}", content, flags=re.DOTALL)
        lines = [content]

    with open(HOME_FILE, "w") as f:
        f.writelines(lines)


def new_project():
    title = input("Project Title: ")
    blurb = input("Short Blurb: ")
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

    # 3. Update homepage
    update_home_page(title, folder_name, blurb, is_new=True)
    print(f"\n[Success] Project created: {os.path.abspath(proj_index)}")


def amend_project():
    # List directories to pick from
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

    # Get Title from the project's index.md (first line)
    with open(proj_index, "r") as f:
        first_line = f.readline()
        title = first_line.replace("#", "").strip()

    # 1. Append new date header
    with open(proj_index, "a") as f:
        f.write(f"\n## {get_today()}\n\n")

    # 2. Update homepage Last Edited
    update_home_page(title, folder_name, "", is_new=False)
    print(f"\n[Success] Header added: {os.path.abspath(proj_index)}")


if __name__ == "__main__":
    mode = input("Choose: [1] New Project, [2] Amend Project: ")
    if mode == "1":
        new_project()
    elif mode == "2":
        amend_project()
