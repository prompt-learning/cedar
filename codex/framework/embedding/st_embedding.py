from sentence_transformers import SentenceTransformer, util
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
model = SentenceTransformer("flax-sentence-embeddings/st-codesearch-distilroberta-base")

def get_embedding(code: str):
    # replace newlines, which can negatively affect performance.
    code = code.replace("\n", " ")
    return model.encode(code, convert_to_tensor=True)

def get_embeddings(code_snippets: str):
    # replace newlines, which can negatively affect performance.
    return model.encode(code_snippets)


def snippet_similarity(snippet_1, snippet_2):
    snippet_1_embedding = get_embedding(snippet_1)
    snippet_2_embedding = get_embedding(snippet_2)
    cos_similarity = util.cos_sim(snippet_1_embedding, snippet_2_embedding)
    return cos_similarity


def throw_literals():
    code_snippet_1 = """
    # JavaScript
    if(spaceBefore !== NULL && localStorage.remainingSpace === spaceBefore) {
        throw 'QUOTA_EXCEEDED_ERR';
    }
"""

    code_snippet_2 = """
   # JavaScript 
   if (prev_output.is_stable === 0)
        throw \"prev is not stable\";
    if (prev_output.is_serial === 1 && prev_output.sequence !== 'good')
    """
    score = snippet_similarity(code_snippet_1, code_snippet_2)
    print(f"similarity score:{score}")
    return score


def throw_literals_vs_for_in():
    code_snippet_1 = """ 
   # JavaScript 
   for (var option in fieldData.options) {
        option = fieldData.options[option];
"""

    code_snippet_2 = """
   # JavaScript 
   if (prev_output.is_stable === 0)
        throw \"prev is not stable\";
    if (prev_output.is_serial === 1 && prev_output.sequence !== 'good')
    """
    score = snippet_similarity(code_snippet_1, code_snippet_2)
    print(f"similarity score:{score}")
    return score


def main():
    print("both examples are throw literals")
    throw_literals()  #
    print("=================================")
    print("throw literals and for in comparison")
    throw_literals_vs_for_in()
    print("=================================")


if __name__ == "__main__":
    main()
