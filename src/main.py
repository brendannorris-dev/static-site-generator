from textnode import TextNode, TextType
from copystatic import copy_files_recursive
import os, shutil, sys

from generatepage import generate_page, generate_pages_recursive
from markdown_html import markdown_to_html_node

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_files_recursive("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)

main()