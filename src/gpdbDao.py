import psycopg2
import sys
import StringIO
import base64

def getConnection():
	try:
		conn = psycopg2.connect("dbname='ccb' user='gpadmin' host='192.168.147.134' password='changeme'")
		return conn 
	except:
		print "I am unable to connect to the database"

def executeSql(sql):
	conn = getConnection()
	cur = conn.cursor()
	cur.execute(sql)
	rows = cur.fetchall()
	headers = [desc[0] for desc in cur.description]
	cur.close()
	conn.close()
	return headers, rows

def executeCorrelation(key):
	conn = getConnection()
	cur = conn.cursor()
	cur.execute("SELECT kospi_code, snp_code, cor_value[1] correlation, cor_value[2] p_value" \
		+ " FROM ( " \
		+ "	SELECT kospi_code, snp_code, array_agg(a.s_date order by s_date) as s_date, stock.r_correlation_v2(array_agg(kospi_price order by s_date), array_agg(snp_price order by s_date))  cor_value " \
		+ "		FROM ( " \
		+ "			SELECT a.s_date, a.code kospi_code, b.code snp_code,  a.updown kospi_price, b.updown snp_price " \
		+ "			FROM  " \
		+ "			( " \
		+ "			SELECT code, data_date s_date , score updown " \
		+ "			FROM stock.socre_price   " \
		+ "			WHERE code = '" + key + "'  " \
		+ "				AND data_date >= '2017-01-01'  " \
		+ "				AND data_date < '2017-07-01' " \
		+ "			) as a, " \
		+ "			( " \
		+ "			SELECT code, data_date - '1 day'::interval s_date, score updown " \
		+ "			FROM stock.socre_price   " \
		+ "			WHERE code not like 'KRX:%' " \
		+ "				AND data_date >= '2017-01-01'  " \
		+ "				AND data_date < '2017-07-01' " \
		+ "			) as b	 " \
		+ "			WHERE a.s_date = b.s_date " \
		+ "		) as a " \
		+ "	GROUP BY kospi_code, snp_code " \
		+ "	) as a  WHERE cor_value[1] IS NOT NULL ORDER BY 3 DESC ")
	rows = cur.fetchall()
	headers = [desc[0] for desc in cur.description]
	cur.close()
	conn.close()
	return headers, rows
