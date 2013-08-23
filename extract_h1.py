#!/usr/bin/env python

from HTMLParser import HTMLParser
from pelican import signals, readers, contents
import os, markdown

class H1Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.currTag = None
        self.h1 = None

    def handle_starttag(self, tag, attrs):
        if "h1" == tag:
            self.currTag = tag

    def handle_endtag(self, tag):
        if "h1" == tag:
            self.currTag = None

    def handle_data(self, data):
        if not self.h1 and self.currTag:
            self.h1 = data


def extract_h1(content):
    if isinstance(content, contents.Static):
        return

    markdownFilePath = content.source_path
    extension = os.path.splitext(markdownFilePath)[1][1:]
    if not extension in readers.MarkdownReader.file_extensions:
        return

    htmlContent = markdown.markdown(content._content, extensions=['headerid(forceid=False)'])
    parser = H1Parser()
    parser.feed(htmlContent)
    content.html_h1 = parser.h1

def register():
    signals.content_object_init.connect(extract_h1)

if __name__ == "__main__":
    parser = H1Parser()
    htmlStr = open("./index.html").read()
    parser.feed(htmlStr)
    print parser.html_h1

