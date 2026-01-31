import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    os.makedirs(dest_dir_path, exist_ok=True)
    
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        
        if os.path.isfile(content_path):
            if item.endswith(".md"):
                html_filename = item[:-3] + ".html"
                html_dest_path = os.path.join(dest_dir_path, html_filename)
                generate_page(content_path, template_path, html_dest_path, basepath)
        else:
            generate_pages_recursive(content_path, template_path, dest_path, basepath)
