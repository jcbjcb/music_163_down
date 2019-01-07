
from html.parser import HTMLParser


class PageHtmlParse(HTMLParser):

    a_text = False

    def __init__(self):
        HTMLParser.__init__(self)
        self.pages = 0
        self.params = ''
    def handle_starttag(self, tag, attrs):
        # pass
        if tag == "a":
            for (variable, value) in attrs:
                if variable == "class":
                    # print(value)
                    if value == "zpgi":
                        for (variable1, value1) in attrs:
                            if variable1 == "href":
                                self.params = value1[value1.index("?")+1:]
                                break
                        self.a_text = True
                    else:
                        self.a_text = False

        # print('<%s>' % tag)

    def handle_endtag(self, tag):
        pass
        # print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        pass
        # print('<%s/>' % tag)

    def handle_data(self, data):
        if self.a_text and self.lasttag == "a" and data != "\n":
            if int(data) > 0 :
                self.pages = int(data)

        # print(data)

    def handle_comment(self, data):
        pass
        # print('<!--', data, '-->')

    def handle_entityref(self, name):
        pass
        # print('&%s;' % name)

    def handle_charref(self, name):
        pass
        # print('&#%s;' % name)

