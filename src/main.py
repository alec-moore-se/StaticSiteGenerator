from website_generator import copy_files_recursive, generate_pages_recursive
import shutil
import os
import sys

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main(basepath="/"):
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        if basepath[len(basepath)-1] != '/':
            basepath += '/'
    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)
    copy_files_recursive(dir_path_static, dir_path_docs)
    generate_pages_recursive(
        dir_path_content, template_path, dir_path_docs, basepath)


main()
