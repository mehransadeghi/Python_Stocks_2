class Tickers:
'''
This class must:
	– Have a function, say save tickers that fetches the first n valid tickers from the URL 1 and writes the
	tickers in a file, say tickers.txt.
	– To ensure that a ticker is valid, you should use the iex-api-python to verify that the price function
	for the Stock corresponding to the fetched ticker works. That is, if there are some tickers for which the
	price() function of the iex API does not work, then that ticker should not be written to the file.
	– Write one ticker symbol per line of the file tickers.txt. The number n will be provided to the driver
	as an optional argument and will be at most 110.
	– The class must have a method for initialization of its objects and any other methods you feel are
	necessary.
'''


	def pull110ItemsURL(self):
	    # Set up Chrome instance of this url
	    driver = webdriver.Chrome(executable_path='./chromedriver')
	    driver.get('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQrender=download')

	    # Click on the 150 option in page size select so we can get all the symbols we need
	    page_size_select = driver.find_element_by_id('main_content_lstpagesize')
	    for page_size_option in page_size_select.find_elements_by_tag_name('option'):
	        if page_size_option.text == '150 Items Per Page':
	            page_size_option.click()
	            break

	    return driver.current_url



	def save_tickers(self, n, url, file_name):
		if int(n) > 110:
        	raise Exception("You need to give me a number less than or equal to 150!")

	    # Create request with 150 item url
	    request = requests.get(url=pull110ItemsURL())
	    parser = PyQuery(request.text)
	    table = parser("#CompanylistResults")

	    table_parser = PyQuery(table)
	    symbols = table_parser("h3")
	    symbol_list = [symbol for symbol in symbols.text().split()]

	    for i, ticker in enumerate(symbol_list):
	        try:
	            if i <= int(n):
	                Stock(symbol=ticker).price()
	            else:
	                break
	        except:
	            symbol_list.remove(ticker)

	    f = open(filename, "w")
	    for i, symbol in enumerate(symbol_list):
	        if i <= int(n):
	            f.write(symbol + '\n')
	        else:
	            break

	    f.close()


	def __init__(self):
		pass
		#TODO: How to write appropriate inits?
		
import sys
import csv
import datetime
import time
from iex import Stock

class Fetcher:




	def write_to_file(self, ticker, info_writer, endTime):
	    currentDT = datetime.datetime.now()
	    hour = str(currentDT.hour)
	    minute = currentDT.minute
	    if minute < 10:
	        minute = '0' + str(minute)
	    else:
	        minute = str(minute)

	    # If function exceeds its endTime then exit the module
	    if currentDT >= endTime:
	        return

	    ticker_info = Stock(symbol=ticker).quote()
	    info_writer.writerow([hour + ':' + minute, ticker, ticker_info['low'], ticker_info['high'], ticker_info['open'],
	                          ticker_info['close'], ticker_info['latestPrice'], ticker_info['latestVolume']])


	def fetch_all_data(self, time_lim, ticker_file, csv_file):
	    open_csv = open(csv_file, 'a')
	    info_writer = csv.writer(open_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	    while True:
	        fp = open(ticker_file)
	        # Calculate time to sleep until next minute starts
	        sleepTime = 60 - (datetime.datetime.now().second + datetime.datetime.now().microsecond / 1000000.0)
	        time.sleep(sleepTime)

	        # Calculate how long the function should run
	        endTime = datetime.datetime.now() + datetime.timedelta(seconds=int(time_lim))
	        for ticker in fp:
	            writeToFile(ticker=ticker.strip('\n'), info_writer=info_writer, endTime=endTime)
	        fp.close()


	def update_ticker(self, ticker):
		pass
	def __init__(self):
		pass


'''
	– Read all the tickers from an input file (tickers.txt) or use some function of the Tickers class to fetch
	the tickers.
	– Define a function that updates the current stock information for the ticker that is passed as an argument.
	The information is updated in an information database (say stocks now.db for example). The name of
	the table will be StockData. Use sqlite3 database.
	– There should be another function, say fetch all data() of the class that calls the above function for each
	input ticker.
	– The fetch all data() function should run for specified time period, say time lim in seconds and update
	the data in the database table.
	– For each ticker in the tickers.txt file, the database table, should have one row for each minute.
	– The Time column should contain time in the HH:MM format with HH ranging from 00 to 23. There
	should be one and only one row corresponding to a specific value of Time and Ticker.
	– In order to extract the stock information for a ticker, say ”AAPL”, you should use the iex-api-python
	which is described here: https://pypi.org/project/iex-api-python/. You need to fetch the current data for the following fields: low, high, open, close, latestPrice, latestVolume. Use the
	quote() function of the Stock corresponding to the ticker.
	– The table must have following columns:
	Time, Ticker, latestPrice, latestVolume, Close, Open, low, high
	– Store the time of the query and the respective keys and values in the database table. For each iteration,
	during which you save the data for a specific minute, you may wait till the start of the next minute, say,
	12:37 and then save the data for all tickers during that iteration with the Time field set to the minute
	(12:37).
	– The class must have a method for initialization of its objects and any other methods you feel are
	necessary.
	– You may assume that your code will be tested on an empty database that you have to create based on
	the name of the database file provided.
	– Please use the information on the API page to figure out how to install iex-api-python. The page also
	has the information for fetching necessary data about a stock ticker.
'''





class Query:

'''
	– Define a function that prints and/or returns the details corresponding to a specific time and ticker
	symbol to the terminal.
	– The class must have a method for initialization of its objects and any other methods you feel are
	necessary.
'''





