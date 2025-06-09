from flask import Flask, render_template, request, redirect, url_for, session, jsonify

import os
import sqlite3

app = Flask(__name__)
app.secret_key =  os.environ['APP_SECRET_KEY']

ADMIN_USERNAME =  os.environ['ADMIN_USERNAME']
ADMIN_PASSWORD =  os.environ['ADMIN_PASSWORD']

@app.route('/products')
def products():
    with sqlite3.connect('store.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT case_name, price, image FROM products ")
        products = cursor.fetchall()
    return render_template('ino.html',products=products)


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin-dashboard')
        else:
            return "Incorrect login!"
    return render_template('admin.html')

@app.route('/admin-dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/admin')

    conn = sqlite3.connect('store.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        if request.method == 'POST':
            print("Form Data:", dict(request.form))

            #delete a product
            if 'delete' in request.form:
                case_name = request.form.get('case_name')
                print(case_name)
                if case_name:
                    cur.execute("DELETE FROM products WHERE case_name = ?", (case_name,))
                    conn.commit()

            #add a product
            elif 'add' in request.form:
                case_name = request.form.get('case_name')
                price = request.form.get('price')
                image = request.form.get('image')

                print( case_name, price, image)

                if case_name and price and image:
                    cur.execute(
                        "INSERT INTO products (case_name, price, image) VALUES (?, ?, ?)",
                        (case_name, int(price), image)
                    )
                    conn.commit()

        #load products and return template
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        return render_template("admin_dash.html", products=products)

    finally:
        conn.close()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('store.db')
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
        except:
            return "User already exists or error occurred"

        session['name'] = name  
        return redirect('/user')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('store.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['name'] = user['name']  
            return redirect('/user')
        else:
            return "Invalid login"
    return render_template('login.html')

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    items = data.get("items", [])

    conn = sqlite3.connect("store.db")
    cur = conn.cursor()

    for item in items:
        cur.execute("UPDATE products SET amount_sold = COALESCE(amount_sold, 0) + 1 WHERE case_name = ?", (item,))
    
    conn.commit()
    conn.close()

    return jsonify({})


@app.route('/user')
def user():
    if 'name' not in session:
        return redirect('/login')
    return render_template('user.html', name=session['name'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


@app.route('/admin-logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin')



@app.route('/')
def home():
    
    return render_template('home.html')
    
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=81)


