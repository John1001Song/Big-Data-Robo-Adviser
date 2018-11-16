import pandas as pd
import numpy as np
import arff2pandas as a2p
import os
import arff
import math

feature_list = [#"Ticker",
                #"Qualified ticker",
                "Gross Profit Growth",
                "EBIT Growth",
                "Net Income Growth",
                "EPS Growth",
                "EPS Diluted Growth",
                "Weighted Average Shares Diluted Growth",
                "Operating CF Growth",
                "Asset Growth",
                "Book Value per Share Growth",
                "Debt Growth",
                "Receivables growth",
                "Inventory Growth",
                "Dividends per Share Growth",
                "FCF Growth",
                "R&D Expense Growth",
                "SG&A Expenses Growth",
                "Operating Income Growth",
                "Weighted Average Shares Growth"]

full_feature_list = [#"Ticker",
                "Qualified ticker",
                "Gross Profit Growth",
                "EBIT Growth",
                "Net Income Growth",
                "EPS Growth",
                "EPS Diluted Growth",
                "Weighted Average Shares Diluted Growth",
                "Operating CF Growth",
                "Asset Growth",
                "Book Value per Share Growth",
                "Debt Growth",
                "Receivables growth",
                "Inventory Growth",
                "Dividends per Share Growth",
                "FCF Growth",
                "R&D Expense Growth",
                "SG&A Expenses Growth",
                "Operating Income Growth",
                "Weighted Average Shares Growth"]

arff_attribute_list = [
                  ("Qualified ticker", 'INTEGER'),
                  ("Gross Profit Growth", 'REAL'),
                  ("EBIT Growth", 'REAL'),
                  ("Net Income Growth", 'REAL'),
                  ("EPS Growth", 'REAL'),
                  ("EPS Diluted Growth", 'REAL'),
                  ("Weighted Average Shares Diluted Growth", 'REAL'),
                  ("Operating CF Growth", 'REAL'),
                  ("Asset Growth", 'REAL'),
                  ("Book Value per Share Growth", 'REAL'),
                  ("Debt Growth", 'REAL'),
                  ("Receivables growth", 'REAL'),
                  ("Inventory Growth", 'REAL'),
                  ("Dividends per Share Growth", 'REAL'),
                  ("FCF Growth", 'REAL'),
                  ("R&D Expense Growth", 'REAL'),
                  ("SG&A Expenses Growth", 'REAL'),
                  ("Operating Income Growth", 'REAL'),
                  ("Weighted Average Shares Growth", 'REAL')]


def get_qualified_list(path):
    df = pd.read_csv(path)
    t_list = list()
    for ticker in df['ticker']:
        t_list.append(ticker)
    return t_list


def read_one_company(path, ticker, qualified_list, all_company_result, full_attributes):
    print(f"working on {ticker}")
    df = pd.read_excel(path)
    if df.empty:
        return

    # ====================
    feature_value_list = list()
    # init the list
    for i in range(len(full_attributes)):
        feature_value_list.append(0.0)

    # based on the feature list index, update the array or list value
    # pass the feature list as a parameter, so when the feature list changes, this function will automatically change
    # ====================

    # use features to check what features are left
    feature_checker = list()
    for ele in feature_list:
        feature_checker.append(ele)

    qualified_ticker_index = full_attributes.index("Qualified ticker")

    if ticker in qualified_list:
        feature_value_list[qualified_ticker_index] = 1
    else:
        feature_value_list[qualified_ticker_index] = 0

    for ele in feature_list:
        try:
            ele_index = full_attributes.index(ele)
            row_content = df.loc[ele]
            feature_value_list[ele_index] = sum(row_content) / len(row_content)
        except Exception as ex:
            print(ex)
            feature_value_list[ele_index] = 0

    test_list = list()
    for x in feature_value_list:
        if type(x) == str:
            test_list.append(x)
        else:
            if math.isnan(x):
                test_list.append(0)
            else:
                test_list.append(x)

    all_company_result.append(test_list)


def run(dataset_path):
    arff_res = dict()
    arff_res["description"] = "company dataset"
    arff_res["relation"] = "company"
    arff_res["attributes"] = arff_attribute_list
    all_company_result = list()

    qualified_list = get_qualified_list('qualified_tickers.csv')
    # read each file and get the avg value for each factor
    # the avg values are in a dict and appended to the list
    [read_one_company(dataset_path + fname, fname, qualified_list, all_company_result, full_feature_list) for fname in
     os.listdir(dataset_path) if fname.endswith('.xlsx')]

    arff_res['data'] = all_company_result
    print(arff_res)
    arff.dump('test.arff', arff_res['data'], 'company', None)


if __name__ == '__main__':
    run('../datasets/NASDAQ/financial_statement/growth/annual/')
