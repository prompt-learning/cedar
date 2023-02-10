from typing import List

import models
from dataset.dataset import Dataset


def extract_substring_between_markers(string: str,
                                      start_marker: str,
                                      end_marker: str) -> str:
    start_index = string.find(start_marker)
    end_index = string.find(end_marker)
    return string[start_index + len(start_marker):end_index]

class SequencerDataset(Dataset):
    def __init__(self, dataset_path):
        self.before_path = dataset_path[0]
        self.after_path = dataset_path[1]

        with open(self.before_path) as before_file, open(self.after_path) as after_file:
            self.before_file_content_orig = before_file.read()
            self.after_file_content_orig = after_file.read()

    def parse(self) -> List[models.sequencer_datapoint]:
        raw_records = []
        before_file_content = self.before_file_content_orig.splitlines()
        after_file_content = self.after_file_content_orig.splitlines()

        if len(before_file_content) != len(after_file_content):
            raise Exception(f"before and after file content are not the same length.\n"
                            f"before: {len(before_file_content)}, after: {len(after_file_content)}.\n"
                            f"before_file_name:{self.before_path}, after_file_name:{self.after_path}")

        pairs = zip(before_file_content, after_file_content)

        for dp in pairs:
            source_code_with_method_context = dp[0]
            target_statement = dp[1]

            buggy_method_context = source_code_with_method_context
            buggy_code = extract_substring_between_markers(string = buggy_method_context,
                                                           start_marker = "<START_BUG>",
                                                           end_marker = "<END_BUG>")
            correct_code = target_statement


            buggy_method_context = buggy_method_context.replace("<seq2seq4repair_space>", " ")
            buggy_code = buggy_code.replace("<seq2seq4repair_space>", " ")
            correct_code = correct_code.replace("<seq2seq4repair_space>", " ")
            dp = models.sequencer_datapoint(buggy_method_context=buggy_method_context,
                                            buggy_code=buggy_code,
                                            correct_code=correct_code,
                                            complexity="N/A")

            raw_records.append(dp)
        return raw_records
