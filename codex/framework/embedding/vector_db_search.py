from enum import Enum

import vdblite

embedding_type = Enum('embedding_type', 'st unixcoder')


class VectorDB:
    def __init__(self, embed_type: embedding_type):
        if embed_type == embedding_type.st:
            self.vdb_st = vdblite.Vdb()
            self.vdb_st.load('tfix-source-code-embeddings-st.vdb')
        elif embed_type == embedding_type.unixcoder:
            self.vdb_unixcoder = vdblite.Vdb()
            self.vdb_unixcoder.load('tfix-source-code-embeddings-unixcoder.vdb')
        else:
            raise Exception('Invalid semantic search type')

    def search(self, query_source_code_embedding, embed_type: embedding_type):
        if embed_type == embedding_type.st:
            return self.vdb_st.search(query_source_code_embedding, 'vector', 1000)
        elif embed_type == embedding_type.unixcoder:
            return self.vdb_unixcoder.search(query_source_code_embedding, 'vector', 1000)
        else:
            raise Exception('Invalid semantic search type')
