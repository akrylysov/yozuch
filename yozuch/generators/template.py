import codecs
import os
from yozuch.generators import Generator
from yozuch.entries import Entry
from yozuch.utils import makedirs, path_from_url


class TemplateEntry(Entry):

    def __init__(self, url, template, page_id, template_vars=None):
        super().__init__(url)
        self.url = url
        self.template = template
        self.page_id = page_id
        self.template_vars = template_vars

    def _write_file(self, content, path):
        with codecs.open(path, 'w', 'utf-8') as f:
            f.write(content)

    def write(self, context, env, output_dir):
        if self.template is None:
            raise LookupError('Template is not set for {}'.format(self.page_id))
        path = os.path.join(output_dir, path_from_url(self.url))
        template = env.get_template(self.template)
        template_vars = {}
        if self.template_vars:
            template_vars.update(self.template_vars)
        template_vars.update({
            'site': context.site,
            'theme': context.theme,
            'config': context.config,
            'page_id': self.page_id,
            'page_url': self.url,
        })
        content = template.render(**template_vars)
        makedirs(os.path.dirname(path))
        self._write_file(content, path)


class TemplateGenerator(Generator):

    def _register_reference(self, context, entry):
        context.references[entry.page_id] = entry.url

    def __init__(self, url_template, name, template):
        super().__init__(url_template, name)
        self.template = template

    def generate(self, context):
        yield TemplateEntry(self.url_template, self.template, self.name)
