import sys
import urllib2
from bs4 import BeautifulSoup
import os
import json
import timeit
import ast

import sqlite3 as lite

url1='https://play.google.com/store/apps/collection/topselling_paid'
url2='https://play.google.com/store/apps/collection/topselling_free'
url3='https://play.google.com/store/apps/details?id=com.dama.papercamera'

list_of_dict=[]

file1='applist_paid'
file2='applist_free'
file3='database_paid'
file4='database_free'
filetest='test.txt'

arr1=[]
arr2=[]
arr3=[]
arr4=[]
arrtest=[]


def call_db():
	with open(file3,'r') as f:
	    content = f.readlines()
	    c = ast.literal_eval(content[0])

	for i in c:
		add_to_db[c]


def add_to_db(db,):
	x = c[0]
	#print c[1]['rating']

	try:
		con = lite.connect('test.db')
		con.row_factory = lite.Row
		cur = con.cursor()
		
		#check for existence of table cars
		cur.executescript("""
			DROP TABLE IF EXISTS Cars;
			CREATE TABLE Cars(rank INT,name TEXT,developer_website TEXT,developer_email TEXT,category TEXT,rating REAL,rating_count INT,install_from INT,install_to INT);
			""")
		
		string = "INSERT INTO Cars VALUES(%s,'%s','%s','%s','%s',%s,%s,%s,%s)" % (1,x['name'],x['developer_website'],x['developer_email'],x['category'],x['rating'],x['rating_count'],x['install_from'],x['install_to'])


		print string
		cur.execute(string)
		con.commit()

	except lite.Error , e:
		if con:
			con.rollback()
		print "Error %s" % e.args[0]
		sys.exit()

	cur.execute("SELECT * FROM Cars")
	rows = cur.fetchall()	
	print rows[0]['name']



def generate_app_list():
	#generate a file containing a list of apps

	for i in range(0,500,24):
		curl ='https://play.google.com/store/apps/collection/topselling_paid?start='+str(i)
		append_app_entry(curl,arr1,file1)

		curl ='https://play.google.com/store/apps/collection/topselling_free?start='+str(i)
		append_app_entry(curl,arr2,file2)


def append_app_entry(url,arr=arrtest,file=filetest):
	# appends a single app url to the list

	print 'Now Scraping ' +url

	soup = BeautifulSoup( urllib2.urlopen(url).read() )

	for i in soup.find_all('li',{'class' : 'goog-inline-block'}):
		appurl = 'https://play.google.com/store/apps/details?id=' + i.get('data-docid')
		arr.append(appurl)
		
		with open(file, "w") as myfile:
			for item in arr:
			  myfile.write("%s\n" % item)


def generate_app_database():
	with open(file1,'r') as f:
	    content = f.readlines()
	for i in content:
		append_app_details(i,arr3,file3)

	with open(file2,'r') as f:
	    content = f.readlines()
	for i in content:
		append_app_details(i,arr4,file4)	


def append_app_details(app_url=url3,arr=arrtest,file=filetest):
	d={}
	soup = BeautifulSoup( urllib2.urlopen(app_url).read() )


	try : foo = soup.find('td',{'class' : 'doc-banner-title-container'})
	except : return 'error'
	
	try : d['name'] = foo.find('h1',{'class' : 'doc-banner-title'}).get_text()
	except : d['name'] = '***'
	
	content = soup.find('div',{'class' : 'doc-overview'})

	try:
		for a in content.find_all('a'):
			if 'Website' in a.get_text():
				d['developer_website'] = a.get('href')
			if 'Email' in a.get_text():
				d['developer_email'] = a.get('href')
	except:
		d['developer_email'] = '***'
		d['developer_website'] = '***'

	metadata = soup.find('dl',{'class' : 'doc-metadata-list'})

	try: d['category'] = metadata.find(text="Category:").findNext('dd').contents[0].get_text()
	except: d['category'] = '***'

	try: d['rating'] = float( metadata.find('div',{'class' : 'ratings goog-inline-block'}).get('content') )
	except: d['rating'] = '***'

	try:
		d['rating_count']= int(metadata.find('span',{'itemprop' : 'ratingCount'}).get('content'))
	except:
		d['rating_count'] = '***'
	
	#install should be 2 fields from and to
	try : unicode_trash = metadata.find(text="Installs:").findNext('dd').contents[0]
	except: 
		d['install_from'] = '***'
		d['install_to'] = '***'
	else:
		d['install_from'] = int( unicode_trash.encode('ascii','ignore').split('-')[0].replace(',','') )
		d['install_to'] = int( unicode_trash.encode('ascii','ignore').split('-')[1].replace(',','') )


	
	
	'''
	#obsolute piece of code

	try : 
		d['developer_orgname'] = foo.find('a',{'class' : 'doc-header-link'}).get_text()
		d['developer_otherapps'] = 'https://play.google.com/store/apps/details?id=' + foo.find('a',{'class' : 'doc-header-link'}).get('href')
	except : pass
	try: d['category_link'] = 'https://play.google.com/store/apps/details?id=' + metadata.find(text="Category:").findNext('dd').contents[0].get('href')
	except: pass
	try: d['img_last30days'] = metadata.find(text="Installs:").findNext('dd').contents[1].img.get('src')
	except: pass
	try: d['last_published'] = metadata.find('time').get_text()
	except: pass
	try : d['content_rating'] = metadata.find(text="Content Rating:").findNext('dd').contents[0]
	except: pass
	'''

	arr.append(d)
		
	with open(file, 'w') as outfile:
		json.dump(arr, outfile)  
		
	print 'successfully appended file ' + file

	return d




if __name__ == '__main__':
	#start = timeit.default_timer()
	#generate_app_list()
	#print append_app_details()
	call_db()
	#stop = timeit.default_timer()
	#print stop - start 

