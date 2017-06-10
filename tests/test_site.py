import os
import shutil
import difflib
import codecs
from yozuch.builder import build
from tests import YozuchTestCase


class BuilderTest(YozuchTestCase):

    IGNORE_PATTERNS = ('.DS_Store',)

    def _assertDirectoryContent(self, first, second):
        names = os.listdir(first)
        ignore = shutil.ignore_patterns(*self.IGNORE_PATTERNS)(first, names)
        for name in names:
            if name not in ignore:
                first_path = os.path.join(first, name)
                second_path = os.path.join(second, name)
                if os.path.isdir(first_path):
                    self._assertDirectoryContent(first_path, second_path)
                else:
                    self.assertTrue(os.path.isfile(second_path), 'Unable to find {}'.format(second_path))
                    if os.path.splitext(name)[1] in ('.html', '.xml', '.txt'):
                        with codecs.open(first_path, 'r', 'utf-8-sig') as f1, codecs.open(second_path, 'r', 'utf-8-sig') as f2:
                            diff = list(difflib.unified_diff(
                                f1.readlines(),
                                f2.readlines(),
                                fromfile=first_path,
                                tofile=second_path)
                            )
                            self.assertEqual(len(diff), 0, '\n'.join(diff))

    def test_build(self):
        source_path = os.path.join(self.ROOT_DIR, 'data')
        output_path = os.path.join(source_path, 'output')
        compiled_data_path = os.path.join(self.ROOT_DIR, 'compiled-data')
        shutil.rmtree(output_path, True)
        build(source_path)
        self._assertDirectoryContent(compiled_data_path, output_path)
        shutil.rmtree(output_path, True)
