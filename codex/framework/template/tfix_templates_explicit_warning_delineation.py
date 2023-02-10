import os
import sys
import models

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# STOP_DELIMETER = '==================='
STOP_DELIMETER = "END_OF_DEMO"


def get_tfix_demo_template_explicit_warning_delineation(data: models.tfix_datapoint, with_commands: bool) -> str:
    source_code_original = data.source_code
    source_code_original = source_code_original.replace(data.warning_line,
                                 f"{data.warning_line} ##warning line \n")

    if with_commands:
        return f"""
### Fix bug in the following JavaScript code:
### Buggy JavaScript
{source_code_original}

"rule_id" : {data.linter_report_rule_id}
"evidence": {data.linter_report_evidence}
"warning_line": {data.warning_line}
   
### Fixed JavaScript
{data.target_code}
{STOP_DELIMETER}
"""
    else:
        return f"""
### Fix bug in the following JavaScript code:
### Buggy JavaScript
{data.source_code}
   
### Fixed JavaScript
{data.target_code}
{STOP_DELIMETER}
        """


def get_tfix_query_template_explicit_warning_delineation(data: models.atlas_datapoint, with_commands: bool) -> str:
    source_code_original = data.source_code
    source_code_original = source_code_original.replace(data.warning_line,
                                                    f"{data.warning_line} ##warning line \n")

    if with_commands:
        return f"""
### Fix bug in the following JavaScript code:
### Buggy JavaScript
{source_code_original}

"rule_id" : {data.linter_report_rule_id}
"evidence": {data.linter_report_evidence}
"warning_line": {data.warning_line}
   
### Fixed JavaScript"""
    else:
        return f"""
### Fix bug in the following JavaScript code:
### Buggy JavaScript
{source_code_original}
   
### Fixed JavaScript"""
