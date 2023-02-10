import os
import sys
from enum import Enum

import vdblite

import models
from embedding import embedding_utils, embedding_unixcoder_utils

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from dataset.atlas_dataset import AtlasDataset

embedding_mode = Enum('embedding_mode', 'st_embedding unixcoder_embedding')
what_to_embed = Enum('what_to_embed', 'focal_method_and_test focal_method test_method')


def generate_and_persist_code_snippet_embedding(data: list[models.atlas_datapoint],
                                                what_info_embed_type: str,
                                                embed_type: embedding_mode):
    vdb = vdblite.Vdb()
    i = 0

    for dp in data:
        print(f"process record {i}")

        if what_info_embed_type == what_to_embed.focal_method_and_test:
            if len(dp.focal_method):
                code_snippet = dp.focal_method + '\n' + dp.test_method
            else:
                code_snippet = dp.test_method
        elif what_info_embed_type == what_to_embed.focal_method:
            code_snippet = dp.focal_method
        elif what_info_embed_type == what_to_embed.test_method:
            code_snippet = dp.test_method
        else:
            raise Exception("Invalid what_to_embed")

        # code_snippet = dp.test_method
        if embed_type == embedding_mode.unixcoder_embedding:
            embedding = embedding_unixcoder_utils.get_unixcoder_embedding(code_snippet)
        elif embed_type == embedding_mode.st_embedding:
            embedding = embedding_utils.get_embedding(code_snippet)
        else:
            raise Exception("Invalid embedding type")

        info = {'vector': embedding,
                'focal_method': dp.focal_method,
                'test_method': dp.test_method,
                'assertion': dp.assertion,
                'assertion_type': dp.assertion_type,
                'method_name': dp.method_name,
                'test_name': dp.test_name,
                'complexity': dp.complexity}
        print(f"loaded {i} items.")
        i = i + 1
        vdb.add(info)

    vdb.details()

    if embed_type == embedding_mode.unixcoder_embedding:
        vdb.save("atlas-test-method-embeddings-unixcoder.vdb")
    elif embed_type == embedding_mode.st_embedding:
        vdb.save("atlas-test-method-embeddings-st.vdb")
    else:
        raise Exception("Invalid embedding type")


def main(training_set_folder_path: str, test_set_folder_path: str,
         what_info_embed_type: what_to_embed, embed_type: embedding_mode):
    if training_set_folder_path and test_set_folder_path:
        training_set = AtlasDataset(training_set_folder_path + '/testMethods.txt',
                                    training_set_folder_path + '/assertLines.txt')

        training_data: list[models.atlas_datapoint] = training_set.parse()

        generate_and_persist_code_snippet_embedding(training_data, what_info_embed_type, embed_type)


if __name__ == "__main__":
    training_set_folder_path = None
    test_set_folder_path = None

    if len(sys.argv) >= 2:
        print(f"running script with options: {sys.argv}")

        training_set_folder_path = sys.argv[1]
        test_set_folder_path = sys.argv[2]

    # hard coding path
    training_set_folder_path = "dataset/atlas-dataset/Training"
    test_set_folder_path = "dataset/atlas-dataset/Testing"

    # training_set_folder_path = "/Volumes/wd-ssd-2tb/ubc-works/repos/embedding-experiment-atlas-st/neural-code-assistance/codex/framework/dataset/atlas-dataset/Training"
    # test_set_folder_path = "/Volumes/wd-ssd-2tb/ubc-works/repos/embedding-experiment-atlas-st/neural-code-assistance/codex/framework/dataset/atlas-dataset/Testing"

    embed_type = embedding_mode.st_embedding
    what_info_embed_type = what_to_embed.test_method
    main(training_set_folder_path, test_set_folder_path, what_info_embed_type, embed_type)
