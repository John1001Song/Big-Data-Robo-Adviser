import requests
import json
import urllib3
from bs4 import BeautifulSoup
import os
import re
from urllib.request import Request
from urllib.request import urlopen
from urllib import parse
import pandas as pd


def get_company_financial_statement_page(company, raw_url):
    url = raw_url.format(company)
    # page = BeautifulSoup(requests.get(url).content, 'html.parser')
    company_name_csv = "{}.csv".format(company)
    file = requests.get(url, allow_redirects=True)
    open(company_name_csv, 'wb').write(file.content)

    return

def download_income_sheet(raw_url):
    # https: // stockrow.com / api / companies / GOOGL / financials.xlsx?dimension = MRQ & section = Income
    # Statement & sort = desc
    pass

def download_balance_sheet(raw_url):
    # https: // stockrow.com / api / companies / GOOGL / financials.xlsx?dimension = MRQ & section = Balance
    # Sheet & sort = desc
    pass

def download_cash_flow_sheet(raw_url):
    # https: // stockrow.com / api / companies / GOOGL / financials.xlsx?dimension = MRQ & section = Cash
    # Flow & sort = desc
    pass

def download_metrics_sheet(raw_url):
    # https: // stockrow.com / api / companies / GOOGL / financials.xlsx?dimension = MRQ & section = Metrics & sort = desc
    pass

def download_growth_sheet(ticker):
    # two variables ticker, time_period
    raw_url = "https://stockrow.com/api/companies/{}/financials.xlsx?dimension={}&section=Growth&sort=desc"

    quarterly_url = raw_url.format(ticker, 'MRQ')
    annual_url = raw_url.format(ticker, 'MRY')

    q_req = Request(quarterly_url)
    a_req = Request(annual_url)
    q_req.add_header("User-Agent","Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36")
    a_req.add_header("User-Agent","Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36")

    file_name = "%s.xlsx"%(ticker)
    quarterly_path = "./financial_statements/growth/quarterly/%s"%(file_name)
    annual_path = "./financial_statements/growth/annual/%s"%(file_name)

    # download quarterly growth
    response = urlopen(q_req)
    file = response.read()

    with open(quarterly_path, 'wb') as q_f:
        q_f.write(file)
        print("save quarterly growth: %s"%(file_name))

    # download annual growth
    response = urlopen(a_req)
    file = response.read()

    with open(annual_path, 'wb') as a_f:
        a_f.write(file)
        print("save annual growth: %s"%(file_name))

def download_company_quarterly_statements(company_ticket, raw_url):
    url_without_sheet_type = raw_url.format(company_ticket)
    print(url_without_sheet_type)
    download_growth_sheet(url_without_sheet_type)
    pass

def download_company_annual_statements(company_ticket, raw_url):
    pass

def download_all(name_list):
    # nasdaq_company_info = pd.read_csv('NASDAQ_companylist.csv', usecols=["Symbol"])
    # name_list = nasdaq_company_info['Symbol']
    # print(name_list)

    for ticker in name_list:
        download_growth_sheet(ticker)

if __name__ == '__main__':

    # download_growth_sheet('GOOGL')

    nasdaq_100_name_list = ['ATVI', 'ADBE', 'ALXN', 'ALGN', 'GOOGL', 'GOOG', 'AMZN', 'AAL', 'AMGN', 'ADI', 'AAPL', 'AMAT', 'ASML', 'ADSK', 'ADP', 'BIDU', 'BIIB', 'BMRN', 'BKNG', 'AVGO', 'CA', 'CDNS', 'CELG', 'CHTR', 'CHKP', 'CTAS', 'CSCO', 'CTXS', 'CTSH', 'CMCSA', 'COST', 'CSX', 'CTRP', 'XRAY', 'DLTR', 'EBAY', 'EA', 'EXPE', 'ESRX', 'FB', 'FAST', 'FISV', 'GILD', 'HAS', 'HSIC', 'HOLX', 'IDXX', 'ILMN', 'INCY', 'INTC', 'INTU', 'ISRG', 'JBHT', 'JD', 'KLAC', 'LRCX', 'LBTYA', 'LBTYK', 'MAR', 'MXIM', 'MELI', 'MCHP', 'MU', 'MSFT', 'MDLZ', 'MNST', 'MYL', 'NTES', 'NFLX', 'NVDA', 'ORLY', 'PCAR', 'PAYX', 'PYPL', 'PEP', 'QCOM', 'QRTEA', 'REGN', 'ROST', 'STX', 'SHPG', 'SIRI', 'SWKS', 'SBUX', 'SYMC', 'SNPS', 'TMUS', 'TTWO', 'TSLA', 'TXN', 'KHC', 'FOXA', 'FOX', 'ULTA', 'VRSK', 'VRTX', 'VOD', 'WBA', 'WDC', 'WDAY', 'WYNN', 'XLNX']
    download_all(nasdaq_100_name_list)


# company -> annual -> growth
#                   -> metrics
#                   -> income
#                   -> balance
#                   -> cash_flow

# company -> quarterly -> growth
#                      -> metrics
#                      -> income
#                      -> balance
#                      -> cash_flow