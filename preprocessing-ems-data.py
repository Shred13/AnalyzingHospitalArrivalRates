import pandas as pd
from PythonWork import export_to_csv

from _datetime import datetime

# All of the following commented out code is to show all the preprocessing steps I went through
# data = pd.read_csv('ems-incident-dispatch-data.csv')
# # data is now a pandas dataframe
#
# # data.drop(columns='BOROUGH',  inplace=True)
# went from ~1.84gb to 234 mb
# cols_to_keep = ['FIRST_HOSP_ARRIVAL_DATETIME', 'BOROUGH']
# data = data[cols_to_keep]
# prints what day of the week it is, with 0 = Monday and 6 = Sunday


# data.dropna(subset=['FIRST_HOSP_ARRIVAL_DATETIME'], inplace=True)
# # before dropping the null data, 8557848 rows
# # after dropping: 5990574 rows
# # now only 164.60 mb big

# data.FIRST_HOSP_ARRIVAL_DATETIME = pd.to_datetime(data.FIRST_HOSP_ARRIVAL_DATETIME, format='%Y-%m-%dT%H:%M:%S')

data = pd.read_csv('ems-data-4.0.csv')
data["FIRST_HOSP_ARRIVAL_DATETIME"] = pd.to_datetime(data.FIRST_HOSP_ARRIVAL_DATETIME)
# print(data)
# a = data.at[1, 'FIRST_HOSP_ARRIVAL_DATETIME']


def returnday(date):
    return date.weekday()


data['weekday'] = data['FIRST_HOSP_ARRIVAL_DATETIME'].apply(lambda x: returnday(x))

export_to_csv.export(data, "final-ems-data.csv")

