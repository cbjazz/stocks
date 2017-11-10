#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse
import cgi
import barh_demo
import gpdbDao

class S(BaseHTTPRequestHandler):
	host = '192.168.147.135'
	port = 28081

	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		parsed_path = urlparse.urlparse(self.path)

		path = parsed_path.path
		query = parsed_path.query 

		params = {}
		if len(query) > 1:
			params = cgi.parse_qs(query, True, True)
		if 'sql' in params:
			sql = params['sql'][0]
		if 'key' in params:
			key = params['key'][0]

		#self.writeMenu()
		if path == '/top':
			self.getTopPage()
		elif path == '/bottom':
			self.getBottomPage()
		elif path == '/result':
			self.getResultPage(sql)
		elif path == '/cor':
			self.getCorPage(key)
		else: 
			self.getMainPage()
		
			
	def do_HEAD(self):
		self._set_headers()
		

	def do_POST(self):
		self._set_headers()
		self.wfile.write("<html><body><h1>POST!</h1></body></html>")

	def writeMenu(self):
		self.wfile.write("<H1><a href='http://" + self.host + ":" + str(self.port) + "/items'> ITEM </a></H1>")
		self.wfile.write("<H1><a href='http://" + self.host + ":" + str(self.port) + "/cor'> CORRELATION </a></H1>")
		self.wfile.write("<H1><a href='http://" + self.host + ":" + str(self.port) + "/apriori'> APRIORI </a></H1>")
		#self.wfile.write("<H1><a href='http://" + self.host + ":" + str(self.port) + "/boxplot'> BOXPLOT </a></H1>")
		#self.wfile.write("<H1><a href='http://" + self.host + ":" + str(self.port) + "/scatter'> SCATTER </a></H1>")
		#self.wfile.write("<H1><a href='http://" + self.host + ":" + str(self.port) + "/flowboxplot'> FLOW BOXPLOT</a></H1>")

	def getGraph(self):
		self.wfile.write("<html>")
		self.wfile.write("<body>")
		self.wfile.write(barh_demo.d3exam())
		self.wfile.write("</body>")
		self.wfile.write("</html>")


	#############################################
	## PAGE- main
	def getMainPage(self):
		self.wfile.write("<html>")
		self.wfile.write('<frameset rows="25%,75%">')
		self.wfile.write('<frame name="_top" src="/top" />')
		self.wfile.write('<frame name="_bottom" src="/bottom" />')
		self.wfile.write('</frameset>')
		self.wfile.write("</html>")
		

	#############################################
	## PAGE- top 
	def getTopPage(self):
		self.wfile.write("<html>")
		self.wfile.write("<body>")
		self.wfile.write('<form name="input" target="_bottom" action="result">')
		self.wfile.write('<div>')
		self.wfile.write('<div style="float:left;width:10%;">')
		self.wfile.write('<p>SQL</p>')
		self.wfile.write('</div>')
		self.wfile.write('<div style="float:left;width:90%;">')
		self.wfile.write('<textarea style="width:100%;" name="sql" rows=10></textarea>')
		self.wfile.write('</div>')
		self.wfile.write('<div style="clear:both;"></div>')
		self.wfile.write('</div>')
		self.wfile.write('<input type="submit" value="submit">')
		self.wfile.write('</from>')
		self.wfile.write("</body>")
		self.wfile.write("</html>")

	#############################################
	## PAGE- top 
	def getResultPage(self, sql):
		headers, result = gpdbDao.executeSql(sql)

		self.wfile.write("<html>")
		self.wfile.write("<body>")
		self.drawItemTableWithHeader(result, headers)
		self.wfile.write("</body>")
		self.wfile.write("</html>")


	def getCorPage(self, key):
		headers, result = gpdbDao.executeCorrelation(key)
		self.wfile.write("<html>")
		self.wfile.write("<body>")
		self.drawItemTableWithHeader(result, headers)
		self.wfile.write("</body>")
		self.wfile.write("</html>")

	def executeMockSql(self, sql):
		resultSet = []
		for i in range(0,3):
			cols = []
			for j in range(0,3):
				cols.append(i*3 + j)
			resultSet.append(cols)	
		return resultSet

	#############################################
	## PAGE- top 
	def getBottomPage(self):
		self.wfile.write("<html>")
		self.wfile.write("<body>")
		self.wfile.write('Hello')
		self.wfile.write("</body>")
		self.wfile.write("</html>")
		
	#############################################
	## ITEM - data table
	def drawItemTableWithHeader(self, results, header):
		self.wfile.write('<table border=1>')
		page = 'analyze'
		for header_idx in range(0, len(header)):
			self.wfile.write('<td>' + header[header_idx] + '</td>')	
			
		for row in results:
			self.wfile.write('<tr>')
			for column_idx in range(0, len(row)):
				if str(row[column_idx]).startswith('chart@'):
					imgData = row[column_idx][len('chart@'):]
					imagePath = '<img src="data:image/png;base64,%s"/>' % imgData 
					self.wfile.write('<td>' + imagePath + '</td>')
				elif str(row[column_idx]).startswith('cor@'):
					page = 'cor'
					link = "/" + page + "?key=" + row[column_idx][len('cor@'):]
					self.wfile.write('<td><a href="' + link + '">' + row[column_idx][len('cor@'):] + '</a></td>')	
				else :	
					self.wfile.write('<td>' + str(row[column_idx]) + '</td>')	
			self.wfile.write('</tr>')
		self.wfile.write('</table>')
	
def run(server_class=HTTPServer, handler_class=S, port=28081):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print "Strating httpd..."
	httpd.serve_forever()


if __name__ == "__main__":
	from sys import argv

	if len(argv) == 2:
		run (port=int(argv[1]))
	else:
		run()
