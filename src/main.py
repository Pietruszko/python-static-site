import os
import shutil
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
    
    print("\nCopying static directory to public...")
    copy_directory_contents("static", "public")
    print("Copy completed!")
    
    print("\nGenerating pages recursively...")
    generate_pages_recursive("content", "template.html", "public")
    print("Page generation completed!")

if __name__ == "__main__":
    main()
