import os
from yozuch.loaders import Loader


class PageLoader(Loader):
    name = 'pages'

    def load(self, context, pages_path):
        for filename in os.listdir(pages_path):
            path = os.path.join(pages_path, filename)
            if not os.path.isfile(path):
                continue
            filename = os.path.basename(path)
            name, ext = os.path.splitext(filename)
            if ext in context.config['PAGE_FILE_EXTENSIONS']:
                yield filename
