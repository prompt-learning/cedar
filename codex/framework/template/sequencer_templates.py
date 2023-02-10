import os
import sys
import models
from util import utils

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# STOP_DELIMETER = '==================='
STOP_DELIMETER = "END_OF_DEMO"


def get_sequencer_demo_template(data: models.sequencer_datapoint, with_commands: bool) -> str:
    if with_commands:
        return f"""
### Fix bug in the following Java class:
### Buggy Java code
{data.buggy_method_context}

"buggy java line": {data.buggy_code}

### Fixed java line
{data.correct_code}
{STOP_DELIMETER}
"""
    else:
        return f"""
### Fix bug in the following Java class:
### Buggy Java code
{data.buggy_method_context}
   
### Fixed java line
{data.correct_code}
{STOP_DELIMETER}
"""


def is_sequencer_query_within_context_window(tfix_query: str, context_window=8000) -> bool:
    return utils.count_codex_tokens(tfix_query) <= context_window


def handle_if_sequencer_query_exceeds_context_window(data: models.atlas_datapoint, tfix_query: str, with_commands: bool, context_window=8000) -> str:
    is_within_context_window = is_sequencer_query_within_context_window(tfix_query, context_window)

    if is_within_context_window:
        return tfix_query
    else:
        if with_commands:
            output_reduce_context_length = f"""
### Fix bug in the following Java code class:
### Buggy Java code
{data.buggy_method_context}

"buggy java line": {data.buggy_code}

### Fixed java line"""
        else:
            output_reduce_context_length = f"""
### Fix bug in the following Java code:
### Buggy Java code
{data.source_code}

### Fixed java line"""
        return output_reduce_context_length


def get_sequencer_query_template(data: models.sequencer_datapoint, with_commands: bool) -> str:
    if with_commands:
        output_tfix_query = f"""
### Fix bug in the following Java code:
### Buggy Java code
{data.buggy_method_context}

"buggy java line": {data.buggy_code}
   
### Fixed java line"""
    else:
        output_tfix_query = f"""
### Fix bug in the following Java code:
### Buggy Java code
{data.buggy_method_context}
   
### Fixed java line"""

    if is_sequencer_query_within_context_window(output_tfix_query):
        return output_tfix_query
    else:
        return handle_if_sequencer_query_exceeds_context_window(data, output_tfix_query, with_commands, context_window=8000)
    return output_tfix_query
