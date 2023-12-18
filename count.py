import pandas as pd

# read the input csv file
input_file = 'parts.csv'
df = pd.read_csv(input_file)

# Create the new DataFrame to store the results
new_df = pd.DataFrame(columns=['CONCERN', 'NO_OF_PARTS', 'NO_OF_CPSCs', 'COMPONENT_AFFECTED', 'HOMOLOG_AFFECTED', 'ASSEMBLY_IMPACT', 'NO_OF_AP', 'NO_OF_DP', 'NO_OF_RV', 'NO_OF_RP', 'NO_OF_NOACTION'])

# Iterate through rows with the same "CONCERN" column value
for CONCERN, CONCERN_rows in df.groupby('CONCERN'):
    NO_OF_PARTS = CONCERN_rows[['PREFIX', 'BASE', 'SUFFIX']].drop_duplicates().shape[0]
    NO_OF_CPSCs = CONCERN_rows['CPSC'].nunique()
    if 'Y' in CONCERN_rows['HOMOLOGATION'].values:
        HOMOLOG_AFFECTED = 'Y'
    else:
        HOMOLOG_AFFECTED = 'N'
    
    if 'C' in CONCERN_rows['C_F_FLAG'].values:
        COMPONENT_AFFECTED = 'Y'
    else:
        COMPONENT_AFFECTED = 'N'
    
    if 'Y' in CONCERN_rows['ASSY_IMPACT_1'].values:
        ASSEMBLY_IMPACT = 'Y'
    else:
        ASSEMBLY_IMPACT = 'N'

    NO_OF_AP = (CONCERN_rows['ACTION_IND'] == 'AP').sum()
    NO_OF_DP = (CONCERN_rows['ACTION_IND'] == 'DP').sum()
    NO_OF_RV = (CONCERN_rows['ACTION_IND'] == 'RV').sum()
    NO_OF_RP = (CONCERN_rows['ACTION_IND'] == 'RP').sum()
    NO_OF_NOACTION = (CONCERN_rows['ACTION_IND'] == '').sum()

    df_newrow = pd.DataFrame({
        'CONCERN': [CONCERN],
        'NO_OF_PARTS': [NO_OF_PARTS],
        'NO_OF_CPSCs': [NO_OF_CPSCs],
        'COMPONENT_AFFECTED': [COMPONENT_AFFECTED],
        'HOMOLOG_AFFECTED': [HOMOLOG_AFFECTED],
        'ASSEMBLY_IMPACT': [ASSEMBLY_IMPACT],
        'NO_OF_AP': [NO_OF_AP],
        'NO_OF_DP': [NO_OF_DP],
        'NO_OF_RV': [NO_OF_RV],
        'NO_OF_RP': [NO_OF_RP],
        'NO_OF_NOACTION': [NO_OF_NOACTION]
    })

    new_df = pd.concat([new_df, df_newrow], ignore_index=True)

new_df['num'] = new_df['CONCERN'].str.extract('(\d+)').astype(int)
new_df = new_df.sort_values('num')
new_df.drop(columns='num', inplace=True)


# save to output csv file
output_file = 'parts_new.csv'
new_df.to_csv(output_file, index=False)