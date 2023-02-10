import pandas as pd

csv_io = "./atlas_stats_testing.csv"
df = pd.read_csv(csv_io, index_col=0)
context_length = 2001

df['rank'] = df.groupby("type")['word_count'].rank(method="first", ascending=True)
df = df.sort_values(['rank', 'word_count'])
df['word_count_cumsum'] = df['word_count'].cumsum()

df = df[df['word_count_cumsum'] < context_length]

types_list = df.groupby('type')['word_count'].apply(list)

print(types_list)
