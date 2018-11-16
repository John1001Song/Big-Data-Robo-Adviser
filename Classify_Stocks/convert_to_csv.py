import pandas as pd

df = pd.read_excel('../datasets/NASDAQ/financial_statement/growth/annual/AABA.xlsx')

df.to_csv('test.csv')

df = pd.read_csv('test.csv')

print(df)