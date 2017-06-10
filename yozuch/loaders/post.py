from yozuch.entries import linkitems, CollectionItem
from yozuch.loaders import RstDocumentLoader
from yozuch.loaders.rstloader import RstLoader


class PostLoader(RstDocumentLoader):
    name = 'posts'

    def _create_post_meta_collection(self, post, site_collection, meta_items):
        if not isinstance(meta_items, list):
            meta_items = [meta_items]
        for name in meta_items:
            if name not in site_collection:
                site_collection[name] = CollectionItem(None, name)
            site_collection[name].posts.append(post)
            yield site_collection[name]

    def _create_meta_collection(self, posts, meta_name):
        site_collection = {}
        for post in posts:
            meta_items = post.metadata.get(meta_name, [])
            items = list(self._create_post_meta_collection(post, site_collection, meta_items))
            setattr(post, meta_name, items)
        result = sorted(site_collection.values(), key=lambda t: t.name)
        return sorted(result, key=lambda t: len(t.posts), reverse=True)

    def _create_meta_sources(self, context, posts):
        context.site['tags'] = self._create_meta_collection(posts, 'tags')

    def load(self, context, path):
        loader = RstLoader(context.config['RST_OPTIONS'])
        posts = loader.load_documents(path)

        posts = sorted(posts, key=lambda p: p.date)
        linkitems(posts)
        posts = list(reversed(posts))
        for post in posts:
            self._set_document_id(self.name, post)

        self._create_meta_sources(context, posts)

        return posts
