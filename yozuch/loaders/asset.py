import os
from yozuch.loaders import Loader


class AssetLoader(Loader):
    name = 'assets'

    def load(self, context, path):
        for root, _, files in os.walk(path):
            for filename in files:
                source_path = os.path.join(root, filename)
                yield source_path, os.path.relpath(source_path, path)
