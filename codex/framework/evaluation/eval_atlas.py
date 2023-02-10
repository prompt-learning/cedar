import csv, sys
from evaluation import Evaluation


if __name__ == "__main__":
    file_name = sys.argv[1]
    csv_data = []
    with open(file_name, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            csv_data.append({
                'expected': row[0],
                'actual': row[1],
                'is_exact_match': row[2],
                'lcs': row[3],
                'edit_distance': row[4]
            })

    exact_match_count = 0
    is_match_count = 0
    with open(file_name.split('.csv')[0] + '-new.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        i = 0
        for data in csv_data:
            if i == 0:
                writer.writerow(['expected', 'actual', 'is_exact_match', 'is_match', 'lcs', 'edit_distance'])
                i += 1
                continue
            evl = Evaluation(data['expected'], data['actual'])
            is_match = evl.is_match()
            if is_match:
                is_match_count += 1
            if data['is_exact_match'] == 'True':
                exact_match_count += 1

            writer.writerow([data['expected'], data['actual'], data['is_exact_match'], is_match, data['lcs'], data['edit_distance']])
            i += 1
    
    print('Exact Match', exact_match_count, 'Match', is_match_count)    

    