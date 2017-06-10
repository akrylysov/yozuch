import docutils.nodes
from docutils.parsers.rst import Directive, directives


class IframeVideo(Directive):

    DEFAULT_WIDTH = 700
    DEFAULT_HEIGHT = 400
    DEFAULT_ALIGN = 'left'

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'height': directives.nonnegative_int,
        'width': directives.nonnegative_int,
        'align': lambda argument: directives.choice(argument, ('left', 'center', 'right')),
    }

    def run(self):
        self.options['video_id'] = directives.uri(self.arguments[0])
        if 'width' not in self.options:
            self.options['width'] = self.DEFAULT_WIDTH
        if 'height' not in self.options:
            self.options['height'] = self.DEFAULT_HEIGHT
        if 'align' not in self.options:
            self.options['align'] = self.DEFAULT_ALIGN
        return [docutils.nodes.raw('', self.html_code.format(**self.options), format='html')]


class Youtube(IframeVideo):
    html_code = '<div class="align-{align} responsive-embed widescreen media">' \
                '<iframe width="{width}" height="{height}" src="https://www.youtube.com/embed/{video_id}"' \
                ' frameborder="0" allowfullscreen></iframe></div>'


def register(context):
    directives.register_directive('youtube', Youtube)
