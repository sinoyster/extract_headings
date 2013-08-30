#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from HTMLParser import HTMLParser
from pelican import signals, readers, contents
import os, sys, re, md5, markdown

def my_default_slugify(value, sep):
    m = md5.new()
    m.update(value)
    return "toc_{}".format(m.digest().encode("hex"))

class Heading:
    HeadRegex = re.compile("h[1-6]")
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value

    def __repr__(self):
        return "{}:{}".format(self.tag, self.value)

    @classmethod
    def is_heading(cls, tag):
        return None != cls.HeadRegex.match(tag)

class HeadingParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.headings = []
        self.tagOpen = False
        self.toc = ""

    def handle_starttag(self, tag, attrs):
        if Heading.is_heading(tag):
            self.headings.append(Heading(tag, ""))
            self.tagOpen = True

    def handle_endtag(self, tag):
        self.tagOpen = False

    def handle_data(self, data):
        if self.tagOpen and len(self.headings) > 0:
            self.headings[-1].value = data

    def generate_toc(self, slugify_func):
        self.toc = "<ul>"
        prevHead = None
        openListSetNum = 0
        linkFormat = "<a href='#{}'>{}</a>"
        for i in xrange(len(self.headings)):
            head = self.headings[i]
            head.parent = None
            headAnchor = "{}".format(slugify_func(head.value, "-"))
            # first elem
            if 0 == i:
                self.toc += ("<li>" + linkFormat).format(headAnchor, head.value)
                continue
            prevHead = self.headings[i-1]
            if head.tag > prevHead.tag:
                head.parent = prevHead
                openListSetNum += 1
                self.toc += ("<ul><li>" + linkFormat).format(headAnchor, head.value)
            elif head.tag < prevHead.tag:
                currParent = prevHead.parent
                while currParent and (head.tag <= currParent.tag):
                    openListSetNum -= 1
                    self.toc += ("</li></ul>")
                    currParent = currParent.parent
                head.parent = currParent
                self.toc += ("</li><li>" + linkFormat).format(headAnchor, head.value)
            else:
                head.parent = prevHead.parent
                self.toc += ("</li><li>" + linkFormat).format(headAnchor, head.value)
        while openListSetNum > 0:
            self.toc += ("</li></ul>")
            openListSetNum -= 1
        if len(self.headings) > 1:
            self.toc += "</li></ul>"
        else:
            self.toc += "</ul>"
        return self.toc


def extract_headings(content):
    if isinstance(content, contents.Static):
        return

    markdownFilePath = content.source_path
    extension = os.path.splitext(markdownFilePath)[1][1:]
    if not extension in readers.MarkdownReader.file_extensions:
        return

    htmlContent = markdown.markdown(content._content)
    parser = HeadingParser()
    parser.feed(htmlContent)
    content.html_headings = parser.headings
    # set article title to h1 if any
    content.html_h1 = ""
    for head in parser.headings:
        if "h1" == head.tag:
            # use the first h1 heading
            content.html_h1 = head.value
            break
    if not content.html_h1:
        content.html_h1 = content.title

    try:
        my_slugify = content.settings['MY_SLUGIFY_FUNC']
    except:
        my_slugify = None
    if not my_slugify:
        my_slugify = my_default_slugify
        #my_slugify = markdown.extensions.headerid.slugify
        #head.value = head.value.decode("UTF-8")
    content.html_toc = parser.generate_toc(my_slugify)


def register():
    signals.content_object_init.connect(extract_headings)

if __name__ == "__main__":
    parser = HeadingParser()
    htmlStr = "<html><head></head><body><h1>hello</h1>\
            <h2>hi, h2</h2><h2>hi, another h2</h2></body></html>"
    parser.feed(htmlStr)
    print parser.headings
    print parser.generate_toc(my_default_slugify)

