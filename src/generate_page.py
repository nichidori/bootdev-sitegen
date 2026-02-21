import os

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def generate_page(basepath, from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using template {template_path}"
    )

    markdown_content = ""
    template_content = ""

    with open(from_path, "r") as file:
        markdown_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()

    content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    final_html = (
        template_content.replace("{{ Title }}", title)
        .replace("{{ Content }}", content)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    with open(dest_path, "w") as file:
        file.write(final_html)


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry.replace(".md", ".html"))
        if os.path.isfile(from_path) and entry.endswith(".md"):
            generate_page(basepath, from_path, template_path, dest_path)
        elif os.path.isdir(from_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(basepath, from_path, template_path, dest_path)
