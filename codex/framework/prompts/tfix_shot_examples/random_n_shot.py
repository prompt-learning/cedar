import random
from typing import List

import models
from demonstration.tfix_demonstrations import MAX_TFIX_COMPLETION_LENGTH_TRAIN
from util import utils


class tfix_datapoint_with_demo_length:
    def __init__(self, datapoint: models.tfix_datapoint, token_count: int):
        self.datapoint = datapoint
        self.token_count = token_count

def random_n_shot_example(query: str,
                          training_data_with_length: list[tfix_datapoint_with_demo_length],
                          how_many_examples: int,
                          with_commands: bool) -> list[models.tfix_datapoint]:
    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_TFIX_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    random_samples: list[tfix_datapoint_with_demo_length] = random.sample(training_data_with_length, how_many_examples)
    random_samples_length = 0
    for sample in random_samples:
        random_samples_length += sample.token_count

    results = []
    if random_samples_length <= max_demo_length:
        results = random_samples
    else:
        random_examples: list[tfix_datapoint_with_demo_length] = random.sample(training_data_with_length, 20000)
        avg_length_per_example = max_demo_length / how_many_examples

        filtered_samples = [x for x in random_examples
                            if x.token_count <= avg_length_per_example]

        results = filtered_samples[:52]

    length_so_far = 0
    for r in results:
        length_so_far += r.token_count
        if length_so_far > max_demo_length:
            raise Exception("Demo length exceeded")

    results = [x.datapoint for x in results]
    return results
