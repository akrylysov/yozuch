from yozuch.generators.post_item_collection import PostItemCollectionGenerator


class TagGenerator(PostItemCollectionGenerator):

    def __init__(self, url_template, name, template=None):
        super().__init__('tags', 'tag', url_template, name, template)
