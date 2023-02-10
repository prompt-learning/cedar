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
### Before commit
{data.source_code}

### After commit
{data.target_code}
{STOP_DELIMETER}
"""
    else:
        return f"""
### Refactor the following Java method:
### Before commit
{data.source_code}

### After commit
{data.target_code}
{STOP_DELIMETER}
"""


def get_tufano_query_template(data: models.tufano_datapoint, with_commands: bool) -> str:
    if with_commands:
        return f"""
### Refactor the following Java method:
### Before commit
{data.source_code}

### After commit"""
    else:
        return f"""
### Refactor the following Java method:
### Before commit
{data.source_code}

### After commit"""
