import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

class QuarterlyPicker:
    def __init__(self):
        # tickers whose growth 10% for 10 years
        self.qualified_ticker_list = []
        self.growth_annual_path = './nasdaq-100/growth/annual/'
        self.growth_quarterly_path = './nasdaq-100/growth/quarterly/'

    def read_one_file(self, path, file):
        # exclude non csv files
        if not ('.xlsx' in file):
            print("Not a xlsx file. ", file)
            return
        print(file)
        df = pd.read_excel(path + file)
        print(df.loc['Gross Profit Growth'])






if __name__ == '__main__':
    qp = QuarterlyPicker()
    qp.read_one_file(qp.growth_quarterly_path, 'AAL.xlsx')
