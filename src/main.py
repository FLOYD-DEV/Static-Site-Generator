import os
import markdown
import shutil
from pathlib import Path
from title_extractor import extract_title
import re

def generate_page(markdown_file_path, template_file_path, output_file_path):
    """Generate a single HTML page from a markdown file and a template."""
    print(f"Generating page: {output_file_path} from {markdown_file_path}")
    try:
        with open(markdown_file_path, 'r') as f:
            markdown_content = f.read()
        html_content = markdown.markdown(markdown_content)
        html_content = (html_content.replace('<em>', '<i>')
                                   .replace('</em>', '</i>')
                                   .replace('<strong>', '<b>')
                                   .replace('</strong>', '</b>'))
        title = extract_title(markdown_content)
        with open(template_file_path, 'r') as f:
            template = f.read()
        html_page = template.replace('{{ Content }}', html_content).replace('{{ Title }}', title)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w') as f:
            f.write(html_page)
    except Exception as e:
        print(f"Error generating {output_file_path}: {e}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Processing content directory: {dir_path_content}")
    os.makedirs(dest_dir_path, exist_ok=True)
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(entry_path):
            dest_subdir = os.path.join(dest_dir_path, entry)
            print(f"Entering subdirectory: {entry_path}")
            generate_pages_recursive(entry_path, template_path, dest_subdir)
        elif os.path.isfile(entry_path) and entry_path.endswith('.md'):
            base_name = os.path.basename(entry_path).replace('.md', '.html')
            output_path = os.path.join(dest_dir_path, base_name)
            print(f"Found markdown file: {entry_path}")
            generate_page(entry_path, template_path, output_path)

def main():
    print("Starting static site generation...")
    dir_path_content = "./content"
    dir_path_static = "./static"
    dir_path_public = "./public"
    template_path = "./template.html"
    print(f"Content path: {dir_path_content}, Template: {template_path}, Output: {dir_path_public}")
    if os.path.exists(dir_path_public):
        print("Clearing public directory...")
        shutil.rmtree(dir_path_public)
    os.makedirs(dir_path_public, exist_ok=True)
    print("Copying static files...")
    from copystatic import copy_files_recursive
    copy_files_recursive(dir_path_static, dir_path_public)
    print("Generating HTML pages...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)
    print("Site generation complete.")

if __name__ == "__main__":
    main()