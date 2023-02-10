import models
from models import atlas_datapoint
from util import utils
import random
from demonstration.atlas_demonstrations import MAX_ATLAS_COMPLETION_LENGTH_TRAIN

def random_n_shot_example(query: str,
                          training_data: list[atlas_datapoint],
                          training_data_with_length: list[models.atlas_datapoint_with_demo_length],
                          with_commands:bool,
                          n=8) -> list[models.atlas_datapoint]:
    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_ATLAS_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    random_samples: list[models.atlas_datapoint_with_demo_length] = random.sample(training_data_with_length, n)

    results = []
    random_samples_length = 0
    for sample in random_samples:
        random_samples_length += sample.token_count
        if random_samples_length > max_demo_length:
            break
        else:
            results.append(sample.datapoint)

    if len(results) != n:
        average_dmeo_length = max_demo_length / n
        random_samples:list[models.atlas_datapoint_with_demo_length] = random.sample(training_data_with_length, 5000)

        chose_samples_that_fits_within_context_window = []
        for sample in random_samples:
            if sample.token_count <= average_dmeo_length:
                chose_samples_that_fits_within_context_window.append(sample)
                if len(chose_samples_that_fits_within_context_window) == n:
                    break

        if len(chose_samples_that_fits_within_context_window) < n:
            raise Exception("Could not find enough samples that fits within the context window")
        results = chose_samples_that_fits_within_context_window

    length_so_far = 0
    for r in results:
        length_so_far += r.token_count
        if length_so_far > max_demo_length:
            raise Exception("Demo length exceeded")

    results = [r.datapoint for r in results]
    print(f"number of demonstrations: {len(results)}")
    return results