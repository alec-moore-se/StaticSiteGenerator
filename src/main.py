from textnode import TextNode, TextType

import os
import shutil


def main():
    static_to_public("./static")


def static_to_public(starting_dir, curr_directory=None):
    if (os.path.exists("./public")):
        shutil.rmtree("./public")
    os.mkdir(f"{starting_dir}/../public")
    static_to_public_rec(starting_dir)


def static_to_public_rec(path, copy_path=os.path.abspath("./public")):
    print(f"copy_path:{copy_path}")
    if os.path.isfile(path):
        print(f"copying: {path} to {copy_path}")
        shutil.copy(path, copy_path)
    else:
        dir_contents = os.listdir(path)
        for paths in dir_contents:
            combo_paths = os.path.join(path, paths)
            print(f"combo_paths:{combo_paths}")
            if os.path.isdir(combo_paths):
                os.mkdir(os.path.join(copy_path, paths))
            static_to_public_rec(combo_paths, os.path.join(copy_path, paths))


main()
