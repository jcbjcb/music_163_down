
from html.parser import HTMLParser


class MusicHtmlParse(HTMLParser):

    a_text = False

    def __init__(self):
        HTMLParser.__init__(self)
        self.musics_id = [

        ]

        self.musics_name = [

        ]
    def handle_starttag(self, tag, attrs):
        # pass
        if tag == "a":
            for (variable, value) in attrs:
                if variable == "href":
                    # print(value)
                    if not value.startswith('/song?id=${song.id}') and not value.startswith('/song?id=${x.id}') and value.startswith('/song?id='):
                        self.a_text = True
                        # print(str(attrs[1][1]))
                        id = value.replace("/song?id=", '')
                        self.musics_id.append(id)
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
        if self.a_text and self.lasttag == "a":
            self.musics_name.append(data)

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

