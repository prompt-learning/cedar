import csv
import hashlib
import os
import sys
import time
from typing import List

from rank_bm25 import BM25Okapi

import models
from codex_api.codex_api_zero_shot import CodexAPIZeroShot
from models import atlas_mode
from template.assert_templates import get_atlas_demo_template
from util import utils
from util.utils import str2bool

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from codex_api.codex_api import CodexAPI
from evaluation.evaluation import Evaluation
from prompts.atlas_prompt import AtlasPrompt, build_atlas_assertion_prompt, build_atlas_assertion_prompt_with_mode, \
    build_atlas_assertion_prompt_bm25
from dataset.atlas_dataset import AtlasDataset


def invoke(codex_api: CodexAPI, ap: str) -> object:
    return codex_api.get_suggestions(ap)


def prompt_codex(testdata: list[models.atlas_datapoint],
                 assertion_prompts: List[AtlasPrompt],
                 shot_mode: atlas_mode,
                 dry_run: bool = False,
                 ) -> None:
    results: List[str] = []
    if shot_mode is atlas_mode.zero_shot:
        codex_api = CodexAPIZeroShot()
    else:
        codex_api = CodexAPI()

    seq = 0
    exact_match_so_far = 0
    for prompt in assertion_prompts:
        if not dry_run:
            print(f"process record {seq}")
            expected_response = testdata[seq].assertion
            (inference_time, response_actual, response_completion_tokens, response_prompt_tokens,
             response_total_tokens) = invoke(codex_api, prompt)
            print(response_actual)
            result = Evaluation(response_actual, expected_response).calculate()
            print(result)
            results.append(models.atlas_result(prompt=prompt,
                                               expected=expected_response,
                                               actual=response_actual,
                                               is_exact_match=result["is_exact_match"],
                                               is_match=result["is_match"],
                                               lcs=result["calc_lcs"],
                                               edit_distance=result["edit_distance"],
                                               inference_time=inference_time,
                                               gpt_token_count=utils.count_codex_tokens(prompt),
                                               word_count=utils.word_count(prompt),
                                               response_completion_tokens=response_completion_tokens,
                                               response_prompt_tokens=response_prompt_tokens,
                                               response_total_tokens=response_total_tokens
                                               ))

            if result["is_exact_match"]:
                exact_match_so_far += 1

            accuracy_so_far = exact_match_so_far / (seq + 1)
            accuracy_percentage_so_far = round(100 * accuracy_so_far, 3)
            print(f"accuracy: {accuracy_percentage_so_far}%")

            seq = seq + 1

    if not dry_run:
        output_file_name = "./results.csv"
        with open(output_file_name, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                ['prompt', 'expected', 'actual', 'is_exact_match', 'is_match', 'lcs', 'edit_distance',
                 'inference_time (secs)',
                 'gpt_token_count', 'word_count',
                 'response_completion_tokens', 'response_prompt_tokens', 'response_total_tokens'])
            writer.writerows(results)
        print(f"output: csv file: {output_file_name}")

def load_bm_25(bm_25_cache_dict, test_methods, training_data_with_length):
    start_time = time.time()
    how_many_md5hash_conflicts = 0

    for dp in training_data_with_length:
        tokenized_test_method = dp.datapoint.test_method.split(" ")
        md5hash = hashlib.md5(" ".join(tokenized_test_method).encode('utf-8')).hexdigest()

        if md5hash in bm_25_cache_dict:
            how_many_md5hash_conflicts += 1
        else:
            bm_25_cache_dict[md5hash] = dp
        test_methods.append(dp.datapoint.test_method)

    print("how_many_md5hash_conflicts: ", how_many_md5hash_conflicts)
    bm25 = BM25Okapi(test_methods)

    end_time = time.time()
    print("load_bm_25: ", end_time - start_time)
    print("The size of the bm25 cache is {} bytes".format(sys.getsizeof(bm_25_cache_dict)))
    print(f"total entries: {len(bm_25_cache_dict.keys())}")
    return bm25

