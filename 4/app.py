from flask import Flask, render_template,request
import pyodbc

app = Flask(__name__)

server = 'server.database.windows.net'
database = 'database'
username = 'sample'
password = 'pwd@123'   
driver= '{ODBC Driver 17 for SQL Server}'


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/piechart')
def pie():
   cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
   cursor = cnxn.cursor()
   data = []
   for i in range(-1,5):
      query = "select count(*) from a3 where mag between " + str(i) + " and " + str(i+1)
      cursor.execute(query)
      rows = cursor.fetchall()
      y = str(i)+" to "+ str(i+1),rows[0][0]
      data.append(y)
   return render_template('piechart.html', rows=data)

@app.route('/magvsdept')
def magvsdep():
   cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
   cursor = cnxn.cursor()
   query = "select top(100) depth,mag from a3 order by time desc"
   cursor.execute(query)
   rows = cursor.fetchall()
   return render_template('magvsdept.html', rows=rows)

   
if __name__ == '__main__':
    app.run()
    