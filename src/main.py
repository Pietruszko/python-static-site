import os
import shutil
import sys
from textnode import TextNode, TextType
from generate_pages_recursive import generate_pages_recursive

def copy_directory_contents(src, dst):
    if os.path.exists(dst):
        print(f"Removing existing directory: {dst}")
        shutil.rmtree(dst)
    
    os.makedirs(dst, exist_ok=True)
    
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy2(src_path, dst_path)
        else:
            print(f"Copying directory: {src_path} -> {dst_path}")
            copy_directory_contents(src_path, dst_path)

def main():
    text_node = TextNode("abc", TextType.BOLD, "www.abc.com")
    print(text_node)
    
    # Get basepath from CLI argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print(f"\nUsing basepath: {basepath}")
    
    # For GitHub Pages, build into docs directory
    dest_dir = "docs"
    
    print(f"\nCopying static directory to {dest_dir}...")
    copy_directory_contents("static", dest_dir)
    print("Copy completed!")
    
    print(f"\nGenerating pages recursively to {dest_dir}...")
    generate_pages_recursive("content", "template.html", dest_dir, basepath)
    print("Page generation completed!")

if __name__ == "__main__":
    main()
