import unittest
from delimiter_funcs import markdown_to_blocks, block_to_block_type, extract_title
from textnode import BlockType

markdown_doc = """
## SHMUX

Shmux is a tmux session management tool written purely in shell script. It's designed to be a simple and lightweight project layout management tool. You can specify a layout for any project, including root directory, windows, panes, and programs to run in each pane.

It's also a little bit of a sassy bitch, so be prepared for that.

### Installation

#### You'll want to clone this repository to a base dir.

```bash
git clone https://github.com/typecraft-dev/shmux.git $HOME/.config/
```

#### Then, source the management.sh file

_zsh_

```
# Add this to your .zshrc
source ~/.config/shmux.sh
```

_bash_

```
# add this to your .bashrc
source ~/.config/shmux.sh
```

_fish_

```
# fuck you
```

### Usage

#### Create a new project layout

You can create a new project and open the example template file

```bash
shmux new "project_name"
```

Then, you can edit the template file to suit your needs.

#### Edit your project layout

Any time you want to edit the layout to a project. Just do it. moron

```bash
shmux edit "project_name"
```

#### Load your project

When you open a new shell, you can just load this shit. No biggie, nerd.

```bash
shmux load "project_name"
```

this will load tmux and attach to the layout you defined in "project_name"
"""

markdown_blocks = None


class test_delimiter_funcs(unittest.TestCase):
    def test_markdown_blocks(self):
        markdown_blocks = markdown_to_blocks(markdown_doc)
        self.assertTrue(len(markdown_blocks) == 25)

    def test_block_to_block_type(self):
        markdown_blocks = markdown_to_blocks(markdown_doc)
        markdown_line_1 = markdown_blocks[0]
        self.assertTrue(block_to_block_type(
            markdown_line_1) == BlockType.HEADING)

    def test_block_to_block_type2(self):
        markdown_blocks = markdown_to_blocks(markdown_doc)
        markdown_line = markdown_blocks[1]
        self.assertTrue(block_to_block_type(
            markdown_line) == BlockType.PARAGRAPH)

    def test_block_to_block_type3(self):
        markdown_blocks = markdown_to_blocks(markdown_doc)
        markdown_line = markdown_blocks[3]
        self.assertTrue(block_to_block_type(
            markdown_line) == BlockType.HEADING)

    def test_block_to_block_type4(self):
        markdown_blocks = markdown_to_blocks(markdown_doc)
        markdown_line = markdown_blocks[5]
        self.assertTrue(block_to_block_type(
            markdown_line) == BlockType.CODE)

    def test_extract_title(self):
        markdown = "   # Hello"
        title = extract_title(markdown)
        self.assertEqual("Hello", title)

    def test_extract_title_error(self):
        markdown = "     Hello"
        title = ""
        try:
            title = extract_title(markdown)
        except Exception:
            pass
        self.assertEqual("", title)

    def test_extract_title_multiline(self):
        markdown = """ what the helly\n # Jelly Belly \n ### cummies"""
        title = extract_title(markdown)
        self.assertEqual("Jelly Belly ", title)
