from flask import Flask
from flask import send_from_directory
from flask import request
from flask import Response
import os
import sqlite3
import threading
import json

app = Flask(__name__)

def root_dir():
	return os.path.abspath(os.path.dirname(__file__))

@app.route('/<path:path>')
def resource(path):
	try :
		mimetypes = {
			".css": "text/css",
			".html": "text/html",
			".js": "application/javascript",
		}
		complete_path = os.path.join(root_dir(), path)
		ext = os.path.splitext(path)[1]
		mimetype = mimetypes.get(ext, "text/html")
		with open(complete_path,'rb') as f :
			content = f.read()	
		return Response(content, mimetype=mimetype)
	except  :
		return ''

@app.route("/home")
def home():
	return """
<!DOCTYPE html>
<html>
<head>
	<title>Dice. Your Own Musical World.</title>
	<link rel="stylesheet" type="text/css" href="css/base.css">
	<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
	<script type="text/javascript" src="js/jquery.js"></script>
	<script type="text/javascript" src="js/base.js"></script>
	<script type="text/javascript" src="bootstrap/js/bootstrap.js"></script>
</head>
<body>
<div class="container">
	<div class="row">
		<div class="col-md-12 list">
			Hey
		</div>

	</div>
	<div class="row">
		<div class="col-md-12 list">
			<audio controls>
				<!-- <source src="horse.ogg" type="audio/ogg"> -->
				<source src="1.mp3" type="audio/mpeg">
				Your browser does not support the audio element.
			</audio>
		</div>
		
	</div>
	
</div>
</body>
</html>
"""
@app.route("/search")
def search() :
	sql = "SELECT hash,title,artist,album,genre from info where "
	for param in request.args.items() :
		sql += ' '
		sql += param[0]
		sql += ' LIKE  "%'
		sql += param[1]
		sql += '%" '
		sql += ' AND '
	sql = sql[:-6].strip()
	print sql	
	con = sqlite3.connect('Data')
	con.text_factory = str
	cur = con.cursor()
	cur.execute(sql)
	exp_fields = ['hash','title','artist','album','genre']
	data = json.dumps([{ exp_fields[i] : item[i] for i in range(len(exp_fields)) } for item in cur.fetchall()],indent=5)
	return data
	
@app.route("/track")
def track() :
	hash_ = request.args.get('hash')
	con = sqlite3.connect('Data')
	con.text_factory = str
	cur = con.cursor()
	cur.execute("SELECT path,hits from info where hash = ?",(hash_,))	
	con.commit()	
	gen = cur.fetchall()[0]
	path = gen[0]
	hits = gen[1]
	hits += 1
	cur.execute("UPDATE info SET hits = ? WHERE hash = ?",(hits,hash_))
	con.commit()
	con.close()
	with open(path,'rb') as f :
		content = f.read()
	print len(content)
	return content[:186225]
	return Response(content, mimetype='audio/mpeg')
	

app.run(host='0.0.0.0', port=6969,debug=True)