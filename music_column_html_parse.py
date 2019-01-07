
from html.parser import HTMLParser


class MusicColumnHtmlParse(HTMLParser):

    a_text = False

    def __init__(self):
        HTMLParser.__init__(self)
        self.musics_path_url = [

        ]

        self.musics_path_name = [

        ]
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (variable, value) in attrs:
                if variable == "class":
                    if value == 's-fc0' or value == "tit f-thide s-fc0":
                        for (variable1, value1) in attrs:
                            if variable1 == "href":
                                # print(value)
                                if value1 != 'javascript:void(0)' and value != 'javascript:;':
                                    self.a_text = True
                                    self.musics_path_url.append(value1)
                    else:
                        self.a_text = False


    def handle_endtag(self, tag):
        pass
        # print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        pass
        # print('<%s/>' % tag)

    def handle_data(self, data):
        if self.a_text and self.lasttag == "a" and data != '\n':
            self.musics_path_name.append(data)

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



