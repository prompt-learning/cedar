from enum import Enum

import vdblite

embedding_type = Enum('embedding_type', 'st unixcoder')


class VectorDBATLAS:
    def __init__(self, embed_type: embedding_type):
        if embed_type == embedding_type.st:
            self.vdb = vdblite.Vdb()
            self.vdb.load('atlas-test-method-embeddings-st.vdb')
            print("ATLAS vector DB loaded")
        else:
            raise Exception('Invalid semantic search type')

    def search(self, query_source_code_embedding, embed_type: embedding_type):
        if embed_type == embedding_type.st:
            return self.vdb_st.search(query_source_code_embedding, 'vector', 1000)
        else:
            raise Exception('Invalid semantic search type')
