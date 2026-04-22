from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__) 

def init_database():
    conn = sqlite3.connect('inventario.db')
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            categoria INTEGER NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

init_database()


@app.route("/")
def index():
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    return render_template('index.html', productos=productos)

@app.route("/create")
def create():
    return render_template('create.html')


@app.route("/save", methods=['POST'])
def save():
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = request.form['precio']
    stock = request.form['stock']

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)
        """,(nombre, categoria, precio, stock)
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/edit/<int:id>")
def producto_edit(id):
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template('edit.html', producto=producto)

@app.route("/update", methods=['POST'])
def producto_update():
    id = request.form['id']
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = request.form['precio']
    stock = request.form['stock']

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE productos SET nombre=?, categoria=?, precio=?, stock=? WHERE id=?
        """,(nombre, categoria, precio, stock, id)
    )
    conn.commit()
    conn.close()
    return redirect("/")    

if __name__ == '__main__':
    app.run(debug=True)
