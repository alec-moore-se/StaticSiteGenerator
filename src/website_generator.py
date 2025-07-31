import os
import shutil
from delimiter_funcs import markdown_to_html_node, extract_title


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)


def generate_page(from_path, template_path, dest_path, basepath):
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
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    # if not os.path.exists(dest_path):
    #   os.makedirs(dest_path)
    with open(dest_path, "w") as h:
        h.write(template)
        h.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path, basepath)
    else:
        dir_contents = os.listdir(dir_path_content)
        for paths in dir_contents:
            combo_paths = os.path.join(dir_path_content, paths)
            if os.path.isdir(combo_paths):
                os.mkdir(os.path.join(dest_dir_path, paths))
            generate_pages_recursive(
                combo_paths, template_path, os.path.join(dest_dir_path, paths), basepath)

# Comment at bottom of file
