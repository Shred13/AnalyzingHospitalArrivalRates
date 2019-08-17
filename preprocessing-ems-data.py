import pandas as pd
from PythonWork import export_to_csv

from _datetime import datetime


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
        return date.timetuple().tm_yday/366
    else:
        return date.timetuple().tm_yday/365


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


data = pd.read_csv('ems-data.csv')

data['how_many_come_in'] = data["FIRST_HOSP_ARRIVAL_DATETIME"].apply(lambda x: arrival_rate(x))

export_to_csv.export(data, "final_process")