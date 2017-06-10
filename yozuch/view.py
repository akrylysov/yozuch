"""
Generator view helper.
"""

DEFAULT_NAMES = {
    'blog-index': 'yozuch.generators.blog_index.BlogIndexGenerator',
    'posts': 'yozuch.generators.post.PostGenerator',
    'tags-index': 'yozuch.generators.template.TemplateGenerator',
    'tags': 'yozuch.generators.tag.TagGenerator',
    'categories-index': 'yozuch.generators.template.TemplateGenerator',
    'categories': 'yozuch.generators.category.CategoryGenerator',
    'archive-index': 'yozuch.generators.template.TemplateGenerator',
    'atom-feed': 'yozuch.generators.template.TemplateGenerator',
    'pages': 'yozuch.generators.page.PageGenerator',
    'documents': 'yozuch.generators.document.DocumentGenerator',
    'assets': 'yozuch.generators.asset.AssetGenerator',
}


def view(url, generator, **kwargs):
    if generator in DEFAULT_NAMES:
        return url, generator, DEFAULT_NAMES[generator], kwargs
    return url, generator, kwargs
