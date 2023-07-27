# import os
# from flask import Flask
from LoanPaymentPlan import LoanPaymentPlan

# application = Flask(__name__)

# @application.route('/')
def main():   
    paymentPlan = LoanPaymentPlan('../data/creditbalancesflat.json')
    paymentPlan.setMonthlyPayments()
    done = False
   
    # return paymentPlan.getBreakDownMonthlyPayment('2024-07')

    while not done:
        
        userInput = input('Enter a date (YYYY-MM) to se the payment information. Enter \'done\' to end the session:  ')
        if userInput == 'done':
            done = True
            print('Bye!')
        else:
            print('\nBreakdown of payments for month {}:\n'.format(userInput))
            print(paymentPlan.getBreakDownMonthlyPayment(userInput))
            print('\n---------\n')
            print('The end of the month balances are:\n')
            print(paymentPlan.getEndOfMonthBalances(userInput))
            print('\n---------\n')
            print('This month you will pay a total of ${} \n'.format(paymentPlan.getMonthPayment(userInput)))
            print('\n---------\n')
            # print(paymentPlan.creditors)
    # return "Hia2"

if __name__ == "__main__":
    # application.run()
    main()