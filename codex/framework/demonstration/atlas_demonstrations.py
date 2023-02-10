import vdblite

import models
from embedding.embedding_utils import get_embedding
from models import atlas_datapoint
from util import utils
from .demonstrations import Demonstration
from template import assert_templates

TYPE_LIMIT = 1

MAX_ATLAS_COMPLETION_LENGTH_TRAIN = 500

class AtlasDemonstration(Demonstration):
    def construct(self, records):
        final_demonstration = ''
        datapoint_by_assertion_type = {}

        for r in records:
            if r.assertion_type in datapoint_by_assertion_type:
                datapoint_by_assertion_type[r.assertion_type].append(r)
            else:
                datapoint_by_assertion_type[r.assertion_type] = [r]

        for _, datapoints in datapoint_by_assertion_type.items():
            count = 0
            for record in datapoints:
                demo = assert_templates.get_atlas_demo_template(record, self.with_commands)
                if record.focal_method != '' and count <= TYPE_LIMIT:
                    final_demonstration += demo
                    count += 1

        return final_demonstration

    def construct_semantic_search(self,
                                  dp: atlas_datapoint,
                                  demonstration_records: list[models.atlas_datapoint],
                                  query: str):
        final_demonstration = ''

        length_of_query = utils.count_codex_tokens(query)
        length_of_completion = 500
        max_demo_length = 8000 - (length_of_query + length_of_completion)

        query_buggy_code_embedding = get_embedding(dp.focal_method)

        print("going to semantic search for {} in Vector DB".format(query))
        results = vdb.search(query_buggy_code_embedding, 'vector', 100)
        records = results
        print("got response from Vector DB")


        datapoint_by_assertion_type = {}
        for r in records:
            demo_record = atlas_datapoint(focal_method=r['focal_method'],
                                          test_method=r['test_method'],
                                          assertion=r['assertion'],
                                          assertion_type=r['assertion_type'],
                                          method_name=r['method_name'],
                                          test_name=r['test_name'],
                                          complexity=r['complexity']
                                          )

            if demo_record.assertion_type in datapoint_by_assertion_type:
                datapoint_by_assertion_type[demo_record.assertion_type].append(demo_record)
            else:
                datapoint_by_assertion_type[demo_record.assertion_type] = [demo_record]

        for _, datapoints in datapoint_by_assertion_type.items():
            count = 0
            for record in datapoints:
                demo = assert_templates.get_atlas_demo_template(record, self.with_commands)
                if record.focal_method != '' \
                        and ((utils.count_codex_tokens(final_demonstration) + utils.count_codex_tokens(
                    demo)) <= max_demo_length):
                    final_demonstration += demo
                    count += 1

        return final_demonstration
