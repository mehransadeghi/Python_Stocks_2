'''
– Should have a main module that takes the following flags:
∗ operation: Values are: ’Fetcher’, ’Ticker’, or ’Query’ Based on the value of this variable, you will
decide which class you will instantiate and the optional arguments whose values you will need.
1. For ’Ticker’: Use the optional flag ’ticker count’ to instantiate Tickers class and then call the
save tickers() function.
2. For ’Fetcher’: Use the optional flags ’db’ and ’time limit to instantiate Fetcher class and then
call the fetch all data() function.
3. For ’Query’: Use the optional flags ’db’ and ’time’ and ’ticker’ to instantiate Query class and
then call the function to fetch and print data from the database. The data must be printed out
to the terminal when this operation is used.
∗ time: Used by the Query class to identify the specific minute for which to print data. Optional
argument used only for the Query class.
∗ ticker: Used by the Query class to identify the specific ticker for which to print data. Optional
argument used only for the Query class.
∗ time limit: Used by the Fetcher class to identify the length of time in seconds for which to fetch
data. Optional argument used only for the Fetcher class.
∗ db: Used by the Fetcher and Query classes to specify the database file to be used. Optional argument
used only for the Fetcher and Query classes.
∗ ticker count: Used only by the Tickers class to specify the number of valid tickers to be fetched.
Optional argument only used by Tickers class.
'''