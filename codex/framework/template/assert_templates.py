import os
import sys
import models

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# STOP_DELIMETER = '==================='
STOP_DELIMETER = "END_OF_DEMO"


def get_atlas_demo_template(data: models.atlas_datapoint, with_commands: bool) -> str:
    if with_commands:
        return f"""
### METHOD_UNDER_TEST:
{data.focal_method}

### UNIT_TEST
{data.test_method}

[METHOD_UNDER_TEST]: {data.method_name}
[UNIT_TEST]: {data.test_name}

### generate assertion
{data.assertion}
{STOP_DELIMETER}
"""
    else:
        return f"""
{data.focal_method}

{data.test_method}

### generate assertion
{data.assertion}
{STOP_DELIMETER}
        """


def get_atlas_query_template(data: models.atlas_datapoint, with_commands: bool) -> str:
    if with_commands:
        return f"""
### METHOD_UNDER_TEST:
{data.focal_method}

### UNIT_TEST
{data.test_method}

[METHOD_UNDER_TEST]: {data.method_name}
[UNIT_TEST]: {data.test_name}

### generate assertion"""
    else:
        return f"""
{data.focal_method}

{data.test_method}

### generate assertion"""


def get_atlas_query_template_with_detailed_nl_desc(data: models.atlas_datapoint, with_commands: bool) -> str:
    if with_commands:
        return f"""generate assertion in the following java code:
### METHOD_UNDER_TEST:
{data.focal_method}

### UNIT_TEST
{data.test_method}

[METHOD_UNDER_TEST]: {data.method_name}
[UNIT_TEST]: {data.test_name}

### generate assertion
"""
    else:
        return f"""
{data.focal_method}

{data.test_method}

### generate assertion"""