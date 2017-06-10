from yozuch.loaders import RstDocumentLoader
from yozuch.loaders.rstloader import RstLoader


class DocumentLoader(RstDocumentLoader):
    name = 'documents'

    def load(self, context, path):
        for doc in RstLoader(context.config['RST_OPTIONS']).load_documents(path):
            self._set_document_id(self.name, doc)
            yield doc
