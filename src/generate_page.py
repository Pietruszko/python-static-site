import os
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()
    
    title = extract_title(markdown)
    
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    
    if basepath != "/":
        html = html.replace('href="/', f'href="{basepath}')
        html = html.replace('src="/', f'src="{basepath}')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(html)
