#import modules
from itertools import product
import pandas as pd

#calculate the number of months in x years
def years_to_months(year):
    return year*12

#divide annual interest rate by number of months in year
def monthy_interest_rate(rate):
    return rate/12

#calculate the monthly repayment including interest for an annual rate
def monthly_payment(principal, year_term, annual_interest_rate):

    '''
    formula: (r(1+r)**n)/(((1+r)**n)-1)
    r = monthly interest rate (annual rate/12)
    n = duration of the mortgage in months
    '''
    
    monthly_interest_rate = monthy_interest_rate(annual_interest_rate)
    repayment_months = years_to_months(year_term)
    term_adjusted_interest_rate = ((1+monthly_interest_rate)**repayment_months)
    numerator = monthly_interest_rate * term_adjusted_interest_rate
    denominator = term_adjusted_interest_rate - 1
   
    return round(principal * (numerator/denominator), 2)
 
#calculate the total cost of credit for the mortgage with an annual rate
def cost_of_credit(principal, year_term, annual_interest_rate):

    adjusted_rate = monthy_interest_rate(annual_interest_rate)
    monthly_repayment = monthly_payment(principal, year_term, annual_interest_rate)
    
    accrued_interest = 0
    balance = principal

    while balance > 0:
       
        monthly_interest = round(balance * adjusted_rate, 2)
        accrued_interest += monthly_interest
        balance = round(balance - (monthly_repayment - monthly_interest), 2)

    return accrued_interest

if __name__ == '__main__':

    ##test uses##
    
    #monthly_payment(400000, 20, 0.0365)
    #cost_of_credit(400000, 20, 0.0365)

    #import df from excel/csv
    #df = pd.read_excel(<path and file>.csv', sheet_name= 'name', header = 0)
    #df = pd.read_csv('<path and file>.csv')

    #test data 
    deposit = 200000
    price_list = [300000, 350000, 400000, 450000, 500000, 
                  550000, 600000, 650000, 700000, 750000,
                  800000, 850000]
    mortgage_list = [price - 200000 for price in price_list]
    term_list = [5,10, 15, 20, 25, 30, 35]
    interest_list = [0.035, 0.0365, 0.038, 0.0385, 0.04, 0.042, 0.044, 0.045, 
                     0.037, 0.0405, 0.048, 0.041, 0.034, 0.0375, 0.033, 0.0455,
                     0.0465, 0.0475, 0.0485, 0.0505, 0.0515, 0.0435, 0.0415, 
                     0.0445, 0.0425, 0.0465, 0.062, 0.0625, 0.0605, 0.0655,
                     0.0705, 0.0715, 0.058, 0.0555, 0.035, 0.0365, 0.038,
                     0.0385, 0.04, 0.042, 0.044, 0.045, 0.037, 0.0405]

    #create every combination of principal, rate term
    combos = list(product(mortgage_list, term_list, interest_list))

    df = pd.DataFrame(combos, columns =['Mortgage', 'Term', 'Interest'])

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    #apply functions to every row of the dataset creating a new column for each function
    df['Monthly_Repayment'] = df.apply(lambda row: monthly_payment(row['Mortgage'], row['Term'], row['Interest']), axis = 1)
    df['Cost_of_Credit'] = df.apply(lambda row: cost_of_credit(row['Mortgage'], row['Term'], row['Interest']), axis = 1)


    #export to excel/csv/
    #df.to_excel(r'Path of excel\File Name.xlsx', sheet_name='Mortgage Cost', index=False)
    #df.to_csv(r'Path of excel\File Name.xlsx', sheet_name='Mortgage Cost', index=False)
