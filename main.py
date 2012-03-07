import web
import tesseract
import base64

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

class home:
	def GET(self):
		web.header("Content-Type","text/html; charset=utf-8")
		return form

	def POST(self):
		infile = web.input()
		if 'image' in infile:
			buf = infile.image  #.file.read()
			print len(buf)
			if buf:
				result = tesseract.ProcessPagesBuffer(buf,len(buf),api)
				print result
				return result
		elif 'imagestr' in infile:
			buf = base64.decodestring(infile.imagestr)
			f = open('im.jpg', 'wb')
			f.write(buf)
			f.close()
			print len(buf)
			if buf:
				result = tesseract.ProcessPagesBuffer(buf,len(buf),api)
				return result

		print 'none'
		raise web.seeother('/')

if __name__ == '__main__':
	app.run()
