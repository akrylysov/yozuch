from yozuch.generators.document import DocumentEntry
from yozuch.generators.template import TemplateGenerator
from yozuch.utils import format_url_from_object


class PostGenerator(TemplateGenerator):

    def generate(self, context):
        for doc in context.site.get('posts', []):
            doc.url = format_url_from_object(self.url_template, doc)
            yield DocumentEntry(self.template, doc, template_vars={'post': doc})
