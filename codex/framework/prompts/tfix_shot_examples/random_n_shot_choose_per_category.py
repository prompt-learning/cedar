import models
import random

from demonstration.tfix_demonstrations import MAX_TFIX_COMPLETION_LENGTH_TRAIN
from models import tfix_datapoint
from prompts.tfix_shot_examples.random_n_shot import tfix_datapoint_with_demo_length
from util import utils


def random_n_shot_chose_per_category(query: str,
                                     training_data_with_length: list[tfix_datapoint_with_demo_length],
                                     how_many_examples: int,
                                     with_commands: bool) -> list[models.tfix_datapoint]:

    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_TFIX_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    datapoints_by_tfix_error_type = {}

    for r in training_data_with_length:
        dp = r.datapoint
        if dp.linter_report_rule_id in datapoints_by_tfix_error_type:
            datapoints_by_tfix_error_type[dp.linter_report_rule_id].append(r)
        else:
            datapoints_by_tfix_error_type[dp.linter_report_rule_id] = [r]

    how_many_error_categories = len(datapoints_by_tfix_error_type.keys())
    print(f"tfix number of error categories: {how_many_error_categories}")

    random_samples = []
    random_samples_length = 0
    for _, datapoints in datapoints_by_tfix_error_type.items():
        random_choice = random.choice(datapoints)
        random_samples.append(random_choice)
        random_samples_length += random_choice.token_count

    results = []
    if random_samples_length <= max_demo_length:
        results = random_samples
    else:
        random_samples = []
        random_samples_length = 0
        avg_length_per_example = max_demo_length / how_many_examples
        for _, datapoints in datapoints_by_tfix_error_type.items():
            filtered_samples = [x for x in datapoints
                                if x.token_count <= avg_length_per_example]

            if len(filtered_samples) == 0:
                # datapoints_sorted = datapoints.sort(key=lambda x: x.token_count)
                datapoints_sorted = sorted(datapoints, key=lambda x: x.token_count)
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
