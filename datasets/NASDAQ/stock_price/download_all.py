from pandas_datareader import data as pdr
import pandas as pd
import fix_yahoo_finance as yf

yf.pdr_override() # <== that's all it takes :-)

nasdaq_company_info = pd.read_csv('NASDAQ_companylist.csv', usecols=["Symbol"])
name_list = nasdaq_company_info['Symbol']

# print(len(name_list.index))

for index in range(0, len(name_list.index)-1):
	curName = name_list[index]
	print("company ", index,": ", curName)
	cur_file_name = curName + ".csv"
	try:
		data = pdr.get_data_yahoo(curName, start="2008-09-12", end="2018-09-12")
		df = pd.DataFrame(data = data)
		df.to_csv(cur_file_name)
	except Exception as e:
		pass
	
	

# download dataframe
# data = pdr.get_data_yahoo("ZYNE", start="2008-09-12", end="2018-09-12")

# download Panel
# data = pdr.get_data_yahoo(["SPY", "IWM"], start="2017-01-01", end="2017-04-30")

# print(data)

# data = yf.download("YI", start="2008-09-12", end="2018-09-12")
# cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
# data.reindex(columns=cols)

# print(data)
# df = pd.DataFrame(data = data)

# print(df)

# df.to_csv("ZYNE.csv")

