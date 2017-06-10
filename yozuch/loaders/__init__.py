class Loader(object):
    name = None

    def load(self, context, path):
        raise NotImplementedError()


class RstDocumentLoader(Loader):

    @staticmethod
    def _set_document_id(kind, doc):
        doc.id = '/{}/{}'.format(kind, doc.filename)
