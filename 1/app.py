from flask import Flask, render_template, request
import sqlite3
from werkzeug.utils import secure_filename
import os
import random

upload = 'static'
allow_extensions = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['upload'] = upload


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/find')
def find():
   return render_template('find.html')

@app.route('/delete')
def delete():
   return render_template('delete.html')

@app.route('/updatedetails')
def updatedetails():
   return render_template('updatedetails.html')

@app.route('/addpicture')
def addpicture():
   return render_template('addpicture.html')

@app.route('/searchsalary')
def searchsalary():
   return render_template('searchsalary.html')

@app.route('/addnew')
def addnew():
   return render_template('addnew.html')

@app.route('/people', methods=['POST','GET'])
def allpeople():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q="Select * from people"
    cur.execute(q)
    rows = cur.fetchall()
    conn.close()
    return render_template("allpeople.html",rows = rows)

@app.route('/retrivenullsal', methods=['POST','GET'])
def retrivenullsal():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q="Select * from people where salary is null or trim(salary) = ''"
    cur.execute(q)
    rows = cur.fetchall()
    conn.close()
    return render_template("allpeople.html",rows = rows)

@app.route('/searchaction', methods=['POST','GET'])
def searchforpeople():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    field=request.form['name']
    q="Select * from people WHERE UPPER(name) =  '"+field.upper()+"' "
    cur.execute(q)
    rows = cur.fetchall()
    conn.close()
    return render_template("allpeople.html",rows = rows)

@app.route('/getDetails', methods=['POST','GET'])
def getDetails():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    field=request.form['name']
    q="Select * from people WHERE UPPER(name) =  '"+field.upper()+"' "
    cur.execute(q)
    rows = cur.fetchall()
    conn.close()
    return render_template("updatepeople.html",rows = rows)

@app.route('/deletePerson', methods=['POST','GET'])
def deletePerson():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    name=request.form['name']
    query="Delete from people WHERE UPPER(name) =  '"+name.upper()+"' "
    cur.execute(query)
    conn.commit()
    q2="Select * from people"
    cur.execute(q2)
    rows = cur.fetchall()
    conn.close()
    return render_template("allpeople.html",rows = rows)


@app.route('/getSalaryRange', methods=['POST','GET'])
def getSalaryRange():
    if (request.method=='POST'):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        minsalary=request.form['minsal']
        maxsalary = request.form['maxsal']
        if not minsalary:
            minsalary = 0
        q1="Select * from people WHERE cast(salary as double) BETWEEN @minsal AND @maxsal and salary is not null and trim(salary)!=''"
        cur.execute(q1,{'minsal':minsalary,'maxsal':maxsalary})
        rows = cur.fetchall()
        conn.close()
    return render_template("allpeople.html",rows = rows)

@app.route('/updateFormDetails', methods=['POST','GET'])
def updateFormDetails():
    if (request.method=='POST'):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        nm=request.form['name']
        st = request.form['state']
        sal = request.form['salary']
        gd = request.form['grade']
        rm = request.form['room']
        tn = request.form['telnum']
        kw = request.form['keywords']
        q="Update people set state='"+st.upper()+"', salary = '"+sal+"', grade = '"+gd+"', room = '"+rm+"', telnum = '"+tn+"', keywords = '"+kw+"' WHERE UPPER(name) =  '"+nm.upper()+"' "
        cur.execute(q)
        conn.commit()
        q2="Select * from people"
        cur.execute(q2)
        rows = cur.fetchall()
        conn.close()
    return render_template("allpeople.html",rows = rows)

def allow_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allow_extensions
@app.route('/addnewperson', methods=['GET', 'POST'])
def addnewperson():
    if (request.method=='POST'):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        nm= request.form['name']
        st= request.form['state']
        sal= request.form['salary']
        gd= request.form['grade']
        rm= request.form['room']
        tn= request.form['telnum']
        kw= request.form['keywords']
        # source https://stackoverflow.com/a/44926557 for file upload
        file = request.files['pict']
        q4 = "Select * from people WHERE UPPER(name) =  '"+nm.upper()+"' "
        cur.execute(q4)
        rows2 = cur.fetchall()
        if len(nm.strip())==0:
            return '<h1>NAME CANNOT BE BLANK</h1> <a href="/addnew">BACK</a>'
        if (len(rows2)==0):
            if file and allow_file(file.filename):
                filename = secure_filename(file.filename)
                q3 = "Select * from people where UPPER(picture) = '"+filename.upper()+"'"
                cur.execute(q3)
                rows1 = cur.fetchall()
                if(len(rows1)>0):
                    x = filename.rsplit('.', 1)[0]
                    r = random.randint(1, 100000000)
                    newFileName = x+str(r)+'.' + filename.rsplit('.', 1)[1].lower()
                    filename = newFileName
                file.save(os.path.join(app.config['upload'], filename))
            if file and not allow_file(file.filename):
                return '<h1>FILE TYPE NOT ALLOWED. PLEASE UPLOAD PNG, JPG, JPEG OR GIF FILES ONLY</h1> <a href="/addnew">GO BACK</a>'
            if not file:
                filename = ''
            q="INSERT INTO people VALUES (@name,@state,@salary,@grade,@room,@telnum,@pic,@keywords)"
            cur.execute(q,{'name':nm,'state':st,'salary':sal,'grade':gd,'room':rm,'telnum':tn,'pic':filename,'keywords':kw})
            conn.commit()
            q2="select * from people"
            cur.execute(q2)
            rows = cur.fetchall()
            conn.close()
            return render_template("allpeople.html",rows = rows)
        else:
            return '<p>PERSON ALREADY EXSISTS</p> <a href="/addnew">TRY AGAIN</a>'

@app.route('/addnewpicture', methods=['GET', 'POST'])
def addnewpicture():
    if (request.method=='POST'):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        name= request.form['name']
        file = request.files['pict']
        if file and allow_file(file.filename):
            filename = secure_filename(file.filename)
            q3 = "Select * from people where UPPER(picture) = '"+filename.upper()+"'"
            cur.execute(q3)
            rows1 = cur.fetchall()
            if(len(rows1)>0):
                x = filename.rsplit('.', 1)[0]
                r = random.randint(1, 100000000)
                newFileName = x+str(r)+'.' + filename.rsplit('.', 1)[1].lower()
                filename = newFileName
            file.save(os.path.join(app.config['upload'], filename))
        if not allow_file(file.filename):
            return '<p>FILE TYPE NOT ALLOWED. PLEASE UPLOAD PNG, JPG, JPEG OR GIF FILES ONLY</p> <a href="/addpic">GO BACK</a>'
        q="Update people set picture = @pic WHERE UPPER(name) =  '"+name.upper()+"' "
        cur.execute(q,{'pic':filename})
        conn.commit()
        q2="select * from people"
        cur.execute(q2)
        rows = cur.fetchall()
        conn.close()
    return render_template("allpeople.html",rows = rows)

if __name__ == '__main__':
    app.debug=False
    app.run()
    