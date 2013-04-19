# all the imports
from __future__ import with_statement
import json
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
@app.before_request
def before_request():
    g.db = connect_db()
@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def show_location():
    cur = g.db.execute('select lat,lng,address,name from location order by id desc')
    locations = [dict(lat = row[0] , lng = row[1], address=row[2], name=row[3]) for row in cur.fetchall()]
    return render_template('show_locations.html', locations= locations)

@app.route('/add',methods=['GET','POST'])
def add_location():
    if request.method == 'POST':
        g.db.execute('insert into location(lat,lng,address,name) values (?, ?,?,?)',
            [request.form['lat'], request.form['lng'],request.form['address'],request.form['name']])
        g.db.commit()
        flash('Target location successfully added')

   
    cur = g.db.execute('select lat,lng,address,name from location order by id desc')
    locations = [dict(lat = row[0] , lng = row[1], address=row[2], name=row[3]) for row in cur.fetchall()]
    return render_template('add_location.html',locations= locations)



@app.route('/location/<location_name>',methods=['GET','POST'])
def singlelocation(location_name=None):
    cur = g.db.execute('select lat,lng,address,name from location where name = ?',[location_name])
    locations = [dict(lat = row[0] , lng = row[1], address=row[2], name=row[3]) for row in cur.fetchall()]
    return render_template('single_location.html',locations= locations)



@app.route('/delete', methods=['GET','POST'])
def delete_location():
    if request.method == 'POST':
        g.db.execute('delete from location where name= ?',[request.form['deletename']])
        g.db.commit()
        flash('Target location successfully deleted')

    cur = g.db.execute('select lat,lng,address,name from location order by id desc')
    locations = [dict(lat = row[0] , lng = row[1], address=row[2], name=row[3]) for row in cur.fetchall()]
    return render_template('delete_location.html',locations= locations)

@app.route('/modify', methods=['GET','POST'])
def modify_location():
    if request.method == 'POST':
        g.db.execute('UPDATE location SET lat= ?, lng=?, address = ?,  name =? where name= ?',[request.form['lat'],request.form['lng'],request.form['address'],request.form['name'],request.form['modifyname']])
        g.db.commit()
        flash('Target location successfully modified')

    cur = g.db.execute('select lat,lng,address,name from location order by id desc')
    locations = [dict(lat = row[0] , lng = row[1], address=row[2], name=row[3]) for row in cur.fetchall()]
    return render_template('modify_location.html',locations= locations)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_location'))
    return render_template('login.html', error=error)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_location'))

if __name__ == '__main__':
    app.run()