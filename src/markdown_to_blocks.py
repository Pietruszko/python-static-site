from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    lines = markdown.splitlines()
    
    blocks = []
    current_block = []
    
    for line in lines:
        if not line.strip():
            if current_block:
                block_text = "\n".join(current_block).strip()
                blocks.append(block_text)
                current_block = []
        else:
            current_block.append(line)
    
    if current_block:
        block_text = "\n".join(current_block).strip()
        blocks.append(block_text)
    
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")
    
    if block.startswith("#"):
        if block.startswith("###### ") and len(block) > 7:
            return BlockType.HEADING
        if block.startswith("##### ") and len(block) > 6:
            return BlockType.HEADING
        if block.startswith("#### ") and len(block) > 5:
            return BlockType.HEADING
        if block.startswith("### ") and len(block) > 4:
            return BlockType.HEADING
        if block.startswith("## ") and len(block) > 3:
            return BlockType.HEADING
        if block.startswith("# ") and len(block) > 2:
            return BlockType.HEADING
    
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if all(len(line) >= 3 and line[0].isdigit() and line[1] == "." and line[2] == " " for line in lines):
        for i, line in enumerate(lines):
            expected_num = i + 1
            if not line.startswith(f"{expected_num}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
