from flask import Flask, render_template,request
import pyodbc
import time
import random
import redis
import pickle
import hashlib
from random import randint

app = Flask(__name__)

server = 'server.database.windows.net'
database = 'database'
username = 'sample'
password = 'pwd@123'   
driver= '{ODBC Driver 17 for SQL Server}'

myHostname = "sample.redis.cache.windows.net"
myPassword = "2461237171531="

r = redis.StrictRedis(host=myHostname, port=6380,
                      password=myPassword, ssl=True)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/create')
def create():
   cxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
   cursor = cxn.cursor()
   start = time.time()
   cursor.execute("Drop table if exists t1; CREATE TABLE [dbo].[t1]( [time] [nvarchar](50) NULL,[latitude] [float] NULL,[longitude] [float] NULL,[depth] [float] NULL,[mag] [float] NULL,[magType] [nvarchar](50) NULL,[nst] [tinyint] NULL,[gap] [float] NULL,[dmin] [float] NULL,[rms] [float] NULL,[net] [nvarchar](50) NULL,[id] [nvarchar](50) NULL,[updated] [nvarchar](50) NULL,[place] [nvarchar](100) NULL,[type] [nvarchar](50) NULL,[horizontalError] [float] NULL,[depthError] [float] NULL,[magError] [float] NULL,[magNst] [bigint] NULL,[status] [nvarchar](50) NULL,[locationSource] [nvarchar](50) NULL,[magSource] [nvarchar](50) NULL);")
   end = time.time()
   exe_time = end - start
   return render_template('create.html', time=exe_time)

@app.route('/all-records', methods=['GET'])
def allrecords():
   cxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
   cursor = cxn.cursor()
   start = time.time()
   cursor.execute("SELECT * FROM a3")
   rows = cursor.fetchall()
   end = time.time()
   exe_time = end - start
   return render_template('all-records.html', rows=rows, time=exe_time)

@app.route('/randomnum')
def randomnum():
   return render_template('randomnum.html')

@app.route('/restrictedset')
def restrictedset():
   return render_template('restrictedset.html')

@app.route('/randomnumredis')
def randomnumredis():
   return render_template('randomnum-redis.html')

@app.route('/restrictedsetredis')
def restrictedsetredis():
   return render_template('restrictedset-redis.html')

@app.route('/randomnumform', methods=['GET',"POST"])
def randomnumform():
   cxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
   cursor = cxn.cursor()
   randnum = int(request.form['randnum'])
   queryList=[]
   q1 = "SELECT TOP 1000 * from a3"
   q2 = "SELECT top 5000 * from a3"
   q3 = "SELECT * from a3"
   q4 = "SELECT top 9000 * from a3 order by time desc"
   queryList.append(q1)
   queryList.append(q2)
   queryList.append(q3)
   queryList.append(q4)
   rowsList = []
   start = time.time()
   for i in range(0, randnum):
      rand_index = randint(0, len(queryList)-1)
      cursor.execute(queryList[rand_index])
      # rows = cursor.fetchall()
      # rowsList.append(rows)
   end = time.time()
   exe_time = end - start
   return render_template('randomnum.html', time=exe_time)

@app.route('/restrictedsetform', methods=['GET',"POST"])
def restrictedsetform():
   cxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
   cursor = cxn.cursor()
   randnum = int(request.form['randnum'])
   minmag = float(request.form['minmag'])
   maxmag = float(request.form['maxmag'])
   rowsList = []
   start = time.time()
   for i in range(0, randnum):
      mag= round(random.uniform(minmag, maxmag),2)
      q="SELECT * from a3 where mag > "+str(mag)
      cursor.execute(q)
      # rows = cursor.fetchall()
      # rowsList.append(rows)
   end = time.time()
   exe_time = end - start
   return render_template('restrictedset.html', time=exe_time)

@app.route('/randomnumredisform', methods=['GET',"POST"])
def randomnumredisform():
   cxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
   cursor = cxn.cursor()
   randnum = int(request.form['randnum'])
   queryList=[]
   q1 = "SELECT TOP 1000 * from a3"
   q2 = "SELECT top 5000 * from a3"
   q3 = "SELECT * from a3"
   q4 = "SELECT top 9000 * from a3 order by time desc"
   queryList.append(q1)
   queryList.append(q2)
   queryList.append(q3)
   queryList.append(q4)
   l= len(queryList)
   start = time.time()
   for i in range(0, randnum):
      rand_index = randint(0, l-1)
      query = queryList[rand_index]
      key = hashlib.sha224(query.encode('utf-8')).hexdigest()
      if (r.get(key)):
         print("redis cached " + str(i))
      else:
         cursor.execute(query)
         data = cursor.fetchall()
         # rows = []
         # for j in data:
         #    rows.append(str(j))  
         # Put data into cache for 1 hour
         r.set(key, pickle.dumps(data) )
         r.expire(key, 3600)
      # cursor.execute(query)
   end = time.time()
   exe_time = end - start
   return render_template('randomnum-redis.html', time=exe_time)

@app.route('/restrictedsetredisform', methods=['GET',"POST"])
def restrictedsetredisform():
   cxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
   cursor = cxn.cursor()
   randnum = int(request.form['randnum'])
   minmag = float(request.form['minmag'])
   maxmag = float(request.form['maxmag'])
   start = time.time()
   for i in range(0, randnum):
      mag= round(random.uniform(minmag, maxmag),2)
      q="SELECT * from a3 where mag > "+str(mag)
      key = hashlib.sha224(q.encode('utf-8')).hexdigest()
      if (r.get(key)):
         print("redis cached " + str(i))
      else:
         cursor.execute(q)
         data = cursor.fetchall()
         r.set(key, pickle.dumps(data) )
         r.expire(key, 3600)
   end = time.time()
   exe_time = end - start
   return render_template('restrictedset-redis.html', time=exe_time)


if __name__ == '__main__':
    app.run()
    