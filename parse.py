import pandas as pd
import re

# read the input csv file
input_file = 'responses.csv'
df = pd.read_csv(input_file)
res1 = df['RES_LINE'][0]
res2 = df['RES_LINE'][1]
res3 = df['RES_LINE'][2]
res4 = df['RES_LINE'][3]
res5 = df['RES_LINE'][4]

con1 = df['CONCERN'][0]
con2 = df['CONCERN'][1]
con3 = df['CONCERN'][2]
con4 = df['CONCERN'][3]
con5 = df['CONCERN'][4]


def extract_text_to_dataframe(string, start_args, end_args, df, con):
    extracted_texts = []
    
    for start_arg, end_arg in zip(start_args, end_args):
        start_index = string.find(start_arg)
        end_index = string.find(end_arg)
        
        if start_index != -1 and end_index != -1:
            extracted_text = string[start_index + len(start_arg):end_index].strip()
            extracted_texts.append(extracted_text)
        else:
            extracted_texts.append('')
    
    df[con + ' Answers'] = extracted_texts
    return df

start_args = ['CONCERN GUIDE', 'ATTRIBUTE TESTING', 'COMPLETION DATE', 'SUPERVISOR FOR THIS CHANGE', 'PPAP DATES', 'PHASE 3', 'BUILD VERIFICATION?', 'PART AVAILABILITY DATE', 'REVERT BACK DATE', 'FILE NAME/LOCATION', 'CAD CONTACT', 'BUYER CONTACT', 'IS THE SUPPLIER', 'TRY OUT COMPLETED', 'OF TRIAL PARTS', 'BLD DATE', '(IN PLANT) DATE', 'RECEIPT OF PO']
end_args = ['2)', 'A)', 'B)', '3)', '4)', '5)', '6)', '7)', '8)', '9)', '10)', '11)', '12)', 'A)', 'B)', 'C)', 'D)','']
labels = ['1', '2', '2A', '2B', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '12A', '12B', '12C', '12D']
df = pd.DataFrame({'Question': labels})
extract_text_to_dataframe(res1, start_args, end_args, df, con1)
extract_text_to_dataframe(res2, start_args, end_args, df, con2)
extract_text_to_dataframe(res3, start_args, end_args, df, con3)
extract_text_to_dataframe(res4, start_args, end_args, df, con4)
extract_text_to_dataframe(res5, start_args, end_args, df, con5)
df.to_csv('parsed.csv', index=False)
print(df)

newdf = df.copy()
def convert_to_structured(df, yn_indices, date_indices, data_indices):
    for i in yn_indices:    # structuring Y/N question rows
        row = df.loc[i]
        for col in df.columns:
            if 'Y' in str(row[col]):
                newdf.at[i, col] = 1
            elif 'N' in str(row[col]):
                newdf.at[i, col] = 2
            else:
                newdf.at[i, col] = 0  
    for i in date_indices:  # structuring question rows which check for dates
        row = df.loc[i]
        for col in df.columns:
            if "DD-MM-YYYY" in row[col]:
                newdf.at[i, col] = 0
            elif row[col] == "":
                newdf.at[i, col] = 2
            else:
                newdf.at[i, col] = 1
    for i in data_indices:  # structuring question rows which check for existing data
        row = df.loc[i]
        for col in df.columns:
            if ("NA" in row[col]) | ("N/A" in row[col]):
                newdf.at[i, col] = 0
            elif (row[col] == "") | ((row[col] == "*")):
                newdf.at[i, col] = 2
            else:
                newdf.at[i, col] = 1
    row = df.loc[2]    # structuring 2A)
    for col in df.columns:
        if ("NA" in row[col]) | ("N/A" in row[col]) | ("nan" in row[col]):
            newdf.at[2, col] = 0
        elif ("DD-MM-YYYY" in row[col]):
            newdf.at[2, col] = 2
        else:
            newdf.at[2, col] = 1
    row = df.loc[3]    # structuring 2B)
    for col in df.columns:
        if (row[col] == ""):
            newdf.at[3, col] = 0
        else:
            newdf.at[3, col] = 1
    row = df.loc[5]    # structuring 4) Phase dates
    pattern = r"\d+[-/][A-Za-z]+[-/]\d+"
    for col in df.columns:
        if (row[col] == ""):
            newdf.at[5, col] = 0
        else:
            dates = re.findall(pattern, row[col])
            newdf.at[5, col] = ' '.join(dates)
yn_rows = [0, 1, 6, 13]
date_rows = [4, 7, 8, 15, 16]
data_rows = [9, 10, 11, 12, 14, 17]
convert_to_structured(df, yn_rows, date_rows, data_rows)
newdf['Question'] = df['Question']
print(newdf)
newdf.to_csv('structured.csv', index=False)


key_value_pairs = {}
for col in newdf.columns[1:]:
    pairs = {key: value for key, value in zip(newdf["Question"], newdf[col])}
    key_value_pairs[col] = pairs

print(key_value_pairs)