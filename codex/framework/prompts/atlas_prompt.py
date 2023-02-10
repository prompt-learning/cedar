import os
import sys
import time
from typing import List

import models

from models import atlas_mode
from prompts.atlas_shot_examples import random_n_shot, random_n_shot_until_context_window
from prompts.atlas_shot_examples import random_select_by_category_n_shot
from template import assert_templates
from template.assert_templates import get_atlas_demo_template
from util import utils
import hashlib
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from prompt import Prompt
from demonstration.atlas_demonstrations import AtlasDemonstration
from atlas_shot_examples import random_1_shot


class AtlasPrompt(Prompt):

    def __init__(self, demonstrations, query, with_commands):
        self.demonstration_records = demonstrations
        self.query = query
        self.with_commands = with_commands

    def construct_prompt(self) -> str:
        atlas_demonstration = AtlasDemonstration(self.with_commands)
        demonstrations = atlas_demonstration.construct(self.demonstration_records)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt

    def construct_prompt_semantic_search(self, t: models.atlas_datapoint):
        atlas_demonstration = AtlasDemonstration(self.with_commands)
        demonstrations = atlas_demonstration.construct_semantic_search(t,
                                                                       self.demonstration_records,
                                                                       self.query)
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt


def build_atlas_assertion_prompt(demonstrations: List[models.atlas_datapoint],
                                 inference: models.atlas_datapoint,
                                 with_commands=True) -> AtlasPrompt:
    query = assert_templates.get_atlas_query_template(inference, with_commands)

    assertion_prompt = AtlasPrompt(demonstrations, query, with_commands)
    return assertion_prompt


def build_atlas_assertion_prompt_with_mode(training_data: list[models.atlas_datapoint],
                                           training_data_with_length: list[models.atlas_datapoint_with_demo_length],
                                           inference: models.atlas_datapoint,
                                           with_commands: bool = True,
                                           mode: atlas_mode = atlas_mode.random_1_shot) -> AtlasPrompt:
    query = assert_templates.get_atlas_query_template(inference, with_commands)

    if mode == atlas_mode.zero_shot:
        demonstrations = []
    elif mode == atlas_mode.random_1_shot:
        demonstrations = random_1_shot.random_1_shot_example(query=query,
                                                             training_data_with_length=training_data_with_length)
        #demonstrations = [demonstration]
    elif mode == atlas_mode.random_n_shot:
        #demonstrations = random_n_shot.random_n_shot_example_()
        demonstrations = random_n_shot.random_n_shot_example(query=query,
                                                             training_data=training_data,
                                                             training_data_with_length=training_data_with_length,
                                                             with_commands=with_commands,
                                                             n=8)
    elif mode == atlas_mode.random_n_shot_until_context_window:
        demonstrations = random_n_shot_until_context_window.random_n_shot_until_context_window_example(query=query,
                                                                                                       training_data=training_data,
                                                                                                       training_data_with_length=training_data_with_length,
                                                                                                       with_commands=with_commands,
                                                                                                       n=20)
    elif mode == atlas_mode.random_assertion_by_category_n_shot:
        # demonstrations = random_select_by_category_n_shot.random_select_by_category_n_shot_example()
        demonstrations = random_select_by_category_n_shot.random_select_by_category_n_shot_example(query=query,
                                                                                                   training_data=training_data,
                                                                                                   training_data_with_length=training_data_with_length,
                                                                                                   with_commands=with_commands)
    else:
        raise Exception("Invalid mode")

    query = assert_templates.get_atlas_query_template(inference, with_commands)
    if mode == atlas_mode.zero_shot:
        query = assert_templates.get_atlas_query_template_with_detailed_nl_desc(inference, with_commands)

    assertion_prompt = AtlasPrompt(demonstrations, query, with_commands)

    return assertion_prompt


MAX_ATLAS_COMPLETION_LENGTH_TRAIN = 500
def build_atlas_assertion_prompt_bm25(training_data:list[models.atlas_datapoint],
                                  bm25,
                                  test_methods,
                                  bm_25_cache_dict: dict,
                                  inference: models.atlas_datapoint,
                                  with_commands:bool = True) -> AtlasPrompt:
    query = assert_templates.get_atlas_query_template(data=inference, with_commands=with_commands)

    start_time = time.time()
    tokenized_query = inference.test_method.split(" ")
    results_top_n = bm25.get_top_n(tokenized_query, test_methods, n=80)
    end_time = time.time()
    print(f"duration to query bm25: {(end_time - start_time)}")

    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_ATLAS_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    candidate_demonstrations = []
    length_so_far = 0

    for r in results_top_n:
        md5hash_of_query = hashlib.md5(r.encode('utf-8')).hexdigest()

        if md5hash_of_query in bm_25_cache_dict:
            dp = bm_25_cache_dict[md5hash_of_query]

            candidate_demo_token_count = dp.token_count
            if (length_so_far + candidate_demo_token_count) <= max_demo_length:
                candidate_demonstrations.append(dp.datapoint)
                length_so_far += candidate_demo_token_count
            else:
                break
        else:
            raise Exception("why key missing in the dict?")

    print("number of candidate demonstrations: ", len(candidate_demonstrations))
    demonstrations = candidate_demonstrations
    assertion_prompt = AtlasPrompt(demonstrations, query, with_commands)

    return assertion_prompt


