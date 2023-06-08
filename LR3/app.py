from flask import Flask, render_template, g
from datetime import datetime
import pytz
import random

#!/usr/bin/python
import psycopg2
from config import config


### Make the flask app
app = Flask(__name__)

@app.route("/dump") 
def dump_entries2(): 
    params = config() 
    conn = psycopg2.connect(**params) 
    cursor = conn.cursor() 
    cursor.execute('select id, date, title, content from entries order by date') 
    rows = cursor.fetchall() 
    output = "" 
    for r in rows: 
        app.logger.debug(str(r)) 
        q = (r[0], r[1].strftime("%Y-%m-%d %H:%M:%S"),) + r[2:] 
        output += str(q) 
        output += "\n" 
    return "<pre>" + output + "</pre>"

@app.route("/dump2") 
def dump_entries(): 
    params = config() 
    conn = psycopg2.connect(**params) 
    cursor = conn.cursor() 
    cursor.execute('select id, date, title, content from entries order by title') 
    rows = cursor.fetchall() 
    output = "" 
    for r in rows: 
        app.logger.debug(str(r)) 
        q = (r[0], r[1].strftime("%Y-%m-%d %H:%M:%S"),) + r[2:] 
        output += str(q) 
        output += "\n" 
    return "<pre>" + output + "</pre>"

@app.route("/")
def hello_world():
    return "Hello, world!"  # Whatever is returned from the function is sent to the browser and displayed.

@app.route("/time")
def get_time():
    now = datetime.now().astimezone(pytz.timezone("US/Central"))
    timestring = now.strftime("%Y-%m-%d %H:%M:%S")  # format the time as a easy-to-read string
    return render_template("time.html", timestring=timestring)


@app.route("/me")
def get_me():
  return "Vereskun<br /> Denis<br /> KID-22"

@app.route("/random")
def pick_number():
    number = random.randint(1, 10)
    return render_template("random.html", number=number)

@app.cli.command("initdb")
def init_db():
    """Clear existing data and create new tables."""
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with app.open_resource("schema.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Initialized the database.")
    
@app.cli.command('populate')
def populate_db():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with app.open_resource("populate.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Populated DB with sample data.")

@app.route("/browse")
def browse():
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rowlist = cursor.fetchall()
    return render_template('browse.html', entries=rowlist)


### Start flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)