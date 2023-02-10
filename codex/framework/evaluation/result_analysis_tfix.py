import csv, sys
import pandas as pd
from collections import Counter


def fix_nulls(s):
    for line in s:
        yield line.replace('\0', '')


if __name__ == "__main__":
    file_name = sys.argv[1]

    exact_match_count = 0
    match_count = 0
    with open(file_name, newline='') as csvfile:
        # csvreader = csv.reader(csvfile, delimiter=',')
        csvreader = csv.DictReader(fix_nulls(csvfile), delimiter=',')

        next(csvreader, None)  # skip the headersutf

        total_count = 0
        sum_lcs_percentage = 0
        sum_inference_time_secs = 0
        sum_edit_distance = 0
        sum_num_demos = 0
        demos = []
        for tfix_result_row in csvreader:
            prompt = tfix_result_row["prompt"]
            num_demos = prompt.count('END_OF_DEMO')
            demos.append(num_demos)
            expected = tfix_result_row["expected"].strip().lower()
            codex = tfix_result_row["codex"].strip().lower()
            is_exact_match = tfix_result_row["is_exact_match"]
            is_match = tfix_result_row["is_match"]
            lcs = tfix_result_row["lcs"]
            edit_distance = tfix_result_row["edit_distance"]
            inference_time_secs = tfix_result_row["inference_time (secs)"]

            if len(lcs) != 0:
                sum_lcs_percentage += (len(lcs) /len(expected) ) * 100

            sum_num_demos += num_demos
            sum_edit_distance += int(edit_distance)
            sum_inference_time_secs += float(inference_time_secs)
            if is_exact_match == "True":
                exact_match_count = exact_match_count + 1
            if is_match == "True":
                match_count = match_count + 1
            total_count = total_count + 1

    avg_lcs_percentage = sum_lcs_percentage/total_count
    avg_inference_time = sum_inference_time_secs/total_count
    avg_edit_distance = sum_edit_distance/total_count
    print('avg_lcs (%):', avg_lcs_percentage)
    print('avg inference time', avg_inference_time)
    print('avg_num_demos:', (sum_num_demos / total_count))
    print('avg edit distance', avg_edit_distance)
    print('exact_match_count:', exact_match_count, 'match_count:', match_count)
    print(f"exact match_count (%): {round(((exact_match_count / total_count) * 100), 3)}, "
          f"match_count(%): {round(((match_count / total_count) * 100), 3)}")
