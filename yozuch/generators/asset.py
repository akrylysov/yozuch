import hashlib
import os
import shutil
from yozuch.utils import makedirs, path_from_url
from yozuch.generators import Generator
from yozuch.entries import Entry


def md5hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


class AssetEntry(Entry):

    def __init__(self, url, asset_id, asset_full_path):
        super().__init__(url, asset_id)
        self.asset_full_path = asset_full_path

    def write(self, context, env, output_dir):
        path = os.path.join(output_dir, path_from_url(self.url))
        makedirs(os.path.dirname(path))
        shutil.copyfile(self.asset_full_path, path)


class AssetGenerator(Generator):

    def generate(self, context):
        for asset_id, asset_full_path, asset_rel_path in context.site.get('assets', []):
            name, ext = os.path.splitext(asset_rel_path)
            if ext in context.config['ASSET_ADD_HASH']:
                asset_rel_path = '{}.{}{}'.format(name, md5hash(asset_full_path), ext)
            url = self.url_template.format(filename=asset_rel_path)
            yield AssetEntry(url, asset_id, asset_full_path)
