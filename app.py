import bcrypt
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

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

            return redirect(url_for('login'))  # Redirect to login page or other success page
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return render_template('error.html', error_message=str(err))

    return render_template('register.html')

if __name__== '__main__':
    app.run(debug=True)