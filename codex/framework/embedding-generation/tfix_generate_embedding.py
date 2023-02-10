import os
import sys
from enum import Enum

import vdblite

file_dir = os.path.dirname(__file__)
sys.path.append('..')
#sys.path.append(file_dir)

import models
from dataset.tfix_dataset import TFixDataset
from embedding import embedding_utils, embedding_unixcoder_utils

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

embedding_mode = Enum('embedding_mode', 'st_embedding unixcoder_embedding')


def generate_and_persist_code_snippet_embedding(data: list[models.tfix_datapoint],
                                                embedding_type: embedding_mode):
    vdb = vdblite.Vdb()
    i = 0

    for dp in data[:5]:
        print(dp.source_code)
        source_code = dp.source_code

        if embedding_type == embedding_mode.unixcoder_embedding:
            source_code_embedding = embedding_unixcoder_utils.get_unixcoder_embedding(source_code)
        elif embedding_type == embedding_mode.st_embedding:
            source_code_embedding = embedding_utils.get_embedding(source_code)
        else:
            raise Exception("Invalid embedding type")

        info = {'vector': source_code_embedding,
                'source_code': dp.source_code,
                'target_code': dp.target_code,
                'linter_report_message': dp.linter_report_message,
                'linter_report_rule_id': dp.linter_report_rule_id,
                'warning_line': dp.warning_line,
                'repo': dp.repo}
        print(f"loaded {i} items.")
        i = i + 1
        vdb.add(info)

    vdb.details()
    vdb.save("tfix-source-code-embeddings-st.vdb")


def main(training_set_file_path: str, test_set_file_path: str, embedding_type: embedding_mode):
    if training_set_folder_path and test_set_folder_path:
        training_set = TFixDataset(training_set_file_path)
        test_set = TFixDataset(test_set_file_path)

        training_data: list[models.tfix_datapoint] = training_set.parse()
        test_data: list[models.tfix_datapoint] = test_set.parse()
        generate_and_persist_code_snippet_embedding(training_data, embedding_type)


if __name__ == "__main__":
    training_set_folder_path = None
    test_set_folder_path = None

    if len(sys.argv) >= 2:
        print(f"running script with options: {sys.argv}")
        training_set_folder_path = sys.argv[1]
        test_set_folder_path = sys.argv[2]

    # hard coding path - clean test
    training_set_folder_path = "../dataset/tfix-dataset/clean-test/train_data.json"
    test_set_folder_path = "../dataset/tfix-dataset/clean-test/test_data.json"

    embedding_type = embedding_mode.unixcoder_embedding
    main(training_set_folder_path, test_set_folder_path, embedding_mode)
