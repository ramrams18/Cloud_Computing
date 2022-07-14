# source: https://stackoverflow.com/a/2888042
import csv
import sqlite3

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE people (name, state,salary,grade,room,telnum,picture,keywords);")

with open('people.csv', 'r') as people:
    dr = csv.DictReader(people)
    to_database = [(i['Name'], i['State'], i['Salary'], i['Grade'], i['Room'],
              i['Telnum'], i['Picture'], i['Keywords']) for i in dr]

cur.executemany(
    "INSERT INTO people (name, state,salary,grade,room,telnum,picture,keywords) VALUES (?, ?,?, ?,?, ?,?, ?);", to_database)
con.commit()
con.close()
