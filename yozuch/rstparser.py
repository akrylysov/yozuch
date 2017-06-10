"""
reStructuredText parser.
"""
import datetime
import docutils.readers.standalone
import docutils.readers.doctree
import docutils.core
import docutils.nodes
import docutils.utils
import docutils.io
from docutils.parsers.rst import Directive, directives
from docutils.writers.html5_polyglot import Writer, HTMLTranslator as BaseTranslator
from urllib.parse import urljoin
from yozuch import logger
from yozuch.generators.asset import AssetEntry  # TODO: do not import
from yozuch.utils import unique_list_items, is_external_url


_PUBLISH_SETTINGS = {
    'strip_comments': True,
    'initial_header_level': 3,
    'report_level': 2,
    'syntax_highlight': 'short',
    'stylesheet_path': None,
}


class _ReadMoreDirective(Directive):

    MARK = '~~YOZUCH_READMORE_MARK~~'

    has_content = False

    def run(self):
        return [docutils.nodes.raw('', self.MARK, format='html')]

directives.register_directive('read-more', _ReadMoreDirective)


def _get_reporter_observer(source):
    def reporter_observer(msg):
        if msg['level'] >= _PUBLISH_SETTINGS['report_level']:
            log_level = {
                0: logger.debug,
                1: logger.info,
                2: logger.warning,
                3: logger.error,
                4: logger.critical,
            }
            text = docutils.nodes.Element.astext(msg)
            log_level[msg['level']]('{source}, line {line}: {text}'.format(source=source, line=msg['line'], text=text))

    return reporter_observer


class _Reader(docutils.readers.standalone.Reader):

    def __init__(self):
        super().__init__()

    def new_document(self):
        doc = docutils.utils.new_document(self.source.source_path, self.settings)
        doc.reporter.stream = False
        doc.reporter.attach_observer(_get_reporter_observer(self.source.source_path))
        return doc


def get_html_translator(rooturl, permalink_text, references, entries):

    def is_asset(href):
        return entries is not None and href in entries and isinstance(entries[href], AssetEntry)

    class _HTMLTranslator(BaseTranslator):

        def __init__(self, doc):
            BaseTranslator.__init__(self, doc)

        def depart_title(self, node):
            close_tag = self.context[-1]
            parent = node.parent
            if permalink_text is not None and isinstance(parent, docutils.nodes.section) and parent.hasattr('ids') and parent['ids']:
                anchor_name = parent['ids'][0]
                if close_tag.startswith('</h'):
                    self.body.append(
                        '<a class="headerlink" href="#{}" title="Permalink to this headline">{}</a>'.format(anchor_name, permalink_text)
                    )
            super().depart_title(node)

        def visit_image(self, node):
            if rooturl is not None:
                uri = node['uri']
                if uri.find('://') == -1:
                    node['uri'] = urljoin(rooturl, uri)
            node['alt'] = ''
            super().visit_image(node)

        def visit_reference(self, node):
            atts = {'class': 'reference'}
            if 'refuri' in node:
                if references is not None and node['refuri'] in references:
                    node['refuri'] = references[node['refuri']]

                atts['href'] = node['refuri']
                if (self.settings.cloak_email_addresses
                        and atts['href'].startswith('mailto:')):
                    atts['href'] = self.cloak_mailto(atts['href'])
                    self.in_mailto = True
                atts['class'] += ' external'

                if is_external_url(atts['href']) or is_asset(atts['href']):
                    atts['target'] = '_blank'
            else:
                assert 'refid' in node, 'References must have "refuri" or "refid" attribute.'
                atts['href'] = '#' + node['refid']
                atts['class'] += ' internal'
            if not isinstance(node.parent, docutils.nodes.TextElement):
                assert len(node) == 1 and isinstance(node[0], docutils.nodes.image)
                atts['class'] += ' image-reference'
            self.body.append(self.starttag(node, 'a', '', **atts))

    return _HTMLTranslator


class Document(object):

    def __init__(self, doctree, filename, title):
        self.doctree = doctree
        self.filename = filename
        self.title = title
        self._metadata = {}
        self.slug = None

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, fields):
        self._metadata.update(fields)
        for key in fields:
            if key in ('author', 'date', 'slug'):
                setattr(self, key, fields[key])

    author = None
    date = None
    slug = None
    content = None
    summary = None


class RstParser(object):

    def __init__(self, options):
        self._options = options

    def _find_node(self, doctree, node_class, remove=True):
        for node in doctree.traverse(node_class):
            if remove:
                node.parent.remove(node)
            return node

    def _find_summary_and_remove_readmore(self, content):
        idx = content.find(_ReadMoreDirective.MARK)
        if idx != -1:
            summary = content[:idx]
            # TODO: think about a better way to close sections? rebuild doctree once more?
            # FIXME: summary may contain heading permalink
            summary += '</div>' * (summary.count('<div') - summary.count('</div'))
            return summary, content[:idx]+content[idx+len(_ReadMoreDirective.MARK):]
        return None, content

    def _parse_and_remove_title(self, doctree):
        node = self._find_node(doctree, docutils.nodes.title)
        if node is not None:
            return node.astext()

    def _parse_and_remove_fields(self, doctree):

        def list_parser(s):
            return unique_list_items(list(map(lambda i: i.strip(), s.split(','))))

        def date_parser(s):
            return datetime.datetime.strptime(s, self._options['meta_date_format'])

        parsers = {
            'tags': list_parser,
            'date': date_parser,
        }

        fields = self._find_node(doctree, docutils.nodes.field_list)
        if fields is not None:
            for field in fields:
                name = field[0].astext().lower()
                value = field[1].astext()
                if name in parsers:
                    value = parsers[name](value)
                yield name, value

    def parse(self, source, filename, additional_meta=None):
        doctree = docutils.core.publish_doctree(
            source=source,
            source_path=filename,
            reader=_Reader(),
            settings_overrides=_PUBLISH_SETTINGS,
        )
        if doctree.reporter.max_level < 3:
            doc = Document(doctree, filename, self._parse_and_remove_title(doctree))
            meta = dict(self._parse_and_remove_fields(doctree))
            if additional_meta:
                meta.update(additional_meta)
            doc.metadata = meta
            return doc

    def _publish(self, doctree, references, rooturl, entries):
        permalink_text = self._options['permalink_text'] if self._options['add_heading_permalink'] else None
        html_writer = Writer()
        html_writer.translator_class = get_html_translator(rooturl, permalink_text, references, entries)

        pub = docutils.core.Publisher(
            reader=docutils.readers.doctree.Reader(parser_name='null'),
            source=docutils.io.DocTreeInput(doctree),
            destination_class=docutils.io.StringOutput,
            writer=html_writer,
        )

        pub.process_programmatic_settings(None, _PUBLISH_SETTINGS, None)
        pub.publish()

        content = pub.writer.parts['fragment']
        return self._find_summary_and_remove_readmore(content)

    def publish(self, doc, references=None, rooturl=None, entries=None):
        doc.summary, doc.content = self._publish(doc.doctree, references, rooturl, entries)
