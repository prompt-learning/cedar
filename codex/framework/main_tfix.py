import csv
import os
import sys
import time
import hashlib
from typing import List
from rank_bm25 import BM25Okapi
import models
from models import tfix_mode
from codex_api.codex_api import CodexAPI
from codex_api.codex_api_top_n import CodexAPITopN
from codex_api.codex_api_zero_shot import CodexAPIZeroShot
from dataset.tfix_dataset import TFixDataset
from prompts.tfix_prompt import TFixPrompt, build_tfix_repair_prompt, tfix_template_type, \
    build_tfix_repair_prompt_with_mode, build_tfix_repair_prompt_bm25
from prompts.tfix_shot_examples.random_n_shot import tfix_datapoint_with_demo_length
from template.tfix_templates import get_tfix_demo_template
from util import utils
from util.utils import str2bool

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from evaluation.evaluation_tfix import Evaluation


def invoke(codex_api: CodexAPI, ap: str) -> object:
    return codex_api.get_suggestions(ap, max_tokens=500)


def invoke_zero_shot(codex_api: CodexAPI, ap: str, stop_token: str) -> object:
    return codex_api.get_suggestions_with_any_stop_token(ap, stop_token=stop_token, max_tokens=500)


def invoke_top_n(codex_api: CodexAPITopN, ap: str) -> object:
    return codex_api.get_suggestions(ap, max_tokens=500)


