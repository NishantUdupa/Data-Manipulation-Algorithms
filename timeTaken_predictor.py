import pandas as pd
from autogluon.tabular import TabularDataset, TabularPredictor

def create_timeTaken (df):
    # remove rows with missing/blank date values
    for column in ['CONCURRED_DATE', 'ORIGIN_DATE']:
            df = df[~(df[column] == '0001-01-01')]
    #Calculate time difference and put that in new column in days
    df['CONCURRED_DATE'] = pd.to_datetime(df['CONCURRED_DATE'])
    df['ORIGIN_DATE'] = pd.to_datetime(df['ORIGIN_DATE'])
    df['timeTaken'] = (df['CONCURRED_DATE'] - df['ORIGIN_DATE']).dt.days
    #Drop date columns
    df.drop(columns='CONCURRED_DATE', inplace=True)
    df.drop(columns='ORIGIN_DATE', inplace=True)
    
    return df

# read the input csv file
traindf = pd.read_csv('training_data.csv')
testdf = pd.read_csv('test_data.csv')

# run code to clean and calculate train and test data
traindf = create_timeTaken(traindf)
testdf = create_timeTaken(testdf)

# save to output csv file
traindf.to_csv('training_data_new.csv', index=False)
testdf.to_csv('test_data_new.csv', index=False)

#train the data to predict the column 'timeTaken'
label = 'timeTaken'
predictor = TabularPredictor(label=label, problem_type='regression').fit(train_data=traindf, time_limit=600)
#read test data and provide extra analysis
leaderboard = predictor.leaderboard(testdf)
y_test = testdf[label]
testdf = testdf.drop(columns=[label])

#generate predictions for each row in test data
y_pred = predictor.predict(testdf)
print("Prediction: \n", y_pred)
perf = predictor.evaluate_predictions(y_true=y_test, y_pred=y_pred)

# extra analysis using fit_summary and feature_importance
summary = predictor.fit_summary()
print('___________________________________')
print(summary)
feature_importance = predictor.feature_importance(traindf)
print('___________________________________')
print(feature_importance)
print('___________________________________')
