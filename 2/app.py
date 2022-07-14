from flask import Flask, render_template,request
import pyodbc

server = 'server.database.windows.net'
database = 'database'
username = 'sample'
password = 'pwd@123'   
driver= '{ODBC Driver 17 for SQL Server}'

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/largeeq')
def largeeq():
   return render_template('large-eq.html')

@app.route('/distance')
def distance():
   return render_template('distance.html')

@app.route('/date-range')
def date_range():
   return render_template('date-range.html')

@app.route('/ndays')
def ndays():
   return render_template('n-days.html')

@app.route('/compare')
def compare():
   return render_template('compare.html')

@app.route('/largest-eq-radius')
def largesteqradius():
   return render_template('largest-eq-radius.html')

@app.route('/eq', methods=['POST','GET'])
def eq():
   with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * from eq")
        rows = cursor.fetchall()
        return render_template("eq-list.html",rows = rows)

@app.route('/largeeqform', methods=['POST','GET'])
def largeeqform():
   num = request.form['num'] 
   with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT top "+num+" * from eq where mag is not null and mag !='' ORDER by mag DESC")
        rows = cursor.fetchall()
        return render_template("eq-list.html",rows = rows)

@app.route('/distancefrom', methods=['POST','GET'])
def distancefrom():
   latitude = request.form['latitude']
   longitude = request.form['longitude']
   radius = request.form['radius'] 
   with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT time,latitude,longitude,depth,mag,magtype,place, (6371 * acos (cos ( radians("+latitude+") )* cos( radians( latitude ) )* cos( radians( longitude ) - radians("+longitude+") )+ sin ( radians("+latitude+") )* sin( radians( latitude ) ))) AS distance FROM eq where (6371 * acos (cos ( radians("+latitude+") )* cos( radians( latitude ) )* cos( radians( longitude ) - radians("+longitude+") )+ sin ( radians("+latitude+") )* sin( radians( latitude ) )))  < "+radius+" ORDER BY distance")
        rows = cursor.fetchall()
        return render_template("distance-eq-list.html",rows = rows)

@app.route('/compareform', methods=['POST','GET'])
def compareform():
   latitude1 = request.form['latitude1']
   longitude1 = request.form['longitude1']
   latitude2 = request.form['latitude2']
   longitude2 = request.form['longitude2']
   radius = request.form['radius'] 
   with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT time,latitude,longitude,depth,mag,magtype,place, (6371 * acos (cos ( radians("+latitude1+") )* cos( radians( latitude ) )* cos( radians( longitude ) - radians("+longitude1+") )+ sin ( radians("+latitude1+") )* sin( radians( latitude ) ))) AS distance FROM eq where (6371 * acos (cos ( radians("+latitude1+") )* cos( radians( latitude ) )* cos( radians( longitude ) - radians("+longitude1+") )+ sin ( radians("+latitude1+") )* sin( radians( latitude ) )))  < "+radius+" ORDER BY distance")
        rows1 = cursor.fetchall()
        cursor.execute("SELECT time,latitude,longitude,depth,mag,magtype,place, (6371 * acos (cos ( radians("+latitude2+") )* cos( radians( latitude ) )* cos( radians( longitude ) - radians("+longitude2+") )+ sin ( radians("+latitude2+") )* sin( radians( latitude ) ))) AS distance FROM eq where (6371 * acos (cos ( radians("+latitude2+") )* cos( radians( latitude ) )* cos( radians( longitude ) - radians("+longitude2+") )+ sin ( radians("+latitude2+") )* sin( radians( latitude ) )))  < "+radius+" ORDER BY distance")
        rows2 = cursor.fetchall()
        return render_template("compare-eq-list.html",rows1 = rows1,rows2 = rows2)

@app.route('/daterangeform', methods=['POST','GET'])
def daterangeform():
   fromDate = request.form['fromDate']
   toDate = request.form['toDate']
   magnitude = request.form['magnitude'] 
   with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * from eq where [time] BETWEEN '"+fromDate+"' and '"+toDate+"' and mag > "+magnitude+" order by time desc")
        rows = cursor.fetchall()
        return render_template("eq-list.html",rows = rows)

@app.route('/ndaysform', methods=['POST','GET'])
def ndaysform():
   ndays = request.form['ndays']
   ndays = int(ndays) - 1
   ndays = str(ndays)
   with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT  * from eq where mag BETWEEN 1 and 2 and time>=DATEADD(DAY,-"+ndays+",'2022-02-11') order by [time] DESC")
        rows1 = cursor.fetchall()
        cursor.execute("SELECT  * from eq where mag BETWEEN 2 and 3 and time>=DATEADD(DAY,-"+ndays+",'2022-02-11') order by [time] DESC")
        rows2 = cursor.fetchall()
        cursor.execute("SELECT  * from eq where mag BETWEEN 3 and 4 and time>=DATEADD(DAY,-"+ndays+",'2022-02-11') order by [time] DESC")
        rows3 = cursor.fetchall()
        cursor.execute("SELECT  * from eq where mag BETWEEN 4 and 5 and time>=DATEADD(DAY,-"+ndays+",'2022-02-11') order by [time] DESC")
        rows4 = cursor.fetchall()
        cursor.execute("SELECT  * from eq where mag BETWEEN 5 and 6 and time>=DATEADD(DAY,-"+ndays+",'2022-02-11') order by [time] DESC")
        rows5 = cursor.fetchall()
        cursor.execute("SELECT  * from eq where mag BETWEEN 6 and 7 and time>=DATEADD(DAY,-"+ndays+",'2022-02-11') order by [time] DESC")
        rows6 = cursor.fetchall()
        return render_template("ndays-range.html",rows1 = rows1,rows2 = rows2,rows3 = rows3,rows4 = rows4,rows5 = rows5,rows6 = rows6)


@app.route('/largesteqform', methods=['POST','GET'])
def largesteqform():
   latitude = request.form['latitude']
   longitude = request.form['longitude']
   radius = request.form['radius'] 
   with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT top(1) time,latitude,longitude,depth,mag,magtype,place, (6371 * acos (cos ( radians("+latitude+") )* cos( radians( latitude ) )* cos( radians( longitude ) - radians("+longitude+") )+ sin ( radians("+latitude+") )* sin( radians( latitude ) ))) AS distance FROM eq where (6371 * acos (cos ( radians("+latitude+") )* cos( radians( latitude ) )* cos( radians( longitude ) - radians("+longitude+") )+ sin ( radians("+latitude+") )* sin( radians( latitude ) )))  < "+radius+" ORDER BY mag DESC")
        rows = cursor.fetchall()
        return render_template("distance-eq-list.html",rows = rows)


if __name__ == '__main__':
    app.run()
    