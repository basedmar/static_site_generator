import os
import shutil
def delete_and_copy(dir_copy, dir_remove_replace):
    if not os.path.exists(dir_remove_replace):
        os.mkdir(dir_remove_replace)
    for item in os.listdir(dir_copy):
        home = os.path.join(dir_copy, item)
        target = os.path.join(dir_remove_replace, item)
        print(f"(ง'̀-'́)ง - {home} to {target}")
        if os.path.isfile(home):
            shutil.copy(home, target)
        else:
            delete_and_copy(home, target)

def extract_title(markdown):
    pass