import bcrypt
import mysql.connector
import base64
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        val = (name, email, phone, hashed_password)
        print(name, email, phone, hashed_password)
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin",database="projectsmile"
            )


            mycursor = mydb.cursor()

            sql = "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)"
            val = (name, email, phone, hashed_password)
            mycursor.execute(sql, val)

            mydb.commit()
            mycursor.close()
            mydb.close()
            print(name, email, phone, hashed_password)
            return redirect(url_for('login'))  # Redirect to login page or other success page
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            # return render_template('error.html', error_message=str(err))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] 


        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="projectsmile"
        )

        mycursor = mydb.cursor()


        # Check if user exists
        sql = "SELECT * FROM users WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)

        user = mycursor.fetchone()

        if user:
            hashed_password = user[4]
            # print(hashed_password)
            # print(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))  # Assuming password is at index 4 (id,name, email, phone, password)
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # Successful login, redirect to dashboard or other page
                return render_template('home.html')
            else:
                return render_template('error.html')
        else:
            return redirect(url_for('register'))  # Redirect to registration page

    return render_template('login.html')

@app.route('/capture', methods=['POST'])
def capture_image():
    image_data = request.json['imageData']

    # Decode the base64 image data
    image_bytes = base64.b64decode(image_data.split(',')[1])

    # Store the image in the database (adjust for your database)
    # ... (database connection and insertion logic)

    return jsonify({'message': 'Image captured and stored successfully'})


if __name__== '__main__':
    app.run(debug=True)