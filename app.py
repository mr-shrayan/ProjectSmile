from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']


        # Here, you would typically store this information in a database
        # ... database operations ...

        return redirect(url_for('login'))  # Redirect to login page or other success page

    return render_template('register.html')