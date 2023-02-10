import models

from typing import List
import json

from dataset.dataset import Dataset


class TufanoDataset(Dataset):
    def __init__(self, path):
        self.path = path
        with open(self.path) as file:
            self.dataset = file.read()

    def parse(self) -> List[models.tufano_datapoint]:
        raw_records = []
        dataset = self.dataset.split("====")

        for dp in dataset:
            if dp.split("----").__len__() == 4:
                code_segments = dp.split("----")

                abstracted_code = code_segments[0].split("\n")
                abstracted_source_code = abstracted_code[1]
                abstracted_target_code = abstracted_code[2]

                source_code = code_segments[1]
                target_code = code_segments[2]

                dp = models.tufano_datapoint(source_code_abstracted=abstracted_source_code,
                                             target_code_abstracted=abstracted_target_code,
                                             source_code=source_code,
                                             target_code=target_code)

                raw_records.append(dp)
        return raw_records
