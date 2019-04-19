import requests
from pyquery import PyQuery
from iex import Stock
from selenium import webdriver

MAX_TICKERS=110


class Tickers:
    """
    A class to fetch all tickers and store them in a file tickers.txt

    :type ticker_count: int
    :param ticker_count: The number of tickers to get
    """
    def __init__(self, n):
        """
        Creates the variables associated with the class

        :type n: int
        :param n: The number of tickers to get
        """
        self.ticker_count = n

    def pull200ItemsURL(self):
        """
        Clicks a button to make the webpage display 200 tickers

        :return: The url to a page containing 200 ticker symbols
        :rtype: string
        """
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


    def __str__(self):
        """
        :return: the number of tickers to grab from the url
        :rtype: string
        """
        return str(self.ticker_count)

    def save_tickers(self, file_name='tickers.txt'):
        """
        Writes ticker symbols to a file named tickers.txt

        :type file_name: string
        :param file_name: Name of the file in which to store the ticker symbols

        :rtype: void
        """
        f int(self.ticker_count) > MAX_TICKERS:
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
					break
			except:
				pass
		
		f = open(file_name, "w")
		for symbol in (valid_tickers):
			f.write(symbol + '\n')	
		f.close()





import datetime
import time
import sqlite3


class Fetcher:
    """
    A class to write all relevant information for the tickers in tickers.txt to a database

    :type database_name: string
    :param database_name: The name of the database to store the information in

    :type time_lim: int
    :param time_lim: The time, in seconds, to update the database
    """

    def __init__(self, db, tl):
        """
        Creates the variables associated with the class

        :type db: string
        :param db: The name of the database to store the information in

        :type tl: int
        :param tl: The time, in seconds, to update the database
        """
        self.database_name = db
        self.time_lim = tl

    def update_ticker(self, ticker, conn, current_time, test=False):
        """
        Creates a new row in the database for the specified ticker and time

        :type ticker: string
        :param ticker: The ticker to be inserted

        :type conn:
        :param conn: The connection to the database

        :type current_time: datetime
        :param current_time: The current time to be inserted

        :rtype: void
        """

        s=Stock(str(ticker))
		ticker_info = Stock(ticker).quote()

		c = conn.cursor()
		values = "('{}', '{}', '{}', '{}', '{}', '{}', {}, {})".format(current_time, ticker, ticker_info['low'], ticker_info['high'], ticker_info['open'],ticker_info['close'],
			ticker_info['latestPrice'], ticker_info['latestVolume'])

		if(test):
			test_file = open('test_fetch.txt', 'a+')
			test_file.write(values+'\n')
			test_file.close()
		cmd = ' INSERT INTO StockData VALUES ' + values
		c.execute(cmd)
		conn.commit()


    def fetch_all_data(self, ticker_file='tickers.txt', test=False): 
        """
        Waits until the start of the next minute and then writes the tickers from tickers.txt to a database

        :type ticker_file: string
        :param ticker_file: Name of the file in which the tickers are stored

        :rtype: void
        """
        currentDT = datetime.datetime.now()
		endTime = currentDT + datetime.timedelta(seconds=int(self.time_lim))
		if(currentDT < endTime):
			conn = sqlite3.connect(self.database_name)  
		while currentDT < endTime:
			print(currentDT, endTime)
			fp = open(ticker_file)
			# Calculate time to sleep until next minute starts
			sleepTime = 60 - (datetime.datetime.now().second + datetime.datetime.now().microsecond / 1000000.0)
			time.sleep(sleepTime)

			current_time = self.two_digit_time(currentDT)
			for ticker in fp:
				self.update_ticker(ticker.strip(), conn, current_time, test)
			fp.close()
			currentDT = datetime.datetime.now()

    def two_digit_time(self, currentDT):
        """
        Formats the time that will be inserted into the database

        :type currentDT: datetime
        :param currentDT: The current time

        :return: The time formatted as HH:MM
        :rtype: string
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



class Query:
    """
    A class to query the database for a certain time and ticker

    :type database_name: string
    :param database_name: The name of the database that information is stored in

    :type time: string
    :param time: The time to search for in the database

    :type ticker: string
    :param ticker: The ticker to search for in the database

    """
    def __init__(self, db, t, tn):
        """
        creates the variables associated with the class

        :type db: string
        :param db: The name of the database that information is stored in

        :type t: string
        :param t: The time to search for in the database

        :type tn: string
        :param tn: The ticker to for in the database
        """
        self.database_name = db
        self.time = t
        self.ticker = tn

    def print_info(self):
        """
        Queries the database for a specific time and ticker

        :rtype: void
        """
        conn = sqlite3.connect(self.database_name)
		c= conn.cursor()
		cmd = ''' SELECT * FROM StockData WHERE Time=='{}' and Ticker=='{}' '''.format(self.time, self.ticker)
		c.execute(cmd)
		return(c.fetchone())

	def __str__(self):
		return 'time = {}, database_name = {}, ticker = {}'.format(self.time, self.database_name, self.ticker)
