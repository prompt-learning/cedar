import models
import random

from demonstration.tfix_demonstrations import MAX_TFIX_COMPLETION_LENGTH_TRAIN
from prompts.tfix_shot_examples.random_n_shot import tfix_datapoint_with_demo_length
from util import utils


def random_1_shot_example(query: str,
                          training_data_with_length: list[tfix_datapoint_with_demo_length]) -> models.tfix_datapoint:

    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_TFIX_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    random_sample: tfix_datapoint_with_demo_length = random.choice(training_data_with_length)
    if random_sample.token_count <= max_demo_length:
        return [random_sample.datapoint]
    else:
        print("WARNING: demo length exceeded. Selecting random example with the max_demo_length.")
        filtered_samples = [x for x in training_data_with_length
                            if x.token_count <= max_demo_length]
        if len(filtered_samples) == 0:
            return []
        return [random.choice(filtered_samples).datapoint]
