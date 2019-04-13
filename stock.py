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
	def save_tickers(self, n, url, file_name):




	def __init__(self):
		


class Fetcher:

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





