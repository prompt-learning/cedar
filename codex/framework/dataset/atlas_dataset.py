import os
import sys
import models
import lizard
from typing import List

from dataset.dataset import Dataset
from util.utils import complexity_count

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# from dataset.Dataset import Dataset
# from dataset.Dataset import Dataset

ASSERTION_TYPES = ["assertEquals", "assertTrue", "assertNotNull",
                   "assertThat", "assertNull", "assertFalse",
                   "assertArrayEquals", "assertSame"]


class AtlasDataset(Dataset):
    def __init__(self, source_file, target_file):
        self.source_file_path = source_file
        self.target_file_path = target_file

        with open(self.source_file_path, "r") as file:
            self.source_dataset = file.readlines()

        with open(self.target_file_path, "r") as file:
            self.assertions = file.readlines()

    def get_focal_method_and_test_method(self, line: str) -> (List[str], List[str]):
        tokens = line.split(' ')
        test_method = []
        focal_method = []
        queue = []
        i = 0

        while i < len(tokens):
            if tokens[i] == '{':
                queue.append(tokens[i])
                test_method.append(tokens[i])
                i += 1
                break
            test_method.append(tokens[i])
            i += 1

        while len(queue) and i < len(tokens):
            if tokens[i] == '{':
                queue.append(tokens[i])

            elif tokens[i] == '}' and len(queue):
                queue.pop(0)

            test_method.append(tokens[i])
            i += 1

        while i < len(tokens):
            focal_method.append(tokens[i])
            i += 1

        return focal_method, test_method

    def parse(self) -> List[models.atlas_datapoint]:
        raw_records = []
        for i in range(0, len(self.source_dataset)):
            focal_method, test_method = self.get_focal_method_and_test_method(
                self.source_dataset[i].rstrip('\n'))
            if len(test_method):
                assertion = self.assertions[i].rstrip('\n')
                assertion_type = None
                for a in assertion.split(' '):
                    if a in ASSERTION_TYPES:
                        assertion_type = a
                        break

                context = ' '.join(focal_method) + ' '.join(test_method) if len(focal_method) else ' '.join(test_method)
                complexity_type = complexity_count(context)

                if len(focal_method) == 0:
                    datapoint = models.atlas_datapoint(focal_method='',
                                                       test_method=' '.join(test_method),
                                                       assertion=assertion,
                                                       assertion_type=assertion_type,
                                                       method_name='',
                                                       test_name=test_method[0],
                                                       complexity=complexity_type)
                else:
                    datapoint = models.atlas_datapoint(focal_method=' '.join(focal_method),
                                                       test_method=' '.join(test_method),
                                                       assertion=assertion,
                                                       assertion_type=assertion_type,
                                                       method_name=focal_method[0],
                                                       test_name=test_method[0],
                                                       complexity=complexity_type)
                raw_records.append(datapoint)

        return raw_records
