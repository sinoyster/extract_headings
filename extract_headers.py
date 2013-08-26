#!/usr/bin/env python

from HTMLParser import HTMLParser
from pelican import signals, readers, contents
import os, re, markdown

class Header:
    HeadRegex = re.compile("h[1-6]")
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value

    def __repr__(self):
        return "{}:{}".format(self.tag, self.value.encode("UTF-8"))

    @classmethod
    def is_header(cls, tag):
        return None != cls.HeadRegex.match(tag)

class HeaderParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.headers = []
        self.tagOpen = False

    def handle_starttag(self, tag, attrs):
        if Header.is_header(tag):
            self.headers.append(Header(tag, ""))
            self.tagOpen = True

    def handle_endtag(self, tag):
        self.tagOpen = False

    def handle_data(self, data):
        if self.tagOpen and len(self.headers) > 0:
            self.headers[-1].value = data

def extract_headers(content):
    if isinstance(content, contents.Static):
        return

    markdownFilePath = content.source_path
    extension = os.path.splitext(markdownFilePath)[1][1:]
    if not extension in readers.MarkdownReader.file_extensions:
        return

    htmlContent = markdown.markdown(content._content, extensions=['headerid(forceid=False)'])
    parser = HeaderParser()
    parser.feed(htmlContent)
    content.html_headers = parser.headers
    # set article title to h1 if any
    content.html_h1 = ""
    for head in parser.headers:
        if "h1" == head.tag:
            content.html_h1 = head.value
        if not content.html_h1:
            content.html_h1 = content.title

def register():
    signals.content_object_init.connect(extract_headers)

if __name__ == "__main__":
    parser = H1Parser()
    htmlStr = open("./index.html").read()
    parser.feed(htmlStr)
    print parser.h1

