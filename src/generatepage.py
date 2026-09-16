from markdown_html import markdown_to_html_node
from markdown_converter import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        from_markdown = f.read()
    with open(template_path, "r") as t:
        template_file = t.read()

    html_string = markdown_to_html_node(from_markdown).to_html()
    title = extract_title(from_markdown)

    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html_string)

    dest_path_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_path_dir):
        os.makedirs(dest_path_dir)
    with open(dest_path, "w") as d:
        d.write(template_file)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(full_path):
            generate_page(full_path, template_path, os.path.join(dest_dir_path, entry.replace(".md",".html")))
        else:
            generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, entry))