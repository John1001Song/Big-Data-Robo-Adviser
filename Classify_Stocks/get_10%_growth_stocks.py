import os
from os.path import isfile, join
from os import listdir
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# caution: 在判别个股的成长性方面，
# 主要有三个指标：一是EPS增长率，二是PEG，三是销售收入增长率，
# 这是检验个股有无成长性的试金石，也是一般机构衡量个股成长性方面的三大核心指标。
class QuarterlyPicker:
    def __init__(self):
        # tickers whose growth 10% for 10 years
        self.qualified_ticker_list = []
        self.growth_annual_path = '../datasets/NASDAQ/financial_statement/growth/annual/'
        self.growth_quarterly_path = '../datasets/NASDAQ/financial_statement/growth/quarterly/'

    def get_all_file_name(self, file_path, file_format):
        # get all files names
        files_names = [f for f in listdir(file_path) if isfile(join(file_path, f))]
        name_array = []

        for name in files_names:
            if file_format in name:
                name_array.append(name)

        return name_array

    def read_one_file(self, path, file):
        # exclude non csv files
        if not '.xlsx' in file:
            # print("Not a xlsx file. ", file)
            return
        print('reading file: ', file, '\n')
        try:
            df = pd.read_excel(path + file)
        except:
            print(f"can't read {file}")
            return None
        return df

    def checkFector(self, df, row_name, avg_growth_bar, all_postive_bar, each_period_growth_bar):
        """
        Check wanted data by the given factor, which is one of the row names.

        :param df: one company financial information in dataframe
        :param row_name: row (factor) name in the dataframe, which represents the wanted data
        :param avg_growth_bar: min average growth requirements for the growth.
        :param all_postive_bar: true -> all values must be positive, false -> does not have to be all positive growth.
        :param each_period_growth_bar: min growth requirement for each of the unit time,
                like, each annual or quarterly growth cannot be lower than the each_period_growth.
        :return: false if fails any of the requirements, true if satisfy all requirements
        """

        try:
            factor = df.loc[row_name]
            print('factor is: ', row_name)

            # check avg growth
            avg_growth = factor.mean()
            if avg_growth < avg_growth_bar:
                print('Lower than avg growth bar value, will return false.')
                print(row_name, ' avg growth is ', avg_growth)
                print('avg growth bar is ', avg_growth_bar, '\n')
                return False

            for index, value in factor.items():
                # print('index: ', index, ' value: ', value)
                # check all positive growth
                if all_postive_bar:
                    if value < 0:
                        print('Negative growth found at ', index, ' value: ', value, '\n')
                        return False
                # check greater than the bar at each time
                if value < each_period_growth_bar:
                    print('Fails to be greater than each_period_growth_bar value: ', each_period_growth_bar)
                    print('At ', index, 'value: ', value, '\n')
                    return False

        except Exception:
            print("This factor may not processed.\n")
            return False

        # pass all bars, return true
        return True

    def checkCoreFactors(self, df, factor_one, factor_two, factor_three):
        """
        Check three core factors. Default factors are EPS Growth, Operating Income Growth, Operating CF Growth.
        Traditionally, should check core three factors: EPS Growth, PEG, Operating Income Growth,
        but PEG is not available in the dataset. I choose to use simple factors.
        Later try FCF Growth and PEG.

        :param df: company financial data in dataframe
        :param factor_one: EPS Growth
        :param factor_two: Operating Income Growth
        :param factor_three: Operating CF Growth
        :return: True if pass all three checks, else False
        """
        # 0.10: expect in high EPS growth
        # True: try high standard bar
        # 0.03: expect EPS growth greater than saving money in banks
        eps_result = self.checkFector(df, factor_one, 0.05, False, -0.1)

        # 0.1: expect total big growth
        # True: expect the company always has a positive trend
        # 0.05: expect each year growth
        op_income_result = self.checkFector(df, factor_two, 0.1, False, -0.1)

        # 0.1: expect total boost in cash growth
        # True: expect the company always has a positive trend
        # 0.05: expect each year has a healthy cash flow growth
        op_cf_result = self.checkFector(df, factor_three, 0.1, False, -0.1)

        if eps_result and op_income_result and op_cf_result:
            return True
        else:
            return False

    def start(self):
        # get all file names
        ticker_list = self.get_all_file_name(self.growth_annual_path, '.xlsx')
        result_list = list()

        for ticker in ticker_list:
            df = self.read_one_file(self.growth_annual_path, ticker)
            if not df.empty and df is not None:
                # Check three core factors. Default factors are EPS Growth, Operating Income Growth, Operating CF Growth.
                if self.checkCoreFactors(df, 'EPS Growth', 'Operating Income Growth', 'Operating CF Growth'):
                    print('Company satisfies three default core factors: ', ticker, '\n')
                    result_list.append(ticker)
        print("here is the qualified tickers: ", result_list)
        res = pd.DataFrame(result_list, columns=['ticker'])
        res.to_csv('qualified_tickers.csv', index=False)

if __name__ == '__main__':
    qp = QuarterlyPicker()
    qp.start()