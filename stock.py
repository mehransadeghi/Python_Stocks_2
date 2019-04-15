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
import sqlite3


class Fetcher:

	def update_ticker(self, ticker, conn, current_time):

	    ticker_info = Stock(symbol=ticker).quote()
	    c = conn.cursor()
	    c.execute(''' INSERT INTO StockData VALUES 
	    	(current_time, ticker, ticker_info['low'], ticker_info['high'], ticker_info['open'],ticker_info['close'],
	    	ticker_info['latestPrice'], ticker_info['latestVolume'])  ''')
	    conn.commit()

	def fetch_all_data(self, time_lim, ticker_file): #TODO: TickerFile

		currentDT = datetime.datetime.now()
	    endTime = currentDT + datetime.timedelta(seconds=int(time_lim))
	    if(currentDT < endTime):
	    	fp = open(ticker_file)
	    	conn = sqlite3.connect('stocks_now.db') #TODO Database Name  #TODO connection check
	    while currentDT < endTime:
	        # Calculate time to sleep until next minute starts
	        sleepTime = 60 - (datetime.datetime.now().second + datetime.datetime.now().microsecond / 1000000.0)
	        time.sleep(sleepTime)

	        current_time = two_digit_time(currentDT)
	        for ticker in fp:
	            update_ticker(ticker=ticker.strip('\n'), conn, current_time)
	        fp.close()

	def two_digit_time(self, currentDT):
	    hour = currentDT.hour
	    minute = currentDT.minute
	    
	    if minute < 10:
	        minute = '0' + str(minute)
	    else:
	        minute = str(minute)

	    if hour < 10:
	        hour = '0' + hour(minute)
	    else:
	        hour = str(hour)
	    return('{}:{}'.format(hour, minute))

	def __init__(self):
		pass



class Query:

'''
	– Define a function that prints and/or returns the details corresponding to a specific time and ticker
	symbol to the terminal.
	– The class must have a method for initialization of its objects and any other methods you feel are
	necessary.
'''





