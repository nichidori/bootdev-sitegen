from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
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
    
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", content)
    
    with open(dest_path, "w") as file:
        file.write(final_html)