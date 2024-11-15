"""
Content generators.
"""


class Generator:

    def __init__(self, url_template, name):
        self.url_template = url_template
        self.name = name

    def generate(self, context):
        raise NotImplementedError()
