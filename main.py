from flask import Flask, render_template, request, Response, flash, redirect,url_for
from time import sleep
import math,random,json,logging,copy,time,socket,sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/addBookPage')
def addBookPage():
    return render_template("add.html")

@app.route('/searchBookPage')
def searchBookPage():
    return render_template("search.html")

@app.route('/addBook',methods = ['POST'])
def addBook():
    error = ''
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    if request.method == 'POST':
        data = request.get_json()
        tag = generateTag(5)

        if data['title'] !='' and data['authors'] != ['']:
            sqlQ = "INSERT INTO Book VALUES ('"+data['title']+"','"+tag + "','" + data['year'] + "')"
            try:
                cur.execute(sqlQ)
                con.commit()
            except Exception as e:
                error = str(e)

            if error =='':
                for i in range(len(data['authors'])):
                    sqlQ = "INSERT INTO Written VALUES ('"+data['authors'][i]+"','"+ tag + "')"
                    try:
                        cur.execute(sqlQ)
                        con.commit()
                    except Exception as e:
                        error = str(e)
        else:
            error="Please include book title and atleast one author name"

        # print(error)
        return {'error':error}

@app.route('/searchBook',methods = ['POST'])
def searchBook():
    error = ''
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    if request.method == 'POST':
        data = request.get_json()

        try:
            sqlQ = "CREATE VIEW IF NOT EXISTS a AS select * from Book NATURAL JOIN Written"
            select = "SELECT * FROM a WHERE True"
            cur.execute(sqlQ)
            con.commit()
            if (data['author'] !=''):
                select += "AND author='"+data['author']+"'"
            if (data['start'] != ''):
                select += "AND year>='"+data['start']+"'"
            if (data['end'] != ''):
                select += "AND year>='"+data['end']+"'"

            print(select)

            cur.execute(select)
            con.commit()
            sqlQ = "SELECT * FROM a"
            rows = cur.execute(sqlQ).fetchall()
            print(rows);
        except Exception as e:
            error = str(e)

        return {'error':error}


def generateTag(len):
    s = ""
    for i in range(len):
        if random.random() > 0.5:
            s += chr(random.randint(65,90))
        else:
            s += chr(random.randint(98,122))
    return s

def sendSQL(command):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    return cur.execute(command).fetchall()

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    #log.setLevel(logging.ERROR)

    con = sqlite3.connect("database.db")
    cur = con.cursor()
    sqlQ = """
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS Book
    (
        title TEXT NOT NULL UNIQUE,
    	id VARCHAR(5) PRIMARY KEY,
    	year INTEGER,
    	CONSTRAINT score_validate CHECK(year >= 1400)
    )

    CREATE TABLE IF NOT EXISTS Written
    (
        author TEXT,
        id VARCHAR(5),
        FOREIGN KEY (id) REFERENCES Book (id)
    )
"""
    sqlQ = sqlQ.split("\n\n")
    for q in sqlQ:
        cur.execute(q)

    app.config['SECRET_KEY'] = generateTag(10)

    IPAddr=socket.gethostbyname(socket.gethostname())

    app.run(host='0.0.0.0', port=81,debug=True, use_debugger=True,use_reloader=False)
