import os
import sys
from enum import Enum

import models
from template import sequencer_templates
from demonstration.sequencer_demonstrations import SequencerDemonstration
from template.sequencer_template_options import sequencer_template_type

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from prompt import Prompt

sequencer_mode = Enum('sequencer_mode',
                      'zero_shot '
                      'random_1_shot '
                      'random_n_shot '
                      'random_n_shot_util_8000_tokens '
                      'random_by_category_n_shot_top_n '
                      'semantic_search')


class SequencerPrompt(Prompt):
    def __init__(self, demonstrations: list[models.sequencer_datapoint],
                 query: str,
                 inference: models.sequencer_datapoint,
                 with_commands: bool = True):
        self.demonstration_records = demonstrations
        self.query = query
        self.with_commands = with_commands
        self.inference = inference

    def construct_prompt(self):
        sequencer_demonstration = SequencerDemonstration(self.with_commands)
        demonstrations = sequencer_demonstration.construct(self.demonstration_records)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt

    def construct_prompt_more_example_of_a_given_violation(self):
        sequencer_demonstration: SequencerDemonstration = SequencerDemonstration(self.with_commands)
        demonstrations = sequencer_demonstration.construct_more_example_of_a_given_violation(self.demonstration_records)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt

    def construct_prompt_more_example_of_a_given_violation_until_8000_tokens(self,
                                                                             template_type: sequencer_template_type):
        sequencer_demonstration = SequencerDemonstration(self.with_commands)
        demonstrations = sequencer_demonstration.construct_more_example_of_a_given_violation_until_8000_tokens(
            self.demonstration_records,
            self.query,
            template_type)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt

    def construct_prompt_semantic_search(self, dp: models.sequencer_datapoint, template_type: sequencer_template_type):
        sequencer_demonstration = SequencerDemonstration(self.with_commands)
        demonstrations = sequencer_demonstration.construct_semantic_search(dp,
                                                                           self.demonstration_records,
                                                                           self.query,
                                                                           template_type)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt


def build_sequencer_repair_prompt(demonstrations: list[models.sequencer_datapoint],
                                  inference: models.sequencer_datapoint,
                                  with_commands: bool = True,
                                  template_type: sequencer_template_type = sequencer_template_type.warning_line_only) -> SequencerPrompt:
    if template_type is sequencer_template_type.explicit_warning_delineation:
        query = get_sequencer_query_template_explicit_warning_delineation(inference, with_commands)
    else:
        query = sequencer_templates.get_sequencer_query_template(inference, with_commands)

    sequencer_prompt = SequencerPrompt(demonstrations, query, inference, with_commands)
    return sequencer_prompt


def build_sequencer_repair_prompt_with_mode(inference: models.sequencer_datapoint,
                                            with_commands: bool = True,
                                            mode: sequencer_mode = sequencer_mode.random_1_shot) -> SequencerPrompt:
    if mode == sequencer_mode.zero_shot:
        demonstrations = []
    elif mode == sequencer_mode.random_1_shot:
        demonstration = random_1_shot.random_1_shot_example()
        demonstrations = [demonstration]
    elif mode == sequencer_mode.random_n_shot:
        demonstrations = random_n_shot.random_n_shot_example()
    elif mode == sequencer_mode.random_assertion_by_category_n_shot:
        demonstrations = random_select_by_category_n_shot.random_select_by_category_n_shot_example()
    elif mode == sequencer_mode.random_assertion_by_category_n_shot_top_n:
        demonstrations = random_select_by_category_n_shot.random_select_by_category_n_shot_example()
    else:
        raise Exception("Invalid mode")

    query = sequencer_templates.get_sequencer_query_template(inference, with_commands)
    if mode == sequencer_mode.zero_shot:
        query = sequencer_templates.get_sequencer_query_template(inference, with_commands)

    sequencer_prompt = SequencerPrompt(demonstrations, query, inference.linter_report_rule_id, with_commands)

    return sequencer_prompt
