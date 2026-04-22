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


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
