import csv
import sys
import models
from template import assert_templates
from template.assert_templates import get_atlas_demo_template
from util import utils
from typing import List
from prompts.atlas_prompt import AtlasPrompt, build_atlas_assertion_prompt
from dataset.atlas_dataset import AtlasDataset


def save_training_data_stats_to_csv(training_data, with_commands):
    """
    save training dataset stats in the csv file
    """
    print("generate stats for the atlas training dataset")
    stats: List[str] = []
    for t in training_data:
        demo = assert_templates.get_atlas_demo_template(t, with_commands)

        sys.stdout.write('.')
        sys.stdout.flush()
        stats.append(models.atlas_stat(query=demo,
                                       assertion_type=t.assertion_type,
                                       gpt_token_count_focal_method=utils.count_codex_tokens(t.focal_method),
                                       gpt_token_count_test_method=utils.count_codex_tokens(t.test_method),
                                       gpt_token_count_assertion_completion=utils.count_codex_tokens(t.assertion),
                                       gpt_token_count_demo=utils.count_codex_tokens(demo),
                                       word_count_demo=utils.word_count(demo)))
    output_file_name = "./atlas-training-dataset-stats.csv"

    with open(output_file_name, 'w') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['demo', 'assertion_type', 'number_of_codex_tokens', 'word_count'])
        writer.writerows(stats)


def save_inference_stats_to_csv(assertion_prompts, test_data, training_data, with_commands):
    """
    save inference dataset stats in the csv file
    """
    print("generate stats for the atlas test dataset")
    stats: List[str] = []
    for t in test_data:
        ap: AtlasPrompt = build_atlas_assertion_prompt(training_data, t, with_commands)
        assertion_prompt: str = ap.construct_prompt()
        assertion_prompts.append(assertion_prompt)

        sys.stdout.write('.')
        sys.stdout.flush()
        stats.append(models.atlas_stat(query=ap.query,
                                       assertion_type=t.assertion_type,
                                       gpt_token_count_focal_method=utils.count_codex_tokens(t.focal_method),
                                       gpt_token_count_test_method=utils.count_codex_tokens(t.test_method),
                                       gpt_token_count_assertion_completion=utils.count_codex_tokens(t.assertion),
                                       gpt_token_count_demo=utils.count_codex_tokens(ap.query),
                                       word_count_demo=utils.word_count(ap.query)))

    output_file_name = "./atlas-inference-dataset-stats.csv"

    with open(output_file_name, 'w') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['query', 'assertion_type', 'number_of_codex_tokens', 'word_count'])
        writer.writerows(stats)


def assertion_completion_length_stats(training_data: list[models.atlas_datapoint],
                                      test_data: list[models.atlas_datapoint]):
    assertion_codex_token_length_train = 0
    train_lengths = []
    for t in training_data:
        train_lengths.append(utils.count_codex_tokens(t.assertion))
        assertion_codex_token_length_train += utils.count_codex_tokens(t.assertion)
    print("average assertion completion length (train):" + str(assertion_codex_token_length_train / len(training_data)))
    print("max assertion completion length (train):" + str(max(train_lengths)))

    assertion_codex_token_length_test = 0
    test_lengths = []
    for t in test_data:
        test_lengths.append(utils.count_codex_tokens(t.assertion))
        assertion_codex_token_length_test += utils.count_codex_tokens(t.assertion)
    print("average assertion completion length (test):" + str(assertion_codex_token_length_test / len(test_data)))
    print("max assertion completion length (test):" + str(max(test_lengths)))


def demo_length_stats(training_data: list[models.atlas_datapoint],
                      test_data: list[models.atlas_datapoint]):
    demo_length_so_far = 0
    min_demo_length = -1
    max_demo_length = 0
    for t in training_data:
        length = utils.count_codex_tokens(get_atlas_demo_template(t, True))
        demo_length_so_far += length
        if min_demo_length == -1:
            min_demo_length = length
        else:
            min_demo_length = min(min_demo_length, length)
        max_demo_length = max(max_demo_length, length)

    avg_demo_length = demo_length_so_far / len(training_data)
    print("avg demo length (train):" + str(avg_demo_length))
    print("min demo length (train):" + str(min_demo_length))
    print("max demo length (train):" + str(max_demo_length))


    demo_length_so_far = 0
    min_demo_length = -1
    max_demo_length = 0
    for t in test_data:
        length = utils.count_codex_tokens(get_atlas_demo_template(t, True))
        demo_length_so_far += length
        if min_demo_length == -1:
            min_demo_length = length
        else:
            min_demo_length = min(min_demo_length, length)
        max_demo_length = max(max_demo_length, length)

    avg_demo_length = demo_length_so_far / len(training_data)
    print("avg demo length (test_data):" + str(avg_demo_length))
    print("min demo length (test_data):" + str(min_demo_length))
    print("max demo length (test_data):" + str(max_demo_length))



def main(training_set_folder_path: str, test_set_folder_path: str, with_commands: bool):
    assertion_prompts: list[AtlasPrompt] = []

    training_set = AtlasDataset(training_set_folder_path + '/testMethods.txt',
                                training_set_folder_path + '/assertLines.txt')
    test_set = AtlasDataset(test_set_folder_path + '/testMethods.txt',
                            test_set_folder_path + '/assertLines.txt')

    training_data: list[models.atlas_datapoint] = training_set.parse()
    test_data: list[models.atlas_datapoint] = test_set.parse()

    # assertion_completion_length_stats(training_data, test_data)
    demo_length_stats(training_data, test_data)

    # save_training_data_stats_to_csv(training_data, with_commands)

    # save_inference_stats_to_csv(assertion_prompts, test_data, training_data, with_commands)


if __name__ == "__main__":
    print("generate statistics for the atlas dataset")

    # hard coding path
    training_set_folder_path = "dataset/atlas-dataset/Training"
    test_set_folder_path = "dataset/atlas-dataset/Testing"
    main(training_set_folder_path, test_set_folder_path, with_commands=True)
