import random
import stock
import sqlite3
import os
def test_tickers():
	d={}
	
	n=int(random.random()*stock.MAX_TICKERS)+1
	t=stock.Tickers(n)
	assert(str(t)==str(n))
	t.save_tickers('test_tickers.txt')
	with open('test_tickers.txt') as test_file:
		lines = test_file.readlines()
	assert(len(lines)==n)

def test_fetcher():
	try:
		os.remove('test_fetch.txt')
	except:
		pass
	d={}
	tl=int(random.random()*30)
	db = 'stocks.db'
	f=stock.Fetcher(db, tl)
	assert (str(f)=='time_limit = {}, database_name = {}'.format(tl, db))
	with open('tickers.txt', 'r') as tickers_file:
		number_of_tickers = len(tickers_file.readlines())
	f.fetch_all_data(test=True)
	with open('test_fetch.txt', 'r')as test_fetch:
		for line in test_fetch:
			values = line.split(',')
			q=stock.Query(db, values[0][1:].replace("'", ""), values[1].strip().replace("'", ""))
			assert (str(q.print_info()).replace("'", "") == line.strip().replace("'", ""))




def test_query():
	d={}
	t = '16:32'
	db = 'stocks.db'
	tn= 'YI'
	f=stock.Query(db, t, tn)
	assert (str(f)=='time = {}, database_name = {}, ticker = {}'.format(t, db, tn))
	qinfo = f.print_info()
	conn = sqlite3.connect(db)
	c= conn.cursor()
	cmd = ''' SELECT * FROM StockData WHERE Time=='{}' and Ticker=='{}' '''.format(t, tn)
	c.execute(cmd)
	assert (c.fetchone() == qinfo)
