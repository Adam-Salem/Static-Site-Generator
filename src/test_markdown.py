import unittest
from markdown_methods import *


class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
            ["This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"])
        
    
    def test_heading_block(self):
        block = "# This is a heading"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.heading, type)
        
    def test_heading_block_2(self):
        block = "### This is a heading"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.heading, type)
        
    def test_heading_block_3(self):
        block = "###### This is a heading"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.heading, type)
        
    def test_heading_block_4(self):
        block = "####### This is a heading"
        type = block_to_block_type(block)
        self.assertNotEqual(BlockType.heading, type)

    def test_heading_block_5(self):
        block = "This is a heading"
        type = block_to_block_type(block)
        self.assertNotEqual(BlockType.heading, type)
        
    def test_code_block(self):
        block = "```This is a heading```"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.code, type)
        
    def test_quote_block(self):
        block = ">This is a quote\n>watch this work properly on the first try\n>that would be sick"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.quote, type)
        
    def test_quote_block_broken(self):
        block = ">This is a quote\n-watch this work properly on the first try\n>that would be sick"
        type = block_to_block_type(block)
        self.assertNotEqual(BlockType.quote, type)  

    def test_quote_block_broken2(self):
        block = ">This is a quote\n >watch this work properly on the first try\n>that would be sick"
        type = block_to_block_type(block)
        self.assertNotEqual(BlockType.quote, type)  
        
    def test_unordered_list_block(self):
        block = "- This is an unordered list\n- watch this work properly on the first try\n- that would be sick"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.unordered_list, type)
        
    def test_unordered_list_block_broken(self):
        block = "-This is an unordered list\n-watch this work properly on the first try\n-that would be sick"
        type = block_to_block_type(block)
        self.assertNotEqual(BlockType.unordered_list, type)
        
    def test_unordered_list_block_broken2(self):
        block = "- This is an unordered list\n> watch this work properly on the first try\n> that would be sick"
        type = block_to_block_type(block)
        self.assertNotEqual(BlockType.unordered_list, type) 
        
    def test_ordered_list_block(self):
        block = "1. This is an ordered list\n2. watch this work properly on the first try\n3. that would be sick"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.ordered_list, type)
        
    def test_ordered_list_block2(self):
        block = "1. This is an ordered list\n2. watch this work properly on the first try\n3. that would be sick\n4. In fact \n5. I think it would be\n6. The greatest of all time\n7. of the python\n8. Coding language's\n9. History"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.ordered_list, type)
        
    def test_ordered_list_block_broken(self):
        block = "1. This is an ordered list\n2.watch this work properly on the first try\n3. that would be sick"
        type = block_to_block_type(block)
        self.assertNotEqual(BlockType.ordered_list, type)
        
    def test_ordered_list_block_broken2(self):
        block = "3. This is an ordered list\n2. watch this work properly on the first try\n1. that would be sick"
        type = block_to_block_type(block)
        self.assertNotEqual(BlockType.ordered_list, type)

    def test_ordered_list_block_broken3(self):
        block = "2. This is an ordered list\n3. watch this work properly on the first try\n4. that would be sick"
        type = block_to_block_type(block)
        self.assertNotEqual(BlockType.ordered_list, type)
if __name__ == "__main__":
    unittest.main()