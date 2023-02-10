import csv, sys
from evaluation_tfix import Evaluation


if __name__ == "__main__":
    file_name = sys.argv[1]
    csv_data = []
    with open(file_name, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            csv_data.append({
                'buggy_code': row[0],
                'warning_line': row[1],
                'linter_report_rule_id': row[2],
                'linter_report_message': row[3],
                'expected': row[4],
                'codex': row[5],
                'is_exact_match': row[6],
                'is_match': row[7],
                'lcs': row[8],
                'edit_distance': row[9],
                'inference_time (secs)': row[10],
                'gpt_token_count': row[11],
                'word_count': row[12],
                'response_completion_tokens': row[13],
                'response_prompt_tokens': row[14],
                'response_total_tokens': row[15]
            })

    exact_match_count = 0
    is_match_count = 0
    with open(file_name.split('.csv')[0] + '-new.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        i = 0
        for data in csv_data:
            if i == 0:
                writer.writerow(['buggy_code', 'warning_line', 'linter_report_rule_id', 'linter_report_message', 'expected', 'codex', 'edit_distance', 'is_exact_match', 'is_match', 'lcs', 'edit_distance', 'inference_time (secs)', 'gpt_token_count', 'word_count', 'response_completion_tokens', 'response_prompt_tokens', 'response_total_tokens'])
                i += 1
                continue
            evl = Evaluation(data['buggy_code'], data['expected'], data['codex'], data['warning_line'])
            is_match = evl.is_match()
            if is_match:
                is_match_count += 1
            is_exact_match = evl.is_exact_match()
            if is_exact_match:
                exact_match_count += 1

            writer.writerow(
                [data['buggy_code'], data['warning_line'],data['linter_report_rule_id'], data['linter_report_message'], data['expected'], data['codex'], data['edit_distance'], is_exact_match, is_match, data['lcs'], data['edit_distance'], data['inference_time (secs)'], data['gpt_token_count'], data['word_count'], data['response_completion_tokens'], data['response_prompt_tokens'], data['response_total_tokens']]
            )
            i += 1

    print('Exact Match', exact_match_count, 'Match', is_match_count)