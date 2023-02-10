import models

from typing import List
import json

from dataset.dataset import Dataset


class TFixDataset(Dataset):
    def __init__(self, path):
        self.path = path
        with open(self.path, encoding = "ISO-8859-1") as file:
            self.dataset_json = json.load(file)

    def parse(self) -> List[models.tfix_datapoint]:
        raw_records = []
        for dp in self.dataset_json:
            source_code = dp["source_code"]
            target_code = dp["target_code"]
            source_file = dp["source_file"]
            target_file = dp["target_file"]

            if "evidence" in dp:
                linter_report_evidence = dp["evidence"]
            else:
                linter_report_evidence = dp["linter_report"]["evidence"]

            if "message" in dp:
                linter_report_message = dp["message"]
            else:
                linter_report_message = dp["linter_report"]["message"]

            if "rule_id" in dp:
                linter_report_rule_id = dp["rule_id"]
            else:
                linter_report_rule_id = dp["linter_report"]["rule_id"]

            warning_line = dp["warning_line"]

            dp = models.tfix_datapoint(source_code=source_code,
                                       target_code=target_code,
                                       source_file=source_file,
                                       target_file=target_file,
                                       linter_report_evidence=linter_report_evidence,
                                       linter_report_message=linter_report_message,
                                       linter_report_rule_id=linter_report_rule_id,
                                       warning_line=warning_line,
                                       repo=dp.get('repo'))

            raw_records.append(dp)
        return raw_records
