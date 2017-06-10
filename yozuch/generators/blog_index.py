from yozuch.generators.template import TemplateEntry, TemplateGenerator
from yozuch.paginator import Paginator


class BlogIndexGenerator(TemplateGenerator):

    def __init__(self, url_template, name, template, posts_per_page=0, pagination_url=None):
        super().__init__(url_template, name, template)
        self.posts_per_page = posts_per_page
        self.pagination_url = pagination_url

    def generate(self, context):
        if self.pagination_url is not None and self.posts_per_page > 0:
            paginator = Paginator(context.site['posts'], self.posts_per_page)
            for page in paginator.pages:
                template_vars = {
                    'paginator': paginator,
                    'paginator_page': page,
                }
                page_id = self.name
                page.url = self.url_template
                if page.number > 1:
                    page.url = self.pagination_url.format(number=page.number)
                    page_id = '{}/{}'.format(self.name, page.number)
                yield TemplateEntry(page.url, self.template, page_id, template_vars=template_vars)
        else:
            yield TemplateEntry(self.url_template, self.template, self.name)
