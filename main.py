import pandas as pd
import numpy as np

def MonthsToPay(dueDate, requestDate):
    return 12*(dueDate.dt.year-requestDate.dt.year)+(dueDate.dt.month-requestDate.dt.month)-1

def TotalPayment(months, total, apr):
    total *= ((1+apr/1200)**months)
    return total

df = pd.read_json('creditbalancesflat.json')

df['submittedDate'] = pd.to_datetime(df['submittedDate'], format='%Y%m%d')
df['dueDate'] = pd.to_datetime(df['dueDate'], format='%Y%m%d')
df['totalLoanDue']  = (df['loanFee']*df['balance']/100+df['balance'])

df['monthsToPay'] = MonthsToPay(df['dueDate'],df['submittedDate'])

firstMonth = df['submittedDate'].min()
lastMonth = df['dueDate'].max()

df['totalPayment'] = TotalPayment(df['monthsToPay'],df['totalLoanDue'],df['apr'])

for single_date in pd.date_range(start=firstMonth, end=lastMonth,freq='MS'):

    conditions = [(df['submittedDate'] > single_date),
                  (df['submittedDate'] < single_date) & (single_date <= df['dueDate']),
                  (df['submittedDate'] > single_date) | (single_date >= df['dueDate'])]
    values = [0,df['totalPayment']/df['monthsToPay'],'paid']
                  
    df[single_date.strftime('%Y-%m')] = np.select(conditions,values) 

print(df)
print(df['totalPayment'])