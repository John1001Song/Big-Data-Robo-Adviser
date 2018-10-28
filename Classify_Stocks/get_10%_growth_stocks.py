import os
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
        self.growth_annual_path = '../NASDAQ-100/growth/annual/'
        self.growth_quarterly_path = '../NASDAQ-100/growth/quarterly/'

    def read_one_file(self, path, file):
        # exclude non csv files
        if not '.xlsx' in file:
            print("Not a xlsx file. ", file)
            return
        print('reading file: ', file)
        df = pd.read_excel(path + file)
        return df

    def factorCheck(self, df, row_name, avg_growth_bar, all_postive_bar, each_period_growth_bar):
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
                print('avg growth bar is ', avg_growth_bar)
                return False

            for index, value in factor.items():
                # print('index: ', index, ' value: ', value)
                # check all positive growth
                if all_postive_bar:
                    if value < 0:
                        print('Negative growth found at ', index, ' value: ', value)
                        return False
                # check greater than the bar at each time
                if value < each_period_growth_bar:
                    print('Fails to be greater than each_period_growth_bar value: ', each_period_growth_bar)
                    print('At ', index, 'value: ', value, '\n')
                    return False

        except Exception:
            print("This factor may not processed.")
            return False

        # pass all bars, return true
        return True




if __name__ == '__main__':
    qp = QuarterlyPicker()
    df = qp.read_one_file(qp.growth_annual_path, 'AAL.xlsx')
    qp.factorCheck(df, 'Operating CF Growth', 0.1, False, 0.1)