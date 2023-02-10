import hashlib
import os
import sys

import models
from models import tfix_mode
from demonstration.tfix_demonstrations import TFixDemonstration, MAX_TFIX_COMPLETION_LENGTH_TRAIN
from prompts.tfix_shot_examples import random_1_shot, random_n_shot, random_select_by_category_n_shot, \
    random_n_shot_choose_per_category, random_n_shot_until_context_window
from prompts.tfix_shot_examples.random_n_shot import tfix_datapoint_with_demo_length
from template import tfix_templates
from template.tfix_template_options import tfix_template_type
from template.tfix_templates_explicit_warning_delineation import get_tfix_query_template_explicit_warning_delineation
from util import utils
from template.tfix_templates import get_tfix_demo_template

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from prompt import Prompt


class TFixPrompt(Prompt):
    def __init__(self,
                 demonstrations: list[models.tfix_datapoint],
                 query: str,
                 inference: models.tfix_datapoint,
                 with_commands: bool = True):
        self.demonstration_records = demonstrations
        self.query = query
        self.with_commands = with_commands
        self.inference = inference

    def construct_prompt(self):
        tfix_demonstration = TFixDemonstration(self.with_commands)
        demonstrations = tfix_demonstration.construct(self.demonstration_records)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt

    def construct_prompt_more_example_of_a_given_violation(self):
        tfix_demonstration = TFixDemonstration(self.with_commands)
        demonstrations = tfix_demonstration.construct_more_example_of_a_given_violation(self.demonstration_records,
                                                                                        self.inference.linter_report_rule_id)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt

    def construct_prompt_more_example_of_a_given_violation_until_8000_tokens(self, template_type: tfix_template_type):
        tfix_demonstration = TFixDemonstration(self.with_commands)
        demonstrations = tfix_demonstration.construct_more_example_of_a_given_violation_until_8000_tokens(
            self.demonstration_records,
            self.query,
            self.inference.linter_report_rule_id,
            template_type)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt

    def construct_prompt_semantic_search(self, dp: models.tfix_datapoint, template_type: tfix_template_type,
                                         semantic_search_type: tfix_mode):
        tfix_demonstration = TFixDemonstration(self.with_commands)
        demonstrations = tfix_demonstration.construct_semantic_search(
            dp,
            self.demonstration_records,
            self.query,
            self.inference.linter_report_rule_id,
            template_type,
            semantic_search_type)

        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt


def build_tfix_repair_prompt(demonstrations: list[models.tfix_datapoint],
                             inference: models.tfix_datapoint,
                             with_commands: bool = True,
                             template_type: tfix_template_type = tfix_template_type.warning_line_only) -> TFixPrompt:
    query = tfix_query(inference, template_type, with_commands)

    tfix_prompt = TFixPrompt(demonstrations, query, inference, with_commands)
    return tfix_prompt


def tfix_query(inference: models.tfix_datapoint,
               template_type: tfix_template_type,
               with_commands: bool = True) -> str:
    if template_type is tfix_template_type.explicit_warning_delineation:
        query = get_tfix_query_template_explicit_warning_delineation(inference, with_commands)
    else:
        query = tfix_templates.get_tfix_query_template(inference, with_commands)
    return query


def build_tfix_repair_prompt_with_mode(training_data: list[models.tfix_datapoint],
                                       training_data_with_length: list[tfix_datapoint_with_demo_length],
                                       inference: models.tfix_datapoint,
                                       with_commands: bool = True,
                                       mode: tfix_mode = tfix_mode.random_1_shot) -> TFixPrompt:
    query = tfix_query(inference=inference, template_type=None, with_commands=with_commands)

    if mode == tfix_mode.zero_shot:
        demonstrations = []
    elif mode == tfix_mode.random_1_shot:
        demonstrations = random_1_shot.random_1_shot_example(query=query,
                                                             training_data_with_length=training_data_with_length)
    elif mode == tfix_mode.random_52_shot:
        demonstrations = random_n_shot.random_n_shot_example(query=query,
                                                             training_data_with_length=training_data_with_length,
                                                             how_many_examples=52,
                                                             with_commands=with_commands)
    elif mode == tfix_mode.random_n_shot_until_context_window:
        demonstrations = random_n_shot_until_context_window.random_n_shot_until_context_window_example(query=query,
                                                                                                        training_data_with_length=training_data_with_length,
                                                                                                        with_commands=with_commands)
    elif mode == tfix_mode.random_52_shot_1_example_per_category:
        demonstrations = random_n_shot_choose_per_category.random_n_shot_chose_per_category(query=query,
                                                                                            training_data_with_length=training_data_with_length,
                                                                                            how_many_examples=52,
                                                                                            with_commands=with_commands)
    else:
        raise Exception("Invalid mode")

    query = tfix_templates.get_tfix_query_template(inference, with_commands)

    tfix_prompt = TFixPrompt(demonstrations, query, inference.linter_report_rule_id, with_commands)

    return tfix_prompt


def build_tfix_repair_prompt_bm25(training_data: list[models.tfix_datapoint],
                                  training_data_with_length: list[tfix_datapoint_with_demo_length],
                                  bm25,
                                  buggy_code_corpus,
                                  bm_25_cache_dict: dict,
                                  inference: models.tfix_datapoint,
                                  with_commands: bool = True) -> TFixPrompt:
    query = tfix_query(inference=inference, template_type=None, with_commands=with_commands)

    tokenized_query = inference.source_code.split(" ")
    results_top_n = bm25.get_top_n(tokenized_query, buggy_code_corpus, n=10000)

    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_TFIX_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    candidate_demonstrations = []
    length_so_far = 0
    tfix_error_type = inference.linter_report_rule_id
    for r in results_top_n:
        buggy_source_code = " ".join(r)
        md5hash_of_query = hashlib.md5(buggy_source_code.encode('utf-8')).hexdigest()

        if md5hash_of_query in bm_25_cache_dict:
            dp = bm_25_cache_dict[md5hash_of_query]

            if dp.linter_report_rule_id != tfix_error_type:
                continue

            candidate_demo_token_count = utils.count_codex_tokens(get_tfix_demo_template(dp, with_commands))
            if (length_so_far + candidate_demo_token_count) <= max_demo_length:
                candidate_demonstrations.append(dp)
                length_so_far += candidate_demo_token_count
            else:
                break
        else:
            raise Exception("why key missing in the dict?")

    demonstrations = candidate_demonstrations
    tfix_prompt = TFixPrompt(demonstrations, query, inference.linter_report_rule_id, with_commands)

    return tfix_prompt
