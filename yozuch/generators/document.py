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

    def _generate_document(self, context, url_template, template, doc):
        doc.url = format_url_from_object(url_template, doc)
        entry = DocumentEntry(template, doc, template_vars={'document': doc})
        self._register_reference(context, entry)
        return entry

    def generate(self, context):
        docs = context.site.get('documents', [])
        if self.source is not None:
            docs = filter(lambda d: d.id == self.source, docs)
        for doc in docs:
            yield self._generate_document(context, self.url_template, self.template, doc)
