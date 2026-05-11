import os
import shutil
from complete import *
def copyy(dir_copy, dir_remove_replace):
    if not os.path.exists(dir_remove_replace):
        os.mkdir(dir_remove_replace)
    for item in os.listdir(dir_copy):
        home = os.path.join(dir_copy, item)
        target = os.path.join(dir_remove_replace, item)
        print(f"(ง'̀-'́)ง - {home} to {target}")
        if os.path.isfile(home):
            shutil.copy(home, target)
        else:
            copyy(home, target)

def extract_title(markdown):
    new = markdown.lstrip()
    splitted = new.split("\n\n")
    if splitted[0].startswith("# ") and splitted[0][1] != "#":
        return (splitted[0].lstrip("# ")).rstrip()
    else:
        raise Exception("no h1 header")

def generate_page(from_path, temp_path, dest):
    print(f"making page from {from_path} to {dest} using {temp_path}")
    markdown = None
    with open(from_path, mode="r") as f:
        markdown = f.read()
    template = None
    with open(temp_path, mode="r") as f:
        template = f.read()
    html = (markdown_to_html(markdown)).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    dest_path = os.path.dirname(dest)
    os.makedirs(dest_path, exist_ok=True)
    with open(dest, mode="w") as f:
        f.write(html)


    