import pandas as pd
import numpy as np

class LoanPaymentPlan:
    def __init__(self, loanJsonPath) -> None:
        self.dfLoans = pd.read_json(loanJsonPath)

        self.dfLoans['submittedDate'] = pd.to_datetime(self.dfLoans['submittedDate'], format='%Y%m%d')
        self.dfLoans['dueDate'] = pd.to_datetime(self.dfLoans['dueDate'], format='%Y%m%d')
        self.dfLoans['totalLoanDue']  = (self.dfLoans['loanFee']*self.dfLoans['balance']/100+self.dfLoans['balance'])
        self.dfLoans['monthsToPay'] = self.MonthsToPay(self.dfLoans['dueDate'],self.dfLoans['submittedDate'])
        self.dfLoans['totalPayment'] = self.TotalPayment(self.dfLoans['monthsToPay'],self.dfLoans['totalLoanDue'],self.dfLoans['apr'])
        
        self.firstMonth = self.dfLoans['submittedDate'].min()
        self.lastMonth = self.dfLoans['dueDate'].max()   

        self.payOnDate = {}
        self.creditors = self.dfLoans['creditCard'].unique()

    def getFirstMonth(self):
        return self.firstMonth
    
    def getLastMonth(self):
        return self.lastMonth
    
    def getLoansDataFrame(self):
        return self.dfLoans
    
    def setMonthlyPayments(self):
        prevMonthBalance =  self.dfLoans['totalLoanDue']
        for single_date in pd.date_range(start=self.firstMonth, end=self.lastMonth,freq='MS'):
            dateMonth =single_date.strftime('%Y-%m')
            conditions = [(self.dfLoans['submittedDate'] > single_date),
                          (self.dfLoans['submittedDate'] < single_date) & (single_date <= self.dfLoans['dueDate']),
                          (self.dfLoans['submittedDate'] > single_date) | (single_date >= self.dfLoans['dueDate'])]
            values = [0,self.dfLoans['totalPayment']/self.dfLoans['monthsToPay'],0]
                    
            self.dfLoans[dateMonth] = np.select(conditions,values)

            self.dfLoans[dateMonth+"_RemainderBalance"] = prevMonthBalance - self.dfLoans[dateMonth]
            prevMonthBalance = self.dfLoans[dateMonth+"_RemainderBalance"]

            self.payOnDate[dateMonth] = self.dfLoans[single_date.strftime('%Y-%m')].sum()
        # self.dfLoans

    def MonthsToPay(self, dueDate, requestDate):
        return 12*(dueDate.dt.year-requestDate.dt.year)+(dueDate.dt.month-requestDate.dt.month)-1

    def TotalPayment(self, months, total, apr):
        total *= ((1+apr/1200)**months)
        return total
    

    def getMonthPayment(self, date):
        #TODO check for data format validation
        if date in self.payOnDate.keys():
            return self.payOnDate[date]
        else:
            raise Exception("Date provided don't exist")
    
    def getBreakDownMonthlyPayment(self, date):
        #TODO check for data format validation and date exist
        return self.dfLoans.groupby('creditCard').agg({date: 'sum'})
    
    def getEndOfMonthBalances(self, date):
        return self.dfLoans.groupby('creditCard').agg({date+"_RemainderBalance": 'sum'})
        