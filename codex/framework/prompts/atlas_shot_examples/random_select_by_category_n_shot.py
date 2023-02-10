import models
import random
from util import utils
from models import atlas_datapoint
from demonstration.atlas_demonstrations import MAX_ATLAS_COMPLETION_LENGTH_TRAIN

def random_select_by_category_n_shot_example(query: str,
                                             training_data: list[models.atlas_datapoint],
                                             training_data_with_length: list[models.atlas_datapoint_with_demo_length],
                                             with_commands: bool) -> list[models.atlas_datapoint]:
    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_ATLAS_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    datapoints_by_atlas_assertion_type = {}

    for r in training_data_with_length:
        dp = r.datapoint
        if dp.assertion_type in datapoints_by_atlas_assertion_type:
            datapoints_by_atlas_assertion_type[dp.assertion_type].append(r)
        else:
            datapoints_by_atlas_assertion_type[dp.assertion_type] = [r]

    how_many_assertion_categories = len(datapoints_by_atlas_assertion_type.keys())
    print(f"how_many_assertion_categories: {how_many_assertion_categories}")

    random_samples = []
    random_samples_length = 0
    for _, datapoints in datapoints_by_atlas_assertion_type.items():
        random_choice = random.choice(datapoints)
        random_samples.append(random_choice)
        random_samples_length += random_choice.token_count

    results = []
    if random_samples_length <= max_demo_length:
        results = random_samples
    else:
        print("Check: this should not happen. random_samples_length > max_demo_length")
        random_samples = []
        random_samples_length = 0
        avg_length_per_example = max_demo_length / len(datapoints_by_atlas_assertion_type)
        for _, datapoints in datapoints_by_atlas_assertion_type.items():
            filtered_samples = [x for x in datapoints
                                if x.token_token_count <= avg_length_per_example]

            if len(filtered_samples) == 0:
                datapoints_sorted = sorted(datapoints, key = lambda x: x.token_count)
                choice = datapoints_sorted[0]
                random_samples.append(choice)
                random_samples_length += choice.token_count
            else:
                random_choice = random.choice(filtered_samples)
                random_samples.append(random_choice)
                random_samples_length += random_choice.token_count
        results = random_samples

    length_so_far = 0
    for r in results:
        length_so_far += r.token_count
        if length_so_far > max_demo_length:
            raise Exception("Demo length exceeded")

    results = [x.datapoint for x in results]
    return results