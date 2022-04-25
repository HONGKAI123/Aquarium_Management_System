import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="aq_admin@localhost",
  password="aq_Password01!"
)

print(mydb)