import os
import shutil

from website_making import *
dir_path_static = "./static"
dir_path_public = "./public"

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        home = os.path.join(dir_path_content, item)
        target = os.path.join(dest_dir_path, item)

        if os.path.isfile(home):
            generate_page(home, template_path, f"{dest_dir_path}/index.html")
        else:
            generate_pages_recursive(home, template_path, target)

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copyy(dir_path_static, dir_path_public)
    generate_pages_recursive("./content", "./template.html", "public")

main()