# -*- coding: utf-8 -*-

import web
import tesseract
import base64
import re
import json

form = '''
<html>
<head>
	<title></title>
</head>
<body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="image" />
<br/>
<input type="submit" />
</form>
</body>
</html>
'''

urls = ('/', 'home')

app = web.application(urls, globals())
api = tesseract.TessBaseAPI()
api.Init(".","fra",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_SINGLE_COLUMN)

rx1 = re.compile(r'(.*) (\d+[\.,_]\s?\d\d).?$')
rx2 = re.compile(r'(\d+) (\d+[\.,]\d\d) (\d+[\.,]\d\d)$')

def get_items(text):
	items = []
	lines = text.strip().split('\n')
	i = 0
	while i < len(lines):
		m1 = rx1.match(lines[i])
		if m1:
			gr = m1.groups()
			items.append({'name': gr[0], 'price': float(gr[1].replace(',','.').replace('_','.').replace(' ','')), 'qty': 1})
			i += 1
		elif i + 1 < len(lines):
			m2 = rx2.match(lines[i+1])
			if m2:
				gr = m2.groups()
				items.append({'name': lines[i], 'price': float(gr[1]), 'qty': int(gr[0])})
				i += 2
			else:
				i += 1
		else:
			i += 1

	return items

class home:
	def GET(self):
		web.header("Content-Type","text/html; charset=utf-8")
		return form

	def POST(self):
		web.header("Content-Type","text/html; charset=utf-8")
		infile = web.input()
		if 'image' in infile:
			buf = infile.image  #.file.read()
			print len(buf)
			if buf:
				result = tesseract.ProcessPagesBuffer(buf,len(buf),api)
				print result
				return json.dumps(get_items(result))
		elif 'imagestr' in infile:
			buf = base64.decodestring(infile.imagestr)
			f = open('im.jpg', 'wb')
			f.write(buf)
			f.close()
			print len(buf)
			if buf:
				result = tesseract.ProcessPagesBuffer(buf,len(buf),api)
				print result
				return json.dumps(get_items(result))

		print 'none'
		raise web.seeother('/')

if __name__ == '__main__':
	app.run()
