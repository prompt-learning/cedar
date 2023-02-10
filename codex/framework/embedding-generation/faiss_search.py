import os
import sys
from pprint import pprint as pp
from time import time
from typing import List

import faiss
import vdblite

import models
from dataset.atlas_dataset import AtlasDataset
from embedding.st_embedding import get_embedding, get_embeddings
from prompts.atlas_prompt import AtlasPrompt
from template import assert_templates

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def build_vector_database(atlas_datapoints):
    for raw_record in atlas_datapoints:
        print(raw_record.test_method)
        code_snippet_emd = get_embedding(raw_record.test_method)
        print(code_snippet_emd)

    test_methods = []
    for raw_record in atlas_datapoints:
        test_methods.append(raw_record.test_method)

    # https://www.pinecone.io/learn/faiss-tutorial/
    code_snippet_emddings = get_embeddings(test_methods)
    print(code_snippet_emddings.shape)

    d = code_snippet_emddings.shape[1]
    index = faiss.IndexFlatL2(d)
    print(index.is_trained)

    index.add(code_snippet_emddings)
    print(index.ntotal)

    k = 2
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("flax-sentence-embeddings/st-codesearch-distilroberta-base")
    xq = model.encode(["def sum()"])

    D, I = index.search(xq, k)  # search
    print(I)
    print(D)


def build_atlas_assertion_prompt(demonstrations: List[models.atlas_datapoint],
                                 inference: models.atlas_datapoint,
                                 with_commands=True) -> AtlasPrompt:
    query = assert_templates.get_atlas_query_template(inference, with_commands)

    assertion_prompt = AtlasPrompt(demonstrations, query, with_commands)
    return assertion_prompt


def main(training_set_folder_path: str, test_set_folder_path: str, with_commands: bool):
    assertion_prompts: list[AtlasPrompt] = []
    if training_set_folder_path and test_set_folder_path:
        training_set = AtlasDataset(training_set_folder_path + '/testMethods.txt',
                                    training_set_folder_path + '/assertLines.txt')
        test_set = AtlasDataset(test_set_folder_path + '/testMethods.txt',
                                test_set_folder_path + '/assertLines.txt')

        training_data: list[models.atlas_datapoint] = training_set.parse()
        test_data: list[models.atlas_datapoint] = test_set.parse()
        generate_and_persist_code_snippet_embedding(training_data)
    else:
        dataset = AtlasDataset('../dataset/dataset-samples/atlas-source-sample.txt',
                               'dataset/dataset-samples/atlas-target-sample.txt')
        raw_records: list[models.atlas_datapoint] = dataset.parse()
        ap: AtlasPrompt = build_atlas_assertion_prompt(raw_records[:len(raw_records) - 1], raw_records[-1],
                                                       with_commands)
        assertion_prompt: str = ap.construct_prompt()
        assertion_prompts.append(ap)

        build_vector_database(raw_records)
        demo_load_code_snippet_embedding()


def generate_and_persist_code_snippet_embedding(test_data: list[models.atlas_datapoint]):
    vdb = vdblite.Vdb()
    i = 0
    for datapoint in test_data:
        print(datapoint.test_method)
        code_snippet = datapoint.test_method
        code_snippet_embedding = get_embedding(code_snippet)
        info = {'vector': code_snippet_embedding,
                'time': time(),
                'uuid': str(code_snippet)}
        print(f"loaded {i} items")
        i = i + 1
        vdb.add(info)

    vdb.details()
    vdb.save("train-method-embeddings.csv")


def demo_load_code_snippet_embedding():
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

    code_snippet_3 = """ 
   # JavaScript 
   for (var option in fieldData.options) {
        option = fieldData.options[option];
    """

    snippet_1_embedding = get_embedding(code_snippet_1)
    snippet_2_embedding = get_embedding(code_snippet_2)
    snippet_3_embedding = get_embedding(code_snippet_3)

    vdb = vdblite.Vdb()

    info = {'vector': snippet_1_embedding, 'time': time(), 'uuid': str(code_snippet_1)}
    vdb.add(info)

    info = {'vector': snippet_2_embedding, 'time': time(), 'uuid': str(code_snippet_2)}
    vdb.add(info)

    info = {'vector': snippet_3_embedding, 'time': time(), 'uuid': str(code_snippet_3)}
    vdb.add(info)

    vdb.details()
    query_embedding = get_embedding("for (var option")
    results = vdb.search(query_embedding, count=2)
    pp(results)

    vdb.save("embedding.csv")


def load_and_search_db():
    vdb = vdblite.Vdb()
    vdb.load("train-method-embeddings.csv")
    query_embedding = get_embedding("for (var option")
    results = vdb.search(query_embedding, count=2)
    pp(results)


if __name__ == "__main__":
    training_set_folder_path = None
    test_set_folder_path = None
    with_commands = True

    if len(sys.argv) >= 2:
        training_set_folder_path = sys.argv[1]
        test_set_folder_path = sys.argv[2]
        with_commands = sys.argv[3]

    # hard coding path
    #training_set_folder_path = "dataset/atlas-dataset/Training"
    #test_set_folder_path = "dataset/atlas-dataset/Testing"
    #main(training_set_folder_path, test_set_folder_path, with_commands)

    load_and_search_db()
