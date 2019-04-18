import argparse
import sys

import stock

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--operation")
	parser.add_argument("--time")
	parser.add_argument("--ticker")
	parser.add_argument("--time_limit")
	parser.add_argument("--db")
	parser.add_argument("--ticker_count")

	args = parser.parse_args()
	if(args.operation=='Fetcher'):
		fetcher = stock.Fetcher(args.db, int(args.time_limit))
		fetcher.fetch_all_data()
	elif(args.operation=='Ticker'):
		ticker=stock.Tickers(int(args.ticker_count))
		ticker.save_tickers()
	elif(args.operation=='Query'):
		query = stock.Query(args.db, args.time, args.ticker)
		query.print_info()
	else:
		print('invalid value for parameter operation')
		sys.exit()