def prompt_codex(testdata: list[models.tfix_datapoint],
                 tfix_prompts: list[TFixPrompt],
                 shot_mode: tfix_mode,
                 dry_run: bool = False, ) -> None:
    results_detailed: List[str] = []
    results_without_prompt: List[str] = []

    #if shot_mode is tfix_mode.zero_shot:
    #    codex_api = CodexAPIZeroShot()
    #    codex_api = CodexAPI()
    #elif shot_mode is tfix_mode.random_assertion_by_category_n_shot_top_n:
    codex_api = CodexAPI()

    seq = 0
    exact_match_so_far = 0
    for prompt in tfix_prompts:
        if not dry_run:
            print(f"process record {seq}")
            expected_response = testdata[seq].target_code

            if mode is tfix_mode.zero_shot:
                (inference_time, response_codex, response_completion_tokens, response_prompt_tokens,
                 response_total_tokens) = invoke_zero_shot(codex_api, prompt, stop_token="###")
            else:
                (inference_time, response_codex, response_completion_tokens, response_prompt_tokens,
                 response_total_tokens) = invoke(codex_api, prompt)

            print(response_codex)
            warning_line = testdata[seq].warning_line
            result = Evaluation(buggy_code=testdata[seq].source_code, expected=expected_response, codex=response_codex, warning_line=warning_line).calculate()
            print(result)
            results_detailed.append(models.tfix_result(prompt=prompt,
                                                       warning_line=warning_line,
                                                       linter_report_rule_id=testdata[seq].linter_report_rule_id,
                                                       linter_report_message=testdata[seq].linter_report_message,
                                                       expected=expected_response,
                                                       codex=response_codex,
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

            results_without_prompt.append(models.tfix_result_without_prompt(buggy_code=testdata[seq].source_code,
                                                                            warning_line=warning_line,
                                                                            linter_report_rule_id=testdata[seq].linter_report_rule_id,
                                                                            linter_report_message=testdata[seq].linter_report_message,
                                                                            expected=expected_response,
                                                                            codex=response_codex,
                                                                            is_exact_match=result["is_exact_match"],
                                                                            is_match=result["is_match"],
                                                                            lcs=result["calc_lcs"],
                                                                            edit_distance=result["edit_distance"],
                                                                            inference_time=inference_time,
                                                                            gpt_token_count=utils.count_codex_tokens(
                                                                                prompt),
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
        output_file_name = "./results-detail-debug.csv"
        with open(output_file_name, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                ['prompt', 'warning_line',
                 'linter_report_rule_id', 'linter_report_message',
                 'expected', 'codex',
                 'is_exact_match', 'is_match',
                 'lcs', 'edit_distance',
                 'inference_time (secs)',
                 'gpt_token_count',
                 'word_count',
                 'response_completion_tokens',
                 'response_prompt_tokens',
                 'response_total_tokens'])
            writer.writerows(results_detailed)
        print(f"output: csv file: {output_file_name}")

        output_file_name = "./results-without_prompt.csv"
        with open(output_file_name, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                ['buggy_code', 'warning_line',
                  'linter_report_rule_id', 'linter_report_message',
                 'expected', 'codex',
                 'is_exact_match', 'is_match',
                 'lcs', 'edit_distance',
                 'inference_time (secs)',
                 'gpt_token_count',
                 'word_count',
                 'response_completion_tokens',
                 'response_prompt_tokens',
                 'response_total_tokens'])
            writer.writerows(results_without_prompt)
        print(f"output: csv file: {output_file_name}")

def load_bm_25(bm_25_cache_dict, buggy_code_corpus, training_data):
    start_time = time.time()
    how_many_md5hash_conflict = 0

    for dp in training_data:
        tokenized_buggy_code = dp.source_code.split(" ")

        md5hash = hashlib.md5(" ".join(tokenized_buggy_code).encode('utf-8')).hexdigest()
        if md5hash in bm_25_cache_dict:
            how_many_md5hash_conflict += 1
        else:
            bm_25_cache_dict[md5hash] = dp
        buggy_code_corpus.append(dp.source_code.split(" "))

    print(f"how_many_md5hash_conflict: {how_many_md5hash_conflict}")
    bm25 = BM25Okapi(buggy_code_corpus)

    end_time = time.time()
    print("duration for populating bm25 cache: " + str(end_time - start_time))
    print("The size of the bm25 cache is {} bytes".format(sys.getsizeof(bm_25_cache_dict)))
    return bm25

def main(training_set_file_path: str, test_set_file_path: str,
         with_commands: bool,
         mode: str,
         template_type: tfix_template_type):
    tfix_prompts: list[TFixPrompt] = []

    if training_set_folder_path and test_set_folder_path:
        training_set = TFixDataset(training_set_file_path)
        test_set = TFixDataset(test_set_file_path)

        training_data: list[models.tfix_datapoint] = training_set.parse()
        test_data: list[models.tfix_datapoint] = test_set.parse()

        training_data_with_length: list[tfix_datapoint_with_demo_length] = []
        for datapoint in training_data:
            token_count = utils.count_codex_tokens(get_tfix_demo_template(datapoint, with_commands))
            training_data_with_length.append(tfix_datapoint_with_demo_length(datapoint, token_count))

        bm_25_cache_dict = {}
        buggy_code_corpus = []
        if mode == tfix_mode.bm_25:
            bm25 = load_bm_25(bm_25_cache_dict, buggy_code_corpus, training_data)

        seq = 0
        for t in test_data:
            start_time = time.time()

            if mode is None:
                tp: TFixPrompt = build_tfix_repair_prompt(training_data, t, with_commands, template_type)
            elif mode == tfix_mode.bm_25:
                tp: TFixPrompt = build_tfix_repair_prompt_bm25(training_data=training_data,
                                                               training_data_with_length=training_data_with_length,
                                                               bm25=bm25,
                                                               buggy_code_corpus=buggy_code_corpus,
                                                               bm_25_cache_dict=bm_25_cache_dict,
                                                               inference=t,
                                                               with_commands=with_commands)
            else:
                tp: TFixPrompt = build_tfix_repair_prompt_with_mode(training_data=training_data,
                                                                    training_data_with_length=training_data_with_length,
                                                                    inference=t,
                                                                    with_commands=with_commands,
                                                                    mode=mode)
                # tp: TFixPrompt = build_tfix_repair_prompt(training_data, t, with_commands, template_type)

            if mode is tfix_mode.zero_shot \
                    or mode is tfix_mode.random_1_shot \
                    or mode is tfix_mode.random_52_shot \
                    or mode is tfix_mode.random_52_shot_1_example_per_category \
                    or mode is tfix_mode.random_n_shot_until_context_window \
                    or mode is tfix_mode.bm_25:
                tp_prompt: str = tp.construct_prompt()
            elif mode is tfix_mode.random_assertion_by_category_n_shot_util_8000_tokens:
                tp_prompt: str = tp.construct_prompt_more_example_of_a_given_violation_until_8000_tokens(template_type)
            elif mode is tfix_mode.semantic_search_st_n_shot:
                tp_prompt: str = tp.construct_prompt_semantic_search(t, template_type)
            else:
                tp_prompt: str = tp.construct_prompt_more_example_of_a_given_violation()

            end_time = time.time()
            duration = end_time - start_time
            print(f"processing record to a prompt: {seq}, time_taken: {duration}")
            seq = seq + 1

            tfix_prompts.append(tp_prompt)
        prompt_codex(test_data, tfix_prompts, mode, dry_run=False)
    else:
        dataset = TFixDataset('dataset/dataset-samples/tfix-sample.json')
        raw_records: list[models.tfix_datapoint] = dataset.parse()

        tp: TFixPrompt = build_tfix_repair_prompt(raw_records[:len(raw_records) - 1],
                                                  raw_records[-1],
                                                  with_commands)
        tfix_prompt: str = tp.construct_prompt()
        tfix_prompts.append(tp)
        print(tfix_prompt)


if __name__ == "__main__":
    training_set_folder_path = None
    test_set_folder_path = None
    with_commands = True
    mode = None

    print("""arguments order: training_set_folder_path test_set_folder_path with_commands mode""")
    print("""arguments hard coded - change in this file:
      - training_set_folder_path and test_set_folder_path hard coded to read from "dataset" folder 
      - with_commands for with or without natural language commands (hard coded - change in this file)
      - see list of modes from tfix_mode enum (hard coded - change in this file)
      """)

    # mode = tfix_mode.random_assertion_by_category_n_shot_top_n
    mode = tfix_mode.random_assertion_by_category_n_shot_util_8000_tokens
    if len(sys.argv) >= 2:
        print(f"running script with options: {sys.argv}")

        training_set_folder_path = sys.argv[1]
        test_set_folder_path = sys.argv[2]
        with_commands = str2bool(sys.argv[3])
        mode = sys.argv[4]
        prompt_type = sys.argv[5]

        if mode == "zero_shot":
            mode = tfix_mode.zero_shot
        elif mode == "random_1_shot":
            mode = tfix_mode.random_1_shot
        elif mode == "random_n_shot":
            mode = tfix_mode.random_n_shot
        elif mode == "random_assertion_by_category_n_shot":
            mode = tfix_mode.random_assertion_by_category_n_shot
        elif mode == "random_assertion_by_category_n_shot_util_8000_tokens":
            mode = tfix_mode.random_assertion_by_category_n_shot_util_8000_tokens
        elif mode == "random_assertion_by_category_n_shot_top_n":
            mode = tfix_mode.random_assertion_by_category_n_shot_top_n
        else:
            raise Exception("Invalid mode")

        if prompt_type == "warning_line_only":
            prompt_type = tfix_template_type.warning_line_only
        elif prompt_type == "explicit_warning_delineation":
            prompt_type = tfix_template_type.explicit_warning_delineation

    prompt_type = None

    # hard coding path - clean test
    training_set_folder_path = "dataset/tfix-dataset/clean-test/train_data.json"
    test_set_folder_path = "dataset/tfix-dataset/clean-test/test_data.json"

    # hard coding path - random test
    # training_set_folder_path = "dataset/tfix-dataset/clean-test/train_data.json"
    # test_set_folder_path = "dataset/tfix-dataset/random-test/data_autofix_tracking_repo_specific_filtered.json"
    # test_set_folder_path = "dataset/tfix-dataset/random-test/data_autofix_tracking_eslint_filtered.json"

    # mode = tfix_mode.semantic_search_st_n_shot
    # mode = tfix_mode.zero_shot
    # mode = tfix_mode.random_1_shot
    # mode = tfix_mode.random_52_shot
    # mode = tfix_mode.random_52_shot_1_example_per_category
    # mode = tfix_mode.bm_25
    # mode = tfix_mode.random_n_shot_until_context_window
    main(training_set_folder_path, test_set_folder_path, with_commands, mode, prompt_type)
