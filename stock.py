import requests

import sys

from pyquery import PyQuery
from iex import Stock
from selenium import webdriver

class Tickers:
	"""

	"""
	def __init__(self, n):
		"""
		creates the variables associated with the class

		:type n: int
		:param n: the number of tickers to get
		"""
		self.ticker_count = n

	def pull200ItemsURL(self):
		"""
		Clicks a button to make the webpage display 200 tickers

		:return: the url to a page containing 200 ticker symbols
		"""
		# Set up Chrome instance of this url
		driver = webdriver.Chrome(executable_path='./chromedriver')
		driver.get('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQrender=download')

		# Click on the 200 option in page size select so we can get all the symbols we need
		page_size_select = driver.find_element_by_id('main_content_lstpagesize')
		for page_size_option in page_size_select.find_elements_by_tag_name('option'):
			if page_size_option.text == '200 Items Per Page':
				page_size_option.click()
				break

		return driver.current_url

	def __str__(self):
		return str(self.ticker_count)


	def save_tickers(self, file_name='tickers.txt'):
		"""
		writes ticker symbols to a file named tickers.txt

		:type file_name: string
		:param file_name: name of the file in which to store the ticker symbols
		:return:
		"""
		if int(self.ticker_count) > 110:
			raise Exception("You need to give me a number less than or equal to 110!")

		# Create request with 150 item url
		request = requests.get(url=self.pull200ItemsURL())
		parser = PyQuery(request.text)
		table = parser("#CompanylistResults")

		table_parser = PyQuery(table)
		symbols = table_parser("h3")
		symbol_list = [symbol for symbol in symbols.text().split()]

		valid_tickers=[]
		for ticker in (symbol_list):
			try:
				if len(valid_tickers) < int(self.ticker_count):
					Stock(ticker).price()
					valid_tickers.append(ticker)
					print(ticker)
				else:
					symbol_list.remove(ticker)
			except:
				pass

		f = open(file_name, "w")
		for symbol in (valid_tickers):
			f.write(symbol + '\n')	
		f.close()



import csv
import datetime
import time

import sqlite3


class Fetcher:
	"""

	"""
	def update_ticker(self, ticker, conn, current_time):
		#print(ticker, len(ticker))
		s=Stock(str(ticker))
		"""
		creates a new row in the database for the specified ticker and time

		:type ticker: string
		:param ticker:

		:type conn:
		:param conn: the connection to the database

		:type current_time: datetime
		:param current_time: the current time

		:return:
		"""
		print(ticker, len(ticker))
		ticker_info = Stock(ticker).quote()
		c = conn.cursor()

		cmd = ''' INSERT INTO StockData VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, {} ) '''.format(current_time, ticker, ticker_info['low'], ticker_info['high'], ticker_info['open'],ticker_info['close'],
			ticker_info['latestPrice'], ticker_info['latestVolume'])
		c.execute(cmd)
		conn.commit()

	def fetch_all_data(self, ticker_file='tickers.txt'): #TODO: TickerFile
		"""
		:type ticker_file: string
		:param ticker_file: name of the file in which the tickers are stored
		:return:
		"""
		currentDT = datetime.datetime.now()
		endTime = currentDT + datetime.timedelta(seconds=int(self.time_lim))
		if(currentDT < endTime):
			conn = sqlite3.connect(self.database_name)  #TODO connection check
		while currentDT < endTime:
			print(currentDT, endTime)
			fp = open(ticker_file)
			# Calculate time to sleep until next minute starts
			sleepTime = 60 - (datetime.datetime.now().second + datetime.datetime.now().microsecond / 1000000.0)
			time.sleep(sleepTime)

			current_time = self.two_digit_time(currentDT)
			for ticker in fp:
				self.update_ticker(ticker.strip(), conn, current_time)
			fp.close()
			currentDT = datetime.datetime.now()

	def two_digit_time(self, currentDT):
		"""
		formats the time that will be inserted into the database

		:type currentDT: datetime
		:param currentDT: the current time
		:return:
		"""
		hour = currentDT.hour
		minute = currentDT.minute
		
		if minute < 10:
			minute = '0' + str(minute)
		else:
			minute = str(minute)

		if hour < 10:
			hour = '0' + str(hour)
		else:
			hour = str(hour)
		return('{}:{}'.format(hour, minute))

	def __init__(self, db, tl):
		"""
		creates the variables associated with the class

		:type db:
		:param db:

		:type tl:
		:param tl:
		"""
		self.database_name = db
		self.time_lim = tl



class Query:
	"""
	"""

	def print_info(self):
		conn = sqlite3.connect(self.database_name)
		c= conn.cursor()
		cmd = ''' SELECT * FROM StockData WHERE Time=='{}' and Ticker=='{}' '''.format(self.time, self.ticker)
		c.execute(cmd)

	def print_info(self, time, ticker):
		""""

		:type time: string
		:param time: the time to print the specified ticker's information for

		:type ticker: string
		:param ticker: the ticker that will have its information printed
		:return:
		"""
		conn = sqlite3.connect('stocks_now.db') #TODO Database Name  #TODO connection check
		c= conn.curosr()
		c.execute(''' SELECT * FROM StockData WHERE Time==time and Ticker==ticker''')
		print(c.fetchone())
	
	def __init__(self, db, t, tn):
		self.database_name = db
		self.time = t
		self.ticker=tn

	def __init__(self):
		"""
		creates the variables associated with the class
		"""
		pass






