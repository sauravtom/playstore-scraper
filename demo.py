import flask, flask.views
import os
from scraper import *
import sqlite3 as lite

app = flask.Flask(__name__)
# Don't do this!
app.secret_key = "bacon"


@app.route('/paid2')
def foo():
    with open(file1,'r') as f:
        content = f.readlines()
    flask.flash(content)
    return flask.render_template('paid.html',content=content)

class Paid(flask.views.MethodView):
    def get(self):
    	with open(file1,'r') as f:
    	    content = f.readlines()
        flask.flash(content)
        return flask.render_template('paid.html',content=content)

class Free(flask.views.MethodView):
    def get(self):
    	with open(file2,'r') as f:
    	    content = f.readlines()
        #flask.flash(content)
        return flask.render_template('free.html',content=content)

class Index(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')      

class DBpaid(flask.views.MethodView):
    def get(self):
    	with open(file3,'r') as f:
    	    content = f.readlines()
        flask.flash(content)
        #print template.render(dictionary=content)
        #return flask.render_template('DBpaid.html',content=content)
        return render_template("DBpaid.html", title='Edit Creative', creative_handler=creative_handler,content=content)         

app.add_url_rule('/', view_func=Index.as_view('main'), methods=['GET'])    
app.add_url_rule('/paid', view_func=Paid.as_view('main1'), methods=['GET'])
app.add_url_rule('/free', view_func=Free.as_view('main2'), methods=['GET'])
app.add_url_rule('/DBpaid', view_func=DBpaid.as_view('main3'), methods=['GET'])

app.debug = True
app.run()


