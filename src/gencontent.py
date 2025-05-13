def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Generate HTML pages recursively from all markdown files in a directory."""
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)
    
    # Iterate through all entries in the content directory
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        
        # If it's a directory
        if os.path.isdir(entry_path):
            # Check if it contains an index.md file
            index_path = os.path.join(entry_path, "index.md")
            if os.path.isfile(index_path):
                # For directories with index.md, create a directory-name.html file
                rel_dir = os.path.relpath(entry_path, dir_path_content)
                output_path = os.path.join(dest_dir_path, rel_dir + ".html")
                generate_page(index_path, template_path, output_path)
            
            # Also recursively process subdirectories
            sub_dest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(entry_path, template_path, sub_dest_dir)
                
        # If it's a markdown file directly
        elif entry.endswith('.md'):
            # For regular .md files, just convert to .html
            output_filename = entry.replace('.md', '.html')
            output_path = os.path.join(dest_dir_path, output_filename)
            generate_page(entry_path, template_path, output_path)