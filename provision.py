import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import MP3
import hashlib
import sqlite3

con = sqlite3.connect('Data')
con.text_factory = str
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS  info (
		hash varchar(255),
		path varchar(255),
		hits int,
		hit_time_stamp varchar(255),
		performer varchar(255),
		lyricist varchar(255),
		genre varchar(255),
		composer varchar(255),
		encodedby varchar(255),
		tracknumber varchar(255),
		album varchar(255),
		copyright varchar(255),
		title varchar(255),
		version varchar(255),
		website varchar(255),
		date varchar(255),
		discnumber varchar(255),
		originaldate varchar(255),
		language varchar(255),
		artist varchar(255),
		author varchar(255),
		bpm int,
		length int,
		organization varchar(255),
		PRIMARY KEY (hash)
		)''')

con.commit()

def insert_db(dict_) :
	try :
		values = default_mapping()
		for k,v in dict_.iteritems() :
			if k in values.keys() :
				values[k] = v
		columns = ', '.join(values.keys())
		placeholders = ', '.join('?' * len(values))		
		sql = 'INSERT INTO info ({}) VALUES ({})'.format(columns, placeholders)		
		cur.execute(sql,values.values())
		con.commit()
	except sqlite3.IntegrityError :
		pass
	

def default_mapping() :
	return {
		'hash' :'',
		'path' :'',
		'hits' : 0,
		'hit_time_stamp' :'',
		'performer':'',
		'lyricist' :'',
		'genre' :'',
		'composer' :'',
		'encodedby' :'',
		'tracknumber' :'',
		'album' :'',
		'copyright' :'',
		'title' :'',
		'version' :'',
		'website' :'',
		'date' :'',
		'discnumber' :'',
		'originaldate' :'',
		'language' :'',
		'artist' :'',
		'author' :'',
		'bpm' : 0,
		'length' : 0,
		'organization' :''
	}

def md5(string) :
	hasher = hashlib.md5()
	hasher.update(string.lower())
	return hasher.hexdigest().lower()

def transform_(dict_) :
	new_dict = {}
	for k,v in dict_.iteritems() :
		new_dict.update({k:v[0]})
	return new_dict

keys = set()
counter = 0

for root, dirs, files in os.walk("/mnt/E0BA285ABA282F88/Users/Daman Arora"):	
	for file_ in files:		
		if file_[-4:] == '.mp3' :
			counter += 1
			path = os.path.join(root,file_)
			try :
				tags = transform_(EasyID3(path))
			except ID3NoHeaderError :
				pass
			tags.update({'path':path})			
			length  = MP3(path).info.length
			with open(path,'rb') as f :
				hash_ = md5(f.read()[:3000] + str(length))
			tags.update({'length':length})	
			tags.update({'hash':hash_})
			insert_db(tags)

			# for tag in ['title','artist','album','genre','date'] :
			# 	try :
			# 		tAg = tags[tag][0]
			# 		Tags.append(tAg)
			# 	except KeyError :
			# 		Tags.append('###')
			# 	for index in range(len(Tags)) :
			# 		temp = []
			# 		for crap in craps :
			# 			if crap in Tags[index] :
			# 				temp.append(crap)
			# 		temp = map ( lambda x : [x,len(x)], temp)
			# 		temp = sorted(temp,key=itemgetter(1))
			# 		if temp == [] :
			# 			Tags[index] = Tags[index].strip()
			# 		else :
			# 			Tags[index] = Tags[index].replace(temp[-1][0],:'',).strip()        
			# return Tags