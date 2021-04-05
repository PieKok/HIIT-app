import csv
import sqlite3

connection = sqlite3.connect(" exerciseDB.db")
cursor = connection.cursor()
cursor.execute(" CREATE TABLE exercises (name, category, equipment);")

with open('exerciseDB.csv') as file:
    dicRead = csv.DictReader(file)
    to_db = [ (item['name'], item['category'], item['equipment']) for item in dicRead ]

cursor.executemany("INSERT INTO exercises (name, category, equipment) VALUES (?, ?, ?);",to_db)
connection.commit()
connection.close()