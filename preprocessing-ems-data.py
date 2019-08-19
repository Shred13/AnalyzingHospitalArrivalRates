import pandas as pd
import numpy as np
from PythonWork import export_to_csv

from _datetime import datetime
from matplotlib import pyplot as plt


def isLeap(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

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

# data["FIRST_HOSP_ARRIVAL_DATETIME"] = pd.to_datetime(data.FIRST_HOSP_ARRIVAL_DATETIME)


def returnday(date):
    return date.weekday()


def return_percent_of_year(date):
    if isLeap(date.year):
        return date.timetuple().tm_yday / 366
    else:
        return date.timetuple().tm_yday / 365


# data['weekday'] = data['FIRST_HOSP_ARRIVAL_DATETIME'].apply(lambda x: returnday(x))

# data['percent_of_year'] = data['FIRST_HOSP_ARRIVAL_DATETIME'].apply(lambda x: return_percent_of_year(x))
#
# data = data.sort_values(by=['FIRST_HOSP_ARRIVAL_DATETIME'])


count = 0
less_than_thirty = True


def arrival_rate(date):
    time = date.time().minute
    global less_than_thirty
    global count
    if time < 30 and less_than_thirty is True:
        count += 1
        return count
    elif time >= 30 and less_than_thirty is True:
        less_than_thirty = False
        count = 1
        return count
    elif time >= 30 and less_than_thirty is False:
        count += 1
        return count
    elif time < 30 and less_than_thirty is False:
        less_than_thirty = True
        count = 1
        return count


# data['how_many_come_in'] = data["FIRST_HOSP_ARRIVAL_DATETIME"].apply(lambda x: arrival_rate(x))


# data = pd.read_csv('ems-data.csv')

row_count = 0


def bucket_creation(value):
    global row_count
    if row_count + 1 == len(data.how_many_come_in):
        return value
    elif row_count is 0:
        row_count += 1
        return np.nan
    elif value > data.how_many_come_in[row_count + 1]:
        row_count += 1
        print(row_count / 5990574)
        return value
    elif value < data.how_many_come_in[row_count + 1]:
        row_count += 1
        return np.nan


# data['arrival_per_30_mins'] = data['how_many_come_in'].apply(lambda x: bucket_creation(x))

# data.drop(columns='how_many_come_in', inplace=True)
# data.dropna(subset=['arrival_per_30_mins'], inplace=True)


# data.FIRST_HOSP_ARRIVAL_DATETIME = pd.to_datetime(data.FIRST_HOSP_ARRIVAL_DATETIME, format='%Y-%m-%dT%H:%M:%S')

# data.drop(columns="FIRST_HOSP_ARRIVAL_DATETIME", inplace=True)

# data.drop(0, inplace=True)


data = pd.read_csv("ems-data.csv")
data.FIRST_HOSP_ARRIVAL_DATETIME = pd.to_datetime(data.FIRST_HOSP_ARRIVAL_DATETIME, format='%Y-%m-%dT%H:%M:%S')

data['FIRST_HOSP_ARRIVAL_DATETIME'] = data['FIRST_HOSP_ARRIVAL_DATETIME'].dt.round('15min')

export_to_csv.export(data, "ems-data-30-mins-datetime.csv")

# string does not work because lack of year

# data = pd.read_csv('ems-data-30-mins-datetime.csv')
plt.plot(data['FIRST_HOSP_ARRIVAL_DATETIME'][:672], data['arrival_per_30_mins'][:672])
plt.show()
