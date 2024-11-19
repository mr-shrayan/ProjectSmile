import mysql.connector

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin"
)

mycursor = mydb.cursor()

# Execute the SQL query to show all databases
mycursor.execute("SHOW DATABASES")

# Fetch all the database names
myresult = mycursor.fetchall()

# Print the database names
for x in myresult:
    print(x)

mydb.close()