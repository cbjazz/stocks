import ystockquote
import json
from pprint import pprint
import psycopg2
import sys

##{'2017-01-02': {'Adj Close': '51600.00',
##                'Close': '51600.00',
##                'High': '52300.00',
##                'Low': '51600.00',
##                'Open': '51800.00',
##                'Volume': '431400'},

def getConnection():
	try:
		conn = psycopg2.connect("dbname='ccb' user='gpadmin' host='172.16.42.172' password='changeme'")
		return conn 
	except:
		print "I am unable to connect to the database"

def getStockCode(conn):
	cur = conn.cursor()
	cur.execute("SELECT company_code || '.' || nation_code, kor_name  FROM stock.kospi_200")
	rows = cur.fetchall()
	cur.close()	
	return rows

def storeStockHistory(conn, code, fromDate, toDate):
	storeList = []
	try:
		data = ystockquote.get_historical_prices(code, fromDate, toDate)
	except:
		print ( code + " URL error")
		return
	if data == None:
		return 
	for stockDate in data:
		print (code + ":" + stockDate)
		storeDic = data[stockDate]
		storeDic["code"] = code
		storeDic["s_date"] = stockDate
		storeDic["adj_close"] = data[stockDate]["Adj Close"]
		storeDic["s_close"] = data[stockDate]["Close"]
		storeDic["s_open"] = data[stockDate]["Open"]
		storeDic["s_high"] = data[stockDate]["High"]
		storeDic["s_low"] = data[stockDate]["Low"]
		storeDic["s_volume"] = data[stockDate]["Open"]
		storeList.append(storeDic)

	cur = conn.cursor()
	cur.executemany("INSERT INTO stock.price(code, s_date, adj_close, s_close, s_open, s_high, s_low, s_volume) VALUES (%(code)s, %(s_date)s, %(adj_close)s, %(s_close)s, %(s_open)s, %(s_high)s, %(s_low)s, %(s_volume)s)", storeList)
	conn.commit()
	cur.close()

if len(sys.argv) < 2:
	print ( "Usage: " + sys.argv[0] + " start_date " + " end_date")
	exit(0)

conn = getConnection()
company_codes = getStockCode(conn)
for company_code in company_codes:
	print (company_code[0] + ":" + company_code[1] + " from " + sys.argv[1] + " to " + sys.argv[2])
	storeStockHistory(conn, company_code[0], sys.argv[1], sys.argv[2]) 
conn.close()
