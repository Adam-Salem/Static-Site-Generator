from enum import Enum
import re

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered list"
    ordered_list = "ordered list"

def markdown_to_blocks(markdown):
    md = markdown.split("\n\n")
    ret_md = []
    for block in md:
        lines = block.split("\n")
        fixed_lines = []
        for line in lines:
            if line:
                fixed_line = line.strip()
                if fixed_line:
                    fixed_lines.append(fixed_line)
        new_block = "\n".join(fixed_lines)
        if new_block:
            ret_md.append(new_block)
    return ret_md

def block_to_block_type(block):
    if re.findall(r"^\#{1,6} ", block) != []:
        return BlockType.heading
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.code
    
    quote = 0
    unordered_list = 0
    ordered_list = 0
    orderedlist = []
    ordered = True
    lines = block.split("\n")
    for i in range(len(lines)):
        if lines[i].startswith(">"):
            quote += 1
        if lines[i].startswith("- "):
            unordered_list += 1
        if re.match(r"^([1-9][0-9]*\.\s)", lines[i]):
            entry = int(re.match(r"^([1-9][0-9]*)", lines[i]).group(0))
            orderedlist.append(entry)
            if ordered and (len(orderedlist) == i + 1) and orderedlist[i] == (i + 1):
                ordered = True
            else:
                ordered = False
            ordered_list += 1
    
    linecount = len(block.split("\n"))
    if linecount > 0 and quote == linecount:
        return BlockType.quote
    elif linecount > 0 and unordered_list == linecount:
        return BlockType.unordered_list
    elif linecount > 0 and ordered_list == linecount and ordered:
        return BlockType.ordered_list
    else:
        return BlockType.paragraph