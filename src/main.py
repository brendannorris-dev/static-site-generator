from textnode import TextNode, TextType
from copystatic import copy_files_recursive
import os, shutil

from markdown_html import markdown_to_html_node

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_files_recursive("static", "public")

main()