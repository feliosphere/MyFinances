from LoanPaymentPlan import LoanPaymentPlan

def main():
    paymentPlan = LoanPaymentPlan('./creditbalancesflat.json')
    paymentPlan.setMonthlyPayments()
    done = False

    while not done:
        userInput = input('Enter a date (YYYY-MM) to se the payment information. Enter \'done\' to end the session:  ')
        if userInput == 'done':
            done = True
            print('Bye!')
        else:
            print('Breakdown of payments for month {}:'.format(userInput))
            print(paymentPlan.getBreakDownMonthlyPayment(userInput))
            print('\n---------\n')
            print('This month you will pay a total of ${} \n'.format(paymentPlan.getMonthPayment(userInput)))





if __name__ == "__main__":
    main()