from yozuch import logger
from yozuch.generators.template import TemplateEntry, TemplateGenerator
from yozuch.utils import format_url_from_object


class PostItemCollectionGenerator(TemplateGenerator):

    def __init__(self, collection_name, item_name, url_template, name, template):
        super().__init__(url_template, name, template)
        self._collection_name = collection_name
        self._item_name = item_name

    def generate(self, context):
        if 'posts' not in context.site:
            return
        items = context.site.get(self._collection_name, [])
        logger.info('Found {} {}'.format(len(items), self._collection_name))
        for item in items:
            page_id = '{}/{}'.format(self.name, item.slug)
            item.url = format_url_from_object(self.url_template, item)
            yield TemplateEntry(item.url, self.template, page_id, template_vars={self._item_name: item})
