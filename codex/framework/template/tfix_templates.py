import os
import sys
import models
from util import utils

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

STOP_DELIMETER = "END_OF_DEMO"


def get_tfix_demo_template(data: models.tfix_datapoint, with_commands: bool) -> str:
    if with_commands:
        return f"""
### Fix ESLint error in the following JavaScript code:
### Buggy JavaScript
{data.source_code}

"rule_id" : {data.linter_report_rule_id}
"evidence": {data.linter_report_evidence}
"warning_line": {data.warning_line}
   
### Fixed JavaScript
{data.target_code}
{STOP_DELIMETER}
"""
    else:
        return f"""
{data.source_code}

{data.linter_report_rule_id}
{data.linter_report_evidence}
{data.warning_line}
   
{data.target_code}
{STOP_DELIMETER}
"""


def is_tfix_query_within_context_window(tfix_query: str, context_window=8000) -> bool:
    return utils.count_codex_tokens(tfix_query) <= context_window


def handle_if_tfix_query_exceeds_context_window(data: models.atlas_datapoint, tfix_query: str, with_commands: bool, context_window=8000) -> str:
    is_within_context_window = is_tfix_query_within_context_window(tfix_query, context_window)

    if is_within_context_window:
        return tfix_query
    else:
        if with_commands:
            output_reduce_context_length = f"""
### Fix ESLint error in the following JavaScript code:
### Buggy JavaScript
{data.source_code}

"rule_id" : {data.linter_report_rule_id}
"evidence": {data.linter_report_evidence}

### Fixed JavaScript"""
        else:
            output_reduce_context_length = f"""
{data.source_code}

{data.linter_report_rule_id}
{data.linter_report_evidence}"""
        return output_reduce_context_length


def get_tfix_query_template(data: models.atlas_datapoint, with_commands: bool) -> str:
    if with_commands:
        output_tfix_query = f"""
### Fix ESLint error in the following JavaScript code:
### Buggy JavaScript
{data.source_code}

"rule_id" : {data.linter_report_rule_id}
"evidence": {data.linter_report_evidence}
"warning_line": {data.warning_line}
   
### Fixed JavaScript"""
    else:
        output_tfix_query = f"""
{data.source_code}

{data.linter_report_rule_id}
{data.linter_report_evidence}
{data.warning_line}
"""

    if is_tfix_query_within_context_window(output_tfix_query):
        return output_tfix_query
    else:
        return handle_if_tfix_query_exceeds_context_window(data, output_tfix_query, with_commands, context_window=8000)
    return output_tfix_query
