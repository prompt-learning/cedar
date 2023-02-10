import os
import sys
from enum import Enum

import models
from demonstration.tufano_demonstrations import TufanoDemonstration
from template import tufano_templates
from template.tufano_template_options import tufano_template_type

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from prompt import Prompt


tufano_mode = Enum('tufano_mode',
                 'zero_shot '
                 'random_1_shot '
                 'random_n_shot '                 
                 'random_n_shot_util_8000_tokens')


class TufanoPrompt(Prompt):
    def __init__(self, demonstrations: list[models.tufano_datapoint],
                 query: str,
                 inference: models.tufano_datapoint,
                 with_commands: bool = True):
        self.demonstration_records = demonstrations
        self.query = query
        self.with_commands = with_commands
        self.inference = inference

    def construct_prompt(self):
        tufano_demonstration = TufanoDemonstration(self.with_commands)
        demonstrations = tufano_demonstration.construct(self.demonstration_records)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt

    def construct_prompt_more_example_of_a_given_violation(self):
        tufano_demonstration = TufanoDemonstration(self.with_commands)
        demonstrations = tufano_demonstration.construct_more_example_of_a_given_violation(self.demonstration_records)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt

    def construct_prompt_more_example_of_a_given_violation_until_8000_tokens(self, template_type: tufano_template_type):
        tufano_demonstration = TufanoDemonstration(self.with_commands)
        demonstrations = tufano_demonstration.construct_more_example_of_a_given_violation_until_8000_tokens(
            self.demonstration_records,
            self.query,
            template_type)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt


def build_tufano_repair_prompt(demonstrations: list[models.tufano_datapoint],
                             inference: models.tufano_datapoint,
                             with_commands: bool = True, template_type: tufano_template_type = tufano_template_type.denineation) -> TufanoPrompt:
    query = tufano_templates.get_tufano_query_template(inference, with_commands)

    tufano_prompt = TufanoPrompt(demonstrations, query, inference, with_commands)
    return tufano_prompt


def build_tufano_repair_prompt_with_mode(inference: models.tufano_datapoint,
                                       with_commands: bool = True,
                                       mode: tufano_mode = tufano_mode.random_1_shot) -> TufanoPrompt:
    if mode == tufano_mode.zero_shot:
        demonstrations = []
    elif mode == tufano_mode.random_1_shot:
        demonstration = random_1_shot.random_1_shot_example()
        demonstrations = [demonstration]
    elif mode == tufano_mode.random_n_shot:
        demonstrations = random_n_shot.random_n_shot_example()
    elif mode == tufano_mode.random_assertion_by_category_n_shot:
        demonstrations = random_select_by_category_n_shot.random_select_by_category_n_shot_example()
    elif mode == tufano_mode.random_assertion_by_category_n_shot_top_n:
        demonstrations = random_select_by_category_n_shot.random_select_by_category_n_shot_example()
    else:
        raise Exception("Invalid mode")

    query = tufano_templates.get_tufano_query_template(inference, with_commands)
    if mode == tufano_mode.zero_shot:
        query = tufano_templates.get_tufano_query_template(inference, with_commands)

    tufano_prompt = TufanoPrompt(demonstrations, query, inference.linter_report_rule_id, with_commands)

    return tufano_prompt
