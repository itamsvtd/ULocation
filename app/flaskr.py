# all the imports
from __future__ import with_statement
import json
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = 'flaskr.json'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



@app.before_request
def before_request():
    try:
        db = open(DATABASE).read()
    except IOError:
        db = '{"location":[]}'
    g.db = json.loads(db)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g,'db'):
        open(DATABASE,'w').write(json.dumps(g.db, indent = 4))

@app.route('/')
def show_location():
    #cur = g.db.execute('select lat,lng,address,name from location order by id desc')
    #locations = [dict(lat = row[0] , lng = row[1], address=row[2], name=row[3]) for row in cur.fetchall()]
    return render_template('show_locations.html', locations=g.db['location'])

@app.route('/add', methods=['GET','POST'])
def add_location():
    if not session.get('logged_in'):
        abort(401)
    #g.db.execute('insert into location (lat,lng , address, name) values (?, ?,?,?)',
    #             [request.form['lat'], request.form['lng'],request.form['address'],request.form['name']])
    g.db['location'].insert(0,
        {
            'lat':request.form['lat'],
            'lng':request.form['lng'],
            'address':request.form['address'],
            'name':request.form['name']
        }
        )
    
    flash('New location successfully created')
    return redirect(url_for('show_location'))

@app.route('/delete', methods=['GET','POST'])
def delete_location():
    if not session.get('logged_in'):
        abort(401)
    locations = g.db['location']
    for x in locations:
        #if x.name==request.form['deletename']:
        g.db['location'].delete(x)

    flash('New location successfully created')
    return redirect(url_for('show_location'))

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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_location'))

if __name__ == '__main__':
    app.run()