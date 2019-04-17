import requests

import sys

from pyquery import PyQuery
from iex import Stock
from selenium import webdriver

class Tickers:
	def __init__(self, n):
		self.ticker_count=n

	def pull150ItemsURL(self):
		# Set up Chrome instance of this url
		driver = webdriver.Chrome(executable_path='./chromedriver')
		driver.get('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQrender=download')

		# Click on the 150 option in page size select so we can get all the symbols we need
		page_size_select = driver.find_element_by_id('main_content_lstpagesize')
		for page_size_option in page_size_select.find_elements_by_tag_name('option'):
			if page_size_option.text == '200 Items Per Page':
				page_size_option.click()
				break

		return driver.current_url



	def save_tickers(self, file_name='tickers.txt'):
		if int(self.ticker_count) > 110:
			raise Exception("You need to give me a number less than or equal to 110!")

		# Create request with 150 item url
		request = requests.get(url=self.pull150ItemsURL())
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
					break
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

	def update_ticker(self, ticker, conn, current_time):
		#print(ticker, len(ticker))
		s=Stock(str(ticker))
		ticker_info = Stock(ticker).quote()
		c = conn.cursor()
		
		cmd = ''' INSERT INTO StockData VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, {} ) '''.format(current_time, ticker, ticker_info['low'], ticker_info['high'], ticker_info['open'],ticker_info['close'],
			ticker_info['latestPrice'], ticker_info['latestVolume'])
		c.execute(cmd)
		conn.commit()

	def fetch_all_data(self, ticker_file='tickers.txt'): #TODO: TickerFile

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
		self.database_name = db
		self.time_lim = tl



class Query:

	def print_info(self):
		conn = sqlite3.connect(self.database_name)
		c= conn.cursor()
		cmd = ''' SELECT * FROM StockData WHERE Time=='{}' and Ticker=='{}' '''.format(self.time, self.ticker)
		c.execute(cmd)
		print(c.fetchone())
	
	def __init__(self, db, t, tn):
		self.database_name = db
		self.time = t
		self.ticker=tn
		






