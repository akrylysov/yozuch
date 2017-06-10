"""
reStructuredText loader.
"""

import os
import codecs
import re
import datetime
from yozuch.rstparser import RstParser


class RstLoader(object):

    def __init__(self, options):
        self._options = options
        self._filename_meta_regexs = [re.compile(rs) for rs in options['filename_meta_formats']]

    def _parse_filename_meta(self, name):
        parsers = {
            'date': lambda s: datetime.datetime.strptime(s, self._options['filename_meta_date_format'])
        }
        for regex in self._filename_meta_regexs:
            result = regex.search(name)
            if result is None:
                continue
            fields = result.groupdict()
            for name, parser in parsers.items():
                if name in fields:
                    fields[name] = parser(fields[name])
            return fields

    def load_documents(self, content_dir):
        for filename in os.listdir(content_dir):
            if filename.startswith('~'):
                continue
            path = os.path.join(content_dir, filename)
            if os.path.isfile(path):
                name, ext = os.path.splitext(filename)
                if ext in self._options['file_extensions']:
                    with codecs.open(path, 'r', 'utf-8-sig') as f:
                        parser = RstParser(self._options)
                        doc = parser.parse(f.read(), filename, additional_meta=self._parse_filename_meta(name))
                        if doc is not None:
                            yield doc
