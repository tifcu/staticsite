from textnode import TextNode, TextType
import os
import shutil
from markdown_blocks import markdown_to_html_node
import sys
def copy_static(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)


    os.mkdir(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)

        else:
            copy_static(src_path, dest_path)
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line [2:].strip()
    raise Exception("No H1 header found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")


    with open(from_path, "r") as f:
        markdown = f.read()


    with open(template_path, "r") as f:
        template = f.read()


    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()


    title = extract_title(markdown)


    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir,exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
        elif os.path.isfile(from_path) and filename.endswith(".md"):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(from_path, template_path, dest_path, basepath)

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_static("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
