from sentence_transformers import SentenceTransformer, util
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
model = SentenceTransformer("flax-sentence-embeddings/st-codesearch-distilroberta-base")


def get_embedding(code: str):
    # replace newlines, which can negatively affect performance.
    code = code.replace("\n", " ")
    return model.encode(code, convert_to_tensor=True)
