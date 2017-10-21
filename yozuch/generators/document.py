from yozuch.generators.template import TemplateEntry, TemplateGenerator
from yozuch.utils import format_url_from_object
from yozuch.rstparser import RstParser


class DocumentEntry(TemplateEntry):

    def __init__(self, template, doc, **kwargs):
        super().__init__(doc.url, template, doc.id, **kwargs)
        self.doc = doc

    def publish(self, context):
        rst_options = context.config['RST_OPTIONS']
        parser = RstParser(rst_options)
        rooturl = context.config['URL'] if not context.config['DEBUG'] else None
        parser.publish(self.doc, context.references, rooturl, context.entries)


class DocumentGenerator(TemplateGenerator):

    def __init__(self, url_template, name, template, source=None):
        super().__init__(url_template, name, template)
        self.source = source

    def generate(self, context):
        docs = [doc for doc in context.site.get('documents', []) if self.source is None or doc.id == self.source]
        for doc in docs:
            doc.url = format_url_from_object(self.url_template, doc)
            yield DocumentEntry(self.template, doc, template_vars={'document': doc})
