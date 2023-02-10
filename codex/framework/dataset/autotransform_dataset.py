import models

from typing import List
import json

from dataset.dataset import Dataset


class AutoTransformDataset(Dataset):
    def __init__(self, dataset_path):
        self.before_path = dataset_path[0]
        self.after_path = dataset_path[1]

        with open(self.before_path) as before_file, open(self.after_path) as after_file:
            self.before_file_content_orig = before_file.read()
            self.after_file_content_orig = after_file.read()

    def parse(self) -> List[models.tufano_datapoint]:
        raw_records = []
        before_file_content = self.before_file_content_orig.splitlines()
        after_file_content = self.after_file_content_orig.splitlines()

        if len(before_file_content) != len(after_file_content):
            raise Exception(f"before and after file content are not the same length.\n"
                            f"before: {len(before_file_content)}, after: {len(after_file_content)}.\n"
                            f"before_file_name:{self.before_path}, after_file_name:{self.after_path}")

        pairs = zip(before_file_content, after_file_content)

        for dp in pairs:
            abstracted_source_code = "N/A"
            abstracted_target_code = "N/A"

            source_code = dp[0]
            target_code = dp[1]

            dp = models.tufano_datapoint(source_code_abstracted=abstracted_source_code,
                                         target_code_abstracted=abstracted_target_code,
                                         source_code=source_code,
                                         target_code=target_code)

            raw_records.append(dp)
        return raw_records
