import csv
from typing import List

import models
from codex_api.codex_api import CodexAPI
from codex_api.codex_api_top_n import CodexAPITopN
from codex_api.codex_api_zero_shot import CodexAPIZeroShot
from evaluation.evaluation_tfix import Evaluation
from main_tfix import invoke_top_n
from prompts.tfix_prompt import TFixPrompt, tfix_mode
from util import utils


def prompt_codex_top_n(testdata: list[models.tfix_datapoint],
                       tfix_prompts: list[TFixPrompt],
                       shot_mode: tfix_mode,
                       dry_run: bool = False, ) -> None:
    results_detailed: List[str] = []
    results_without_prompt: List[str] = []

    if shot_mode is tfix_mode.zero_shot:
        codex_api = CodexAPIZeroShot()
    elif shot_mode is tfix_mode.random_assertion_by_category_n_shot_top_n:
        codex_api = CodexAPITopN()
    else:
        codex_api = CodexAPI()

    seq = 0
    exact_match_so_far = 0
    for prompt in tfix_prompts:
        if not dry_run:
            print(f"process record {seq}")
            expected_response = testdata[seq].target_code

            (inference_time, responses_codex, response_completion_tokens, response_prompt_tokens,
             response_total_tokens) = invoke_top_n(codex_api, prompt)
            print(responses_codex)

            top_1_result = Evaluation(responses_codex[0], expected_response).calculate()
            top_2_result = Evaluation(responses_codex[1], expected_response).calculate()
            top_3_result = Evaluation(responses_codex[2], expected_response).calculate()
            top_4_result = Evaluation(responses_codex[3], expected_response).calculate()
            top_5_result = Evaluation(responses_codex[4], expected_response).calculate()

            print(top_1_result)
            is_match = top_1_result["is_match"] is True or \
                       top_2_result["is_match"] is True or \
                       top_3_result["is_match"] is True or \
                       top_4_result["is_match"] is True or \
                       top_5_result["is_match"] is True

            is_exact_match = top_1_result["is_exact_match"] is True or \
                             top_2_result["is_exact_match"] is True or \
                             top_3_result["is_exact_match"] is True or \
                             top_4_result["is_exact_match"] is True or \
                             top_5_result["is_exact_match"] is True

            results_detailed.append(models.tfix_result_top_n(prompt=prompt,
                                                             expected=expected_response,
                                                             codex_1=responses_codex[0],
                                                             codex_2=responses_codex[1],
                                                             codex_3=responses_codex[2],
                                                             codex_4=responses_codex[3],
                                                             codex_5=responses_codex[4],
                                                             is_exact_match=is_exact_match,
                                                             is_match=is_match,
                                                             lcs=top_1_result["calc_lcs"],
                                                             edit_distance=top_1_result["edit_distance"],
                                                             inference_time=inference_time,
                                                             gpt_token_count=utils.count_codex_tokens(prompt),
                                                             word_count=utils.word_count(prompt),
                                                             response_completion_tokens=response_completion_tokens,
                                                             response_prompt_tokens=response_prompt_tokens,
                                                             response_total_tokens=response_total_tokens
                                                             ))

            results_without_prompt.append(models.tfix_result_top_n(prompt=testdata[seq].source_code,
                                                                   expected=expected_response,
                                                                   codex_1=responses_codex[0],
                                                                   codex_2=responses_codex[1],
                                                                   codex_3=responses_codex[2],
                                                                   codex_4=responses_codex[3],
                                                                   codex_5=responses_codex[4],
                                                                   is_exact_match=is_exact_match,
                                                                   is_match=is_match,
                                                                   lcs=top_1_result["calc_lcs"],
                                                                   edit_distance=top_1_result["edit_distance"],
                                                                   inference_time=inference_time,
                                                                   gpt_token_count=utils.count_codex_tokens(prompt),
                                                                   word_count=utils.word_count(prompt),
                                                                   response_completion_tokens=response_completion_tokens,
                                                                   response_prompt_tokens=response_prompt_tokens,
                                                                   response_total_tokens=response_total_tokens
                                                                   ))

            if is_exact_match:
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
                    ['prompt', 'expected',
                     'codex_1', 'codex_2', 'codex_3', 'codex_4', 'codex_5',
                     'is_exact_match', 'is_match', 'lcs', 'edit_distance',
                     'inference_time (secs)',
                     'gpt_token_count', 'word_count',
                     'response_completion_tokens', 'response_prompt_tokens', 'response_total_tokens'])
            writer.writerows(results_detailed)
        print(f"output: csv file: {output_file_name}")

        output_file_name = "./results-without_prompt.csv"
        with open(output_file_name, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                    ['prompt', 'expected',
                     'codex_1', 'codex_2', 'codex_3', 'codex_4', 'codex_5',
                     'is_exact_match', 'is_match', 'lcs', 'edit_distance',
                     'inference_time (secs)',
                     'gpt_token_count', 'word_count',
                     'response_completion_tokens', 'response_prompt_tokens', 'response_total_tokens'])
            writer.writerows(results_without_prompt)
        print(f"output: csv file: {output_file_name}")
