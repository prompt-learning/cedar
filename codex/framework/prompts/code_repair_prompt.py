import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from prompt import Prompt
from demonstration.code_repair_demonstrations import CodeRepairDemonstration


class CodeRepairPrompt(Prompt):

    def __init__(self, demonstrations, query):
        self.demonstration_records = demonstrations
        self.query = query

    def construct_prompt(self):
        code_repair_demonstration = CodeRepairDemonstration()
        demonstrations = code_repair_demonstration.demonstrations()
        prompt = f"{demonstrations}" \
                 f"{self.query}"
        return prompt
