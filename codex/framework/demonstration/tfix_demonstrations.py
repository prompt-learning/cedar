import os
import sys
import random

import vdblite

import models
from embedding import vector_db_search
from embedding.embedding_unixcoder_utils import get_unixcoder_embedding
from embedding.embedding_utils import get_embedding
from embedding.vector_db_search import embedding_type
from models import tfix_datapoint
from models import tfix_mode
from template import tfix_templates
from template.tfix_template_options import tfix_template_type
from template.tfix_templates_explicit_warning_delineation import get_tfix_demo_template_explicit_warning_delineation
from util import utils

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from demonstrations import Demonstration

TYPE_LIMIT = 52
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

MAX_TFIX_COMPLETION_LENGTH_TRAIN = 728

class TFixDemonstration(Demonstration):

    def construct(self, records):
        final_demonstration = ''
        datapoints_by_tfix_error_type = {}

        for r in records:
            if r.linter_report_rule_id in datapoints_by_tfix_error_type:
                datapoints_by_tfix_error_type[r.linter_report_rule_id].append(r)
            else:
                datapoints_by_tfix_error_type[r.linter_report_rule_id] = [r]

        count = 0
        for _, datapoints in datapoints_by_tfix_error_type.items():
            for record in datapoints:
                demo = tfix_templates.get_tfix_demo_template(record, self.with_commands)
                final_demonstration += demo
                count += 1

        print("Total number of tfix demonstrations: {}".format(count))
        return final_demonstration

    def construct_more_example_of_a_given_violation(self, records, tfix_error_type):
        final_demonstration = ''
        datapoints_by_tfix_error_type = {}

        for r in records:
            if r.linter_report_rule_id in datapoints_by_tfix_error_type:
                datapoints_by_tfix_error_type[r.linter_report_rule_id].append(r)
            else:
                datapoints_by_tfix_error_type[r.linter_report_rule_id] = [r]

        datapoints_by_tfix_error_type = datapoints_by_tfix_error_type[tfix_error_type]
        # for _, datapoints in datapoints_by_tfix_error_type.items():
        count = 0
        for record in datapoints_by_tfix_error_type:
            demo = tfix_templates.get_tfix_demo_template(record, self.with_commands)
            if count < TYPE_LIMIT:
                final_demonstration += demo
                count += 1

        return final_demonstration

    def construct_more_example_of_a_given_violation_until_8000_tokens(self, records, query, tfix_error_type,
                                                                      template_type: tfix_template_type):
        final_demonstration = ''
        datapoints_by_tfix_error_type = {}

        for r in records:
            if r.linter_report_rule_id in datapoints_by_tfix_error_type:
                datapoints_by_tfix_error_type[r.linter_report_rule_id].append(r)
            else:
                datapoints_by_tfix_error_type[r.linter_report_rule_id] = [r]

        datapoints_by_tfix_error_type = datapoints_by_tfix_error_type[tfix_error_type]

        total_count = len(datapoints_by_tfix_error_type)
        take_random_n = min(total_count, 1000)
        random_datapoints_by_tfix_error_type = random.sample(datapoints_by_tfix_error_type, take_random_n)

        # for _, datapoints in datapoints_by_tfix_error_type.items():
        count = 0

        length_of_query = utils.count_codex_tokens(query)
        length_of_completion = MAX_TFIX_COMPLETION_LENGTH_TRAIN
        max_demo_length = 8000 - (length_of_query + length_of_completion)

        for record in random_datapoints_by_tfix_error_type:
            if template_type is tfix_template_type.explicit_warning_delineation:
                demo = get_tfix_demo_template_explicit_warning_delineation(record, self.with_commands)
            else:
                demo = tfix_templates.get_tfix_demo_template(record, self.with_commands)

            # if count < TYPE_LIMIT:
            if (utils.count_codex_tokens(final_demonstration) + utils.count_codex_tokens(demo)) <= max_demo_length:
                final_demonstration += demo
                count += 1
            else:
                break

        return final_demonstration

    def construct_semantic_search(self,
                                  dp: tfix_datapoint,
                                  records: list[models.tfix_datapoint],
                                  query: str,
                                  tfix_error_type: str,
                                  template_type: tfix_template_type,
                                  semantic_search_type: tfix_mode):
        final_demonstration = ''
        datapoints_by_tfix_error_type = {}

        for r in records:
            if r.linter_report_rule_id in datapoints_by_tfix_error_type:
                datapoints_by_tfix_error_type[r.linter_report_rule_id].append(r)
            else:
                datapoints_by_tfix_error_type[r.linter_report_rule_id] = [r]

        datapoints_by_tfix_error_type = datapoints_by_tfix_error_type[tfix_error_type]

        total_count = len(datapoints_by_tfix_error_type)
        take_random_n = min(total_count, 1000)
        random_datapoints_by_tfix_error_type = random.sample(datapoints_by_tfix_error_type, take_random_n)

        # for _, datapoints in datapoints_by_tfix_error_type.items():
        count = 0

        length_of_query = utils.count_codex_tokens(query)
        length_of_completion = MAX_TFIX_COMPLETION_LENGTH_TRAIN
        max_demo_length = 8000 - (length_of_query + length_of_completion)

        if semantic_search_type == tfix_mode.semantic_search_st_n_shot:
            query_source_code_embedding = get_embedding(dp.source_code)
        elif semantic_search_type == tfix_mode.semantic_search_unixcoder_n_shot:
            query_source_code_embedding = get_unixcoder_embedding(dp.source_code)
        else:
            raise Exception('Invalid semantic search type')

        random_datapoints_by_tfix_error_type = vector_db_search.search(query_source_code_embedding,
                                                                       embedding_type.st)
        for record in random_datapoints_by_tfix_error_type:

            dp = tfix_datapoint(
                source_code=record["source_code"],
                target_code=record["target_code"],
                source_file="N/A",
                target_file="N/A",
                linter_report_evidence="N/A",
                linter_report_message=record["linter_report_message"],
                linter_report_rule_id=record["linter_report_rule_id"],
                warning_line="N/A",
                repo=record["repo"]
            )
            if dp.linter_report_rule_id != tfix_error_type:
                continue

            if template_type is tfix_template_type.explicit_warning_delineation:
                demo = get_tfix_demo_template_explicit_warning_delineation(dp, self.with_commands)
            else:
                demo = tfix_templates.get_tfix_demo_template(dp, self.with_commands)

            # if count < TYPE_LIMIT:
            if (utils.count_codex_tokens(final_demonstration) + utils.count_codex_tokens(demo)) <= max_demo_length:
                final_demonstration += demo
                count += 1
            else:
                break

        return final_demonstration
