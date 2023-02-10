import csv, sys
import pandas as pd
from evaluation import Evaluation
from collections import Counter


def fix_nulls(s):
    for line in s:
        yield line.replace('\0', '')


ASSERTION_TYPES = ["assertEquals", "assertTrue", "assertNotNull",
                   "assertThat", "assertNull", "assertFalse",
                   "assertArrayEquals", "assertSame"]

if __name__ == "__main__":
    file_name = sys.argv[1]

    exact_match_count = 0
    match_count = 0
    assertion_type_matched_count = 0
    with open(file_name, newline='') as csvfile:
        # csvreader = csv.reader(csvfile, delimiter=',')
        csvreader = csv.reader(fix_nulls(csvfile), delimiter=',')

        next(csvreader, None)  # skip the headersutf

        total_count = 0
        sum_lcs_percentage = 0
        sum_inference_time_secs = 0
        sum_edit_distance = 0

        for atlas_result_row in csvreader:
            expected = atlas_result_row[0]
            actual = atlas_result_row[1]
            is_exact_match = atlas_result_row[2]
            is_match = Evaluation(expected, actual).is_match()
            lcs = atlas_result_row[4]
            edit_distance = atlas_result_row[5]
            inference_time_secs = atlas_result_row[6]
            if len(lcs) != 0:
                sum_lcs_percentage += (len(lcs) /len(expected) ) * 100
            
            expected_assertion_type = None
            actual_assertion_type = None
            for a in ASSERTION_TYPES:
                if a in expected:
                    expected_assertion_type = a
                if a in actual:
                    actual_assertion_type = a
            
            assertion_type_matched = expected_assertion_type == actual_assertion_type

            if assertion_type_matched:
                assertion_type_matched_count += 1

            sum_edit_distance += int(edit_distance)
            sum_inference_time_secs += float(inference_time_secs)
            if is_exact_match == "True":
                exact_match_count = exact_match_count + 1
            if is_match:
                match_count = match_count + 1
            total_count = total_count + 1
        
    avg_lcs_percentage = sum_lcs_percentage/total_count
    avg_inference_time = sum_inference_time_secs/total_count
    avg_edit_distance = sum_edit_distance/total_count
    print('avg_lcs (%):', avg_lcs_percentage)
    print('assertion_type_matched count:', (assertion_type_matched_count / total_count) * 100)
    print('avg inference time', avg_inference_time)
    print('avg edit distance', avg_edit_distance)
    print('exact_match_count:', exact_match_count, 'match_count:', match_count)
    print(f"exact match_count (%): {round(((exact_match_count / total_count) * 100), 3)}, "
          f"match_count(%): {round(((match_count / total_count) * 100), 3)}")
