import unittest
from htmlnode import LeafNode
from parse_markdown import (
    extract_markdown_images, extract_markdown_links, BlockType,
    markdown_to_blocks, extract_code_blocks, block_to_block_type,
    markdown_to_html_node, text_to_children
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
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
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


    def test_text_to_children(self):
        text = "This is **important**!!!\n"
        children = [
            LeafNode(None, "This is "),
            LeafNode("b", "important"),
            LeafNode(None, "!!!")
        ]
        result = text_to_children(text)
        print("EXPECTED: ", children)
        print("RESULT: ", result)
        self.assertEqual(len(result), len(children))
        self.assertEqual(result[0].tag, children[0].tag)
        self.assertEqual(result[0].value, children[0].value)
        self.assertEqual(result[0].children, children[0].children)
        self.assertEqual(result[0].props, children[0].props)
        self.assertEqual(result[1].tag, children[1].tag)
        self.assertEqual(result[1].value, children[1].value)
        self.assertEqual(result[1].children, children[1].children)
        self.assertEqual(result[1].props, children[1].props)
        self.assertEqual(result[2].tag, children[2].tag)
        self.assertEqual(result[2].value, children[2].value)
        self.assertEqual(result[2].children, children[2].children)
        self.assertEqual(result[2].props, children[2].props)
        
        



    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
    
    def test_ordered_lists(self):
        md = """
1. First point
2. Second thought
3. Third reason
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First point</li><li>Second thought</li><li>Third reason</li></ol></div>"
        )
    
    def test_unordered_lists(self):
        md = """
- First point
- Second thought
- Third reason
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First point</li><li>Second thought</li><li>Third reason</li></ul></div>"
        )

    def test_blockquote(self):
        md = """
> This is a really inspiring quote.

>This is also a quote.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a really inspiring quote.</blockquote><blockquote>This is also a quote.</blockquote></div>"
        )

    def test_all_blocks_and_inlines(self):
        md = """
# Main Heading

This is an introductory paragraph with some **bold** text.

## Heading Two

This paragraph introduces an ordered list.

1. First
2. Second is **important**!!!
3. Third

Closing paragraph for heading two.

## Next Heading Two

This paragraph introduces an unordered list.

- First
- Second
- Third

### Heading Three

Let's make a point with a picture: ![python logo](https://i.imgur.com/zjjcJKZ.png)

#### Heading Four

This paragraph includes a [link](https://imgur.com).

##### Heading Five

We are _really_ getting into the weeds now.

###### Heading Six

Let's get `technical` with an example:

```
# Markdown that should not be processed

- ul one
- ul two
- ul three


```

# Conclusion

We can sum this up with a quote.

> The End.



"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><h1>Main Heading</h1><p>This is an introductory paragraph with some <b>bold</b> text.</p><h2>Heading Two</h2><p>This paragraph introduces an ordered list.</p><ol><li>First</li><li>Second is <b>important</b>!!!</li><li>Third</li></ol><p>Closing paragraph for heading two.</p><h2>Next Heading Two</h2><p>This paragraph introduces an unordered list.</p><ul><li>First</li><li>Second</li><li>Third</li></ul><h3>Heading Three</h3><p>Let's make a point with a picture: <img src="https://i.imgur.com/zjjcJKZ.png" alt="python logo"></p><h4>Heading Four</h4><p>This paragraph includes a <a href="https://imgur.com">link</a>.</p><h5>Heading Five</h5><p>We are <i>really</i> getting into the weeds now.</p><h6>Heading Six</h6><p>Let's get <code>technical</code> with an example:</p><pre><code># Markdown that should not be processed\n\n- ul one\n- ul two\n- ul three</code></pre><h1>Conclusion</h1><p>We can sum this up with a quote.</p><blockquote>The End.</blockquote></div>"""
        )


if __name__ == "__main__":
    unittest.main()