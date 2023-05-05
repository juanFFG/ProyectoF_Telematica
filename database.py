import flask
import pandas as pd
import sqlite3

app = flask.Flask(__name__)

def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT)''')

    # Agregar el usuario "juan" con contraseña "12345"
    c.execute('''INSERT OR IGNORE INTO users (username, password)
                 VALUES (?, ?)''', ('juan', '12345'))

    conn.commit()
    conn.close()

def insert_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password)
                 VALUES (?, ?)''', (username, password))
    conn.commit()
    conn.close()

def find_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users
                 WHERE username=? AND password=?''', (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

@app.route('/enviar_usuarios')
def enviar_usuarios():
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * from users", conn)
    conn.close()

    # Convertir el DataFrame a una lista de diccionarios
    usuarios = df.to_dict('records')

    # Retornar la lista de usuarios como un objeto JSON
    return flask.jsonify(usuarios)


if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8080)
