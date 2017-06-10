import os
from yozuch.generators.template import TemplateEntry, TemplateGenerator


class PageGenerator(TemplateGenerator):

    def __init__(self, url_template, name):
        super().__init__(url_template, name, None)

    def generate(self, context):
        for filename in context.site.get('pages', []):
            name, ext = os.path.splitext(filename)
            url = self.url_template.format(name=name, filename=filename)
            entry = TemplateEntry(url, '!pages/' + filename, 'pages/{}'.format(filename))
            yield entry
