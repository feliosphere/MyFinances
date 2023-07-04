# import pandas as pd
import json

# df = pd.read_json('creditbalances.json')

# print(df)[]
# someDict = {'s1':[{'sub11':1,'sub12':2},{'sub13':3,'sub14':4}],'s2':[{'sub21':5,'sub22':6},{'sub23':7,'sub24':8}]}
# print(someDict)
f = open('creditbalances.json')

creditCardLoans = json.load(f)
print(creditCardLoans)
creditCards = ['Amex', 'Discover', 'ChaseSapphire','MicroCenter']
loansBalances = {}
# print()
for card in creditCardLoans:
    # print(card,creditCardLoans[card])
    for loan in creditCardLoans[card]:
        print(loan['id'])

        #Loan fee: add to balance of loan or total credit card balance to be paid on first month?
        loanFee = loan['balance'] * loan['loanFee']/100
        print(loanFee)

        #Calculate months (set as function later and check a better way using day and when cycle closes)
        requestYear = int(loan['submittedDate']/10000)
        requestMonth = int((loan['submittedDate']-requestYear*10000)/100)
        requestDay = int(loan['submittedDate']-requestYear*10000-requestMonth*100)
        dueYear = int(loan['dueDate']/10000)
        dueMonth = int((loan['dueDate']-dueYear*10000)/100) - 1
        dueDay = int(loan['dueDate']-dueYear*10000-dueMonth*100)
        monthsToPay = (dueYear-requestYear)*12 + (dueMonth-requestMonth)
        print(dueYear,requestYear,dueMonth,requestMonth)
        print(monthsToPay)

        #Assume same interest apply to originator fee (change later if different)
        totalLoanDue = loan['balance']+loanFee
        #Append to dict
        # loansBalances[]

f.close