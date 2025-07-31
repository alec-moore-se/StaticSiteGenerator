import os
import shutil
from delimiter_funcs import markdown_to_html_node, extract_title


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


def generate_page(from_path, template_path, dest_path):
    dest_path = dest_path.replace(".md", ".html")
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")
    markdown = None
    template = None
    with open(from_path) as f:
        markdown = f.read()
        f.close()
    with open(template_path) as g:
        template = g.read()
        g.close()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    # if not os.path.exists(dest_path):
    #   os.makedirs(dest_path)
    with open(dest_path, "w") as h:
        h.write(template)
        h.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
    else:
        dir_contents = os.listdir(dir_path_content)
        for paths in dir_contents:
            combo_paths = os.path.join(dir_path_content, paths)
            if os.path.isdir(combo_paths):
                os.mkdir(os.path.join(dest_dir_path, paths))
            generate_pages_recursive(
                combo_paths, template_path, os.path.join(dest_dir_path, paths))

# Comment at bottom of file