def main(training_set_folder_path: str, test_set_folder_path: str, with_commands: bool, mode: models.atlas_mode):
    assertion_prompts: list[AtlasPrompt] = []

    if training_set_folder_path and test_set_folder_path:
        training_set = AtlasDataset(training_set_folder_path + '/testMethods.txt',
                                    training_set_folder_path + '/assertLines.txt')
        test_set = AtlasDataset(test_set_folder_path + '/testMethods.txt',
                                test_set_folder_path + '/assertLines.txt')

        training_data: list[models.atlas_datapoint] = training_set.parse()
        test_data: list[models.atlas_datapoint] = test_set.parse()

        training_data_with_length: list[models.atlas_datapoint_with_demo_length] = []
        for datapoint in training_data:
            token_count = utils.count_codex_tokens(get_atlas_demo_template(datapoint, with_commands))
            training_data_with_length.append(models.atlas_datapoint_with_demo_length(datapoint, token_count))

        bm_25_cache_dict = {}
        test_methods = []
        if mode == atlas_mode.bm_25:
            bm25 = load_bm_25(bm_25_cache_dict, test_methods, training_data_with_length)

        seq = 0
        for t in test_data:
            start_time = time.time()

            if mode is None or mode is models.atlas_mode.semantic_search:
                ap: AtlasPrompt = build_atlas_assertion_prompt(training_data, t, with_commands)
            elif mode is models.atlas_mode.bm_25:
                ap: AtlasPrompt = build_atlas_assertion_prompt_bm25(training_data=training_data,
                                                                    bm25=bm25,
                                                                    test_methods=test_methods,
                                                                    bm_25_cache_dict=bm_25_cache_dict,
                                                                    inference=t,
                                                                    with_commands=with_commands)
            else:
                ap: AtlasPrompt = build_atlas_assertion_prompt_with_mode(training_data=training_data,
                                                                         training_data_with_length=training_data_with_length,
                                                                         inference=t,
                                                                         with_commands=with_commands,
                                                                         mode=mode)

            assertion_prompt: str = ap.construct_prompt()
            if mode is models.atlas_mode.semantic_search:
                assertion_prompt: str = ap.construct_prompt_semantic_search(t)

            end_time = time.time()
            duration = end_time - start_time
            print(f"processing record to a prompt: {seq}, time_taken: {duration}")
            seq = seq + 1

            assertion_prompts.append(assertion_prompt)
        prompt_codex(test_data, assertion_prompts, mode, dry_run=False)
    else:
        dataset = AtlasDataset('dataset/dataset-samples/atlas-source-sample.txt',
                               'dataset/dataset-samples/atlas-target-sample.txt')
        raw_records: list[models.atlas_datapoint] = dataset.parse()
        ap: AtlasPrompt = build_atlas_assertion_prompt(raw_records[:len(raw_records) - 1], raw_records[-1],
                                                       with_commands)
        assertion_prompt: str = ap.construct_prompt()
        assertion_prompts.append(ap)
        print(assertion_prompt)


if __name__ == "__main__":
    training_set_folder_path = None
    test_set_folder_path = None
    with_commands = True
    mode = None

    print("""arguments hard coded - change in this file:
      - training_set_folder_path and test_set_folder_path hard coded to read from "dataset" folder
      - with_commands for with or without natural language commands (hard coded to True - Line 217)
      - see list of modes from atlas_mode enum ((hard coded to True - Line 217))
      """)

    if len(sys.argv) >= 2:
        print(f"running script with options: {sys.argv}")

        training_set_folder_path = sys.argv[1]
        test_set_folder_path = sys.argv[2]
        with_commands = str2bool(sys.argv[3])
        mode = sys.argv[4]

        if mode == "zero_shot":
            mode = atlas_mode.zero_shot
        elif mode == "random_1_shot":
            mode = atlas_mode.random_1_shot
        elif mode == "random_n_shot":
            mode = atlas_mode.random_n_shot
        elif mode == "random_assertion_by_category_n_shot":
            mode = atlas_mode.random_assertion_by_category_n_shot
        else:
            raise Exception("Invalid mode")

    # hard coding path
    training_set_folder_path = "dataset/atlas-dataset/Training"
    test_set_folder_path = "dataset/atlas-dataset/Testing"
    # mode = select_mode.zero_shot
    # mode = atlas_mode.semantic_search
    # mode = atlas_mode.bm_25

    #mode = atlas_mode.random_n_shot_until_context_window
    #with_commands = True

    mode = atlas_mode.bm_25
    with_commands = True
    main(training_set_folder_path, test_set_folder_path, with_commands, mode)
