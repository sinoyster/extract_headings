# extract_headings plugin for pelican

Any problems, please contact wilbur.ma@foxmail.com

This is a very simple pelican plugin which extracts the h1~h6 headings from a markdown document.

This plugin introduces three new member to the pelican content object:
*  html_h1: the first h1 heading, if not set content.title is used
*  html_headings: a list of heading objects like {tag: "h1", value: "Hello this is h1 heading"}
*  html_toc: table of contents build with the markdown headings, html unordered list style

## License
Released under the BSD (3-Clause) License. Please see LICENSE.txt for more details.

## Requirements
*  python-markdown: pip install Markdown

## Thanks
*  extract_toc plugin
