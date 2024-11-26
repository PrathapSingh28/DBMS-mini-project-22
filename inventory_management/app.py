from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "inventory_secret_key"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pspspsps'
app.config['MYSQL_DB'] = 'inventory_db'
mysql = MySQL(app)

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Product List Page
@app.route('/products')
def product_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('product_list.html', products=products)

# Add Product Page
@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (product_id, name, price, quantity, description) VALUES (%s, %s, %s, %s, %s)",
                    (product_id, name, price, quantity, description))
        mysql.connection.commit()
        cur.close()
       
        return redirect('/products')

    return render_template('add_product.html')

# Edit Product Page
@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE product_id = %s", [product_id])
    product = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE products 
            SET name = %s, price = %s, quantity = %s, description = %s 
            WHERE product_id = %s
        """, (name, price, quantity, description, product_id))
        mysql.connection.commit()
        cur.close()
       
        return redirect('/products')

    return render_template('edit_product.html', product=product)

# Delete Product
@app.route('/products/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE product_id = %s", [product_id])
    mysql.connection.commit()
    cur.close()

    return redirect('/products')

# Search Product
@app.route('/products/search', methods=['GET'])
def search_product():
    query = request.args.get('query')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE name LIKE %s", [f"%{query}%"])
    products = cur.fetchall()
    cur.close()
    return render_template('product_list.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)