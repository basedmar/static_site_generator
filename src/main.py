import os
import shutil

from website_making import *
dir_path_static = "./static"
dir_path_public = "./public"
def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copyy(dir_path_static, dir_path_public)
    generate_page("content/index.md", "./template.html", "public/index.html")

main()
