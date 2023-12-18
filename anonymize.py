import pandas as pd

# read the input csv file
input_file = 'base.csv'
df = pd.read_csv(input_file)

# separate the number part of the data and sort
df['num'] = df['CONCERN'].str.extract('(\d+)').astype(int)
df = df.sort_values('num')

# mask the data with increasing ranks from the num column, appended to "CONCERN-"
df['CONCERN'] = 'CONCERN-' + df['num'].rank(method='first').astype(int).astype(str)

# delete the temp 'num' column
df.drop(columns='num', inplace=True)

# update the dataframe kept in the original order
df.sort_index(inplace=True)

# save to output csv file
output_file = 'anonymized_base.csv'
df.to_csv(output_file, index=False)