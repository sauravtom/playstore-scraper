import sys
import urllib
import urllib2
from bs4 import BeautifulSoup
import os
import timeit

#from google.appengine.api import urlfetch

#import sqlite3 as lite

test_url='https://play.google.com/store/apps/details?id=com.dama.papercamera'

user_agent = 'Python-urllib/1.17 AppEngine-Google'

def generate_app_list(n=500):
	#returns an array containing app list
	arr1=[]
	arr2=[]

	for i in range(0,n,24):
		appurl = ''
		url ='https://play.google.com/store/apps/collection/topselling_paid?start='+str(i)
		#soup = BeautifulSoup( urllib.urlopen(url).read() )
		#result = urlfetch.fetch(url)
		#url_response = urlfetch.fetch( url, headers={ "User-Agent" : user_agent } ).content
		#soup = BeautifulSoup( url_response )

		headers = { 'User-Agent' : 'Yugdom 2.0 by /u/Tomarina github.com/sauravtom/yugdom','Host' : 'play.google.com' }
		req = urllib2.Request(url, None, headers)
		soup = BeautifulSoup( urllib2.urlopen(req).read() )

		for j in soup.find_all('li',{'class' : 'goog-inline-block'}):
			try : appurl = 'https://play.google.com/store/apps/details?id=' + j.get('data-docid')
			except : appurl = 'XXXXXXXXXX'
			
			arr1.append(appurl)
		print appurl	
		print "I #%s : %s" %( i,appurl.split('=')[-1] )

		url ='https://play.google.com/store/apps/collection/topselling_free?start='+str(i)
		soup = BeautifulSoup( urllib.urlopen(url).read() )

		for j in soup.find_all('li',{'class' : 'goog-inline-block'}):
			appurl = 'https://play.google.com/store/apps/details?id=' + j.get('data-docid')
			arr2.append(appurl)
		print "II #%s : %s" %( i,appurl.split('=')[-1] )

	return (arr1,arr2)


def generate_app_details(app_url,rank):
	#returns a dictionary containing app details of the app-url passed as the parameter

	d={}
	d['rank'] = rank
	soup = BeautifulSoup( urllib.urlopen(app_url).read() )
	head = soup.find('td',{'class' : 'doc-banner-title-container'})
	
	try : d['name'] = head.find('h1',{'class' : 'doc-banner-title'}).get_text()
	except : d['name'] = '17291729'
	
	content = soup.find('div',{'class' : 'doc-overview'})

	try: d['developer_website'] = content.find('div',{'class' : 'doc-description-show-all'}).findNext('a').get('href')
	except : d['developer_website'] = '17291729'

	try: d['description'] = content.find('div',{'id' : 'doc-original-text'})
	except : d['description'] = '17291729'

	metadata = soup.find('dl',{'class' : 'doc-metadata-list'})

	try: d['category'] = metadata.find(text="Category:").findNext('dd').contents[0].get_text()
	except: d['category'] = '17291729'

	try: d['rating'] = float( metadata.find('div',{'class' : 'ratings goog-inline-block'}).get('content') )
	except: d['rating'] = 17291729

	try: d['rating_count']= int(metadata.find('span',{'itemprop' : 'ratingCount'}).get('content'))
	except: d['rating_count'] = 17291729
	
	try : unicode_trash = metadata.find(text="Installs:").findNext('dd').contents[0]
	except: 
		d['install_from'] = 17291729
		d['install_to'] = 17291729
	else:
		d['install_from'] = int( unicode_trash.encode('ascii','ignore').split('-')[0].replace(',','') )
		d['install_to'] = int( unicode_trash.encode('ascii','ignore').split('-')[1].replace(',','') )

	print d
	return d


def add_to_db(dict,table,db='test.db'):

	try:
		con = lite.connect(db)
		con.row_factory = lite.Row
		cur = con.cursor()
		
		# add a check for existence of table cars first

		s="""
			DROP TABLE IF EXISTS %s;
			CREATE TABLE %s(rank INT,name TEXT,developer_website TEXT,developer_email TEXT,category TEXT,rating REAL,rating_count INT,install_from INT,install_to INT);
			""" % (table)

		cur.executescript(s)
		
		string = "INSERT INTO %s VALUES(%s,%s,'%s','%s','%s','%s',%s,%s,%s,%s)" % (table,dict['rank'],dict['name'],dict['developer_website'],dict['description'],dict['category'],dict['rating'],dict['rating_count'],dict['install_from'],dict['install_to'])

		print string
		cur.execute(string)
		con.commit()
		print 'DONE'

	except lite.Error , e:
		if con:
			con.rollback()
		print "Error %s" % e.args[0]
		sys.exit()

	#cur.execute("SELECT * FROM Cars")
	#rows = cur.fetchall()
	#print rows['name']


def main():
	arr1,arr2 = generate_app_list()

	for i in arr1:
		d = generate_app_details(i,arr1.index(i)+1)
		#sys.exit(0)
		add_to_db(d)

	for i in arr2:
		d=generate_app_details(i,arr1.index(i)+1)
		add_to_db(d)


if __name__ == '__main__':
	start = timeit.default_timer()
	
	#print generate_app_details(test_url,2)
	#print main()
	print generate_app_list(25)

	stop = timeit.default_timer()
	print stop - start 

