import codecs
import os
import datetime
from yozuch.rstparser import RstParser
from tests import YozuchTestCase


class RstParserTest(YozuchTestCase):

    def read_file(self, filename):
        path = os.path.join(self.ROOT_DIR, 'data', filename)
        with codecs.open(path, 'r', 'utf-8-sig') as f:
            return path, f.read()

    def parse(self, filename, **kwargs):
        path, text = self.read_file(filename)
        doc = self.parser.parse(text, path, **kwargs)
        if doc is not None:
            self.parser.publish(doc)
        return doc

    def setUp(self):
        super(RstParserTest, self).setUp()
        self.parser = RstParser(self.config['RST_OPTIONS'])

    def test_post(self):
        doc = self.parse(os.path.join('posts', 'post.rst'))
        self.assertEqual(doc.title, '测试')
        self.assertEqual(doc.summary, None)
        self.assertEqual(doc.date, datetime.datetime(2013, 10, 2))
        self.assertEqual(doc.metadata['tags'], ['tag1'])
        self.assertEqual(doc.author, 'author1')
        self.assertEqual(doc.metadata['author'], 'author1')
        self.assertFalse(self._is_logger_errors())

    def test_post_additional_meta(self):
        doc = self.parse(os.path.join('posts', '2013-09-20-post-file-metadata.rst'),
                         additional_meta={'date': datetime.datetime(2013, 9, 20), 'slug': 'post-file-metadata'})
        self.assertEqual(doc.title, 'Title')
        self.assertEqual(doc.slug, 'post-file-metadata')
        self.assertEqual(doc.content, '<p>Content.</p>\n')
        self.assertEqual(doc.summary, None)
        self.assertEqual(doc.date, datetime.datetime(2013, 9, 20))
        self.assertEqual(doc.metadata['category'], 'cat2')
        self.assertEqual(doc.metadata['tags'], ['tag1', 'tag 2'])
        self.assertFalse(self._is_logger_errors())

    def test_post_additional_default_meta(self):
        doc = self.parse(os.path.join('posts', 'post-readmore.rst'), additional_meta={'category': 'additional'})
        self.assertEqual(doc.metadata['category'], 'additional')
        self.assertFalse(self._is_logger_errors())

    def test_post_readmore(self):
        doc = self.parse(os.path.join('posts', 'post-readmore.rst'))
        self.assertEqual(doc.title, 'ReadMore')
        self.assertEqual(doc.content, '<p>foo</p>\n<div class="section" id="section">\n<h3>Section<a class="headerlink" href="#section" title="Permalink to this headline">&#x00b6;</a></h3>\n<p>bar</p>\n<p>baz</p>\n</div>\n')
        self.assertEqual(doc.summary, '<p>foo</p>\n<div class="section" id="section">\n<h3>Section<a class="headerlink" href="#section" title="Permalink to this headline">&#x00b6;</a></h3>\n<p>bar</p>\n</div>')
        self.assertEqual(doc.date, datetime.datetime(2011, 1, 1))
        self.assertFalse(self._is_logger_errors())

    def test_post_error(self):
        doc = self.parse(os.path.join('posts', 'post-error.rst'))
        self.assertEqual(doc, None)
        self.assertEqual(len(self.logger_handler.messages['error']), 1)

    def test_page(self):
        doc = self.parse(os.path.join('documents', 'page.rst'))
        self.assertEqual(doc.title, 'Заголовок')
        self.assertEqual(doc.slug, None)
        self.assertEqual(doc.content, '<p>Содержимое</p>\n')
        self.assertEqual(doc.summary, None)
        self.assertFalse(self._is_logger_errors())
