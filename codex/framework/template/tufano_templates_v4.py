import os
import sys
import models

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# STOP_DELIMETER = '==================='
STOP_DELIMETER = "END_OF_DEMO"


def get_tufano_demo_template(data: models.tufano_datapoint, with_commands: bool) -> str:
    if with_commands:
        return f"""
### Refactor the following Java method:
### Before code refactoring
{data.source_code}

### After code refactoring
{data.target_code}
{STOP_DELIMETER}
"""
    else:
        return f"""
### Refactor the following Java method:
### Before code refactoring
{data.source_code}

### After code refactoring
{data.target_code}
{STOP_DELIMETER}
"""


def get_tufano_query_template(data: models.tufano_datapoint, with_commands: bool) -> str:
    if with_commands:
        return f"""
### Refactor the following Java method:
### Before code refactoring
{data.source_code}

### After code refactoring"""
    else:
        return f"""
### Refactor the following Java method:
### Before code refactoring
{data.source_code}

### After code refactoring"""
