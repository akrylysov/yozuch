import os
import shutil
import fnmatch
from yozuch.utils import makedirs, path_from_url
from yozuch.generators import Generator
from yozuch.entries import Entry


def fnmatch_patterns(name, patterns):
    return any([fnmatch.fnmatch(name, pattern) for pattern in patterns])


class AssetEntry(Entry):

    def __init__(self, url, source_path):
        super().__init__(url)
        self.source_path = source_path

    def write(self, context, env, output_dir):
        path = os.path.join(output_dir, path_from_url(self.url))
        makedirs(os.path.dirname(path))
        shutil.copyfile(self.source_path, path)


class AssetGenerator(Generator):

    DEFAULT_IGNORE_PATTERNS = ['.DS_Store']

    def __init__(self, url_template, name, ignore=DEFAULT_IGNORE_PATTERNS):
        super().__init__(url_template, name)
        self.ignore = ignore

    def generate(self, context):
        for source_path, relpath in context.site.get('assets', []):
            if not fnmatch_patterns(os.path.basename(source_path), self.ignore) and not fnmatch_patterns(relpath, self.ignore):
                yield AssetEntry(self.url_template.format(filename=relpath), source_path)
