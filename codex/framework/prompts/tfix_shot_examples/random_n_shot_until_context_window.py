import random

import models
from demonstration.tfix_demonstrations import MAX_TFIX_COMPLETION_LENGTH_TRAIN
from prompts.tfix_shot_examples.random_n_shot import tfix_datapoint_with_demo_length
from util import utils


def random_n_shot_until_context_window_example(query: str,
                                               training_data_with_length: list[tfix_datapoint_with_demo_length],
                                               with_commands: bool) -> list[models.tfix_datapoint]:
    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_TFIX_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    random_samples: list[tfix_datapoint_with_demo_length] = random.sample(training_data_with_length, 1000)
    random_samples_length = 0

    results = []
    for sample in random_samples:
        random_samples_length += sample.token_count
        if random_samples_length > max_demo_length:
            break
        else:
            results.append(sample)

    length_so_far = 0
    for r in results:
        length_so_far += r.token_count
        if length_so_far > max_demo_length:
            raise Exception("Demo length exceeded")

    results = [x.datapoint for x in results]
    return results
