import fnmatch
import os
from yozuch.loaders import Loader


def fnmatch_patterns(name, patterns):
    return any([fnmatch.fnmatch(name, pattern) for pattern in patterns])


class AssetLoader(Loader):
    name = 'assets'

    def load(self, context, path):
        ignore = context.config['ASSET_IGNORE']
        for root, _, files in os.walk(path):
            for filename in files:
                asset_full_path = os.path.join(root, filename)
                asset_rel_path = os.path.relpath(asset_full_path, path)
                if not fnmatch_patterns(os.path.basename(asset_full_path), ignore) and not fnmatch_patterns(asset_rel_path, ignore):
                    yield '/{}/{}'.format(self.name, asset_rel_path), asset_full_path, asset_rel_path
