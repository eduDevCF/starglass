import unittest
from parse_markdown import (
    extract_markdown_images, extract_markdown_links, BlockType,
    markdown_to_blocks, extract_code_blocks, block_to_block_type
)

class TestParseMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link text](https://imgur.com)"
        )
        self.assertListEqual([("link text", "https://imgur.com")], matches)
    
    def test_extract_code_blocks(self):
        md = """## Heading2 about `if... else` blocks

This is how to use conditional logic in Python.

```

username = "Boots"

if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")

```

    You can also add an `elif` statement in there."""

        md_code = """```

username = "Boots"

if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")

"""
        blocks = extract_code_blocks(md)

        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "## Heading2 about `if... else` blocks\n\nThis is how to use conditional logic in Python.\n\n")
        self.assertEqual(blocks[1], md_code)
        self.assertEqual(blocks[2], "\n\n    You can also add an `elif` statement in there.")

    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_with_code(self):
        md = """## Heading2 about `if... else` blocks

This is how to use conditional logic in Python.

```

username = "Boots"

if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")

```

    You can also add an `elif` statement in there."""

        md_code = """```

username = "Boots"

if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")

"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[0], "## Heading2 about `if... else` blocks")
        self.assertEqual(blocks[1], "This is how to use conditional logic in Python.")
        self.assertEqual(blocks[2], md_code)
        self.assertEqual(blocks[3], "You can also add an `elif` statement in there.")

    def test_block_to_block_type(self):
        h1 = "# Heading 1"
        h2 = "## Heading 2"
        h3 = "### Heading 3"
        h4 = "#### Heading 4"
        h5 = "##### Heading 5"
        h6 = "###### Heading 6"
        code = "```\nprint('Hello World')\n"
        quote = ">A wise woman once said..."
        ul = "- Item 1\n- Item 2\n- Item 3"
        ol = "1. First\n2. Second\n3. Third"
        p = "This is a vanilla paragraph."
        self.assertEqual(block_to_block_type(h1), BlockType.H1)
        self.assertEqual(block_to_block_type(h2), BlockType.H2)
        self.assertEqual(block_to_block_type(h3), BlockType.H3)
        self.assertEqual(block_to_block_type(h4), BlockType.H4)
        self.assertEqual(block_to_block_type(h5), BlockType.H5)
        self.assertEqual(block_to_block_type(h6), BlockType.H6)
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(ul), BlockType.UL)
        self.assertEqual(block_to_block_type(ol), BlockType.OL)
        self.assertEqual(block_to_block_type(p), BlockType.P)


if __name__ == "__main__":
    unittest.main()