import pyotp  # genera contraseñas de un solo uso
import sqlite3  # base de datos para nombres de usuario/contraseñas
import hashlib  # hashes seguros y resúmenes de mensajes
import uuid  # para crear identificadores únicos universales
from flask import Flask, request

app = Flask(__name__)  # Crea una instancia de la aplicación Flask

db_name = 'test.db'  # Nombre de la base de datos SQLite

@app.route('/')
def index():
    return '¡Bienvenido a la parte 3 del examen transversal!'  # Devuelve un mensaje de bienvenida en la ruta principal ("/")

@app.route('/signup/v2', methods=['GET', 'POST'])
def signup_v2():
    conn = sqlite3.connect(db_name)  # Conecta a la base de datos SQLite
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
           (USERNAME  TEXT    PRIMARY KEY NOT NULL,
            HASH      TEXT    NOT NULL);''')  # Crea una tabla en la base de datos si no existe
    conn.commit()
    try:
        # Genera el hash de la contraseña proporcionada por el usuario utilizando el algoritmo SHA-256
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        # Inserta el nombre de usuario y el hash de la contraseña en la tabla USER_HASH
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) "
                  "VALUES ('{0}', '{1}')".format(request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El nombre de usuario ya está registrado."  # Devuelve un mensaje de error si el nombre de usuario ya está registrado
    print('username: ', request.form['username'], ' password: ', request.form['password'], ' hash: ', hash_value)
    return "Registro exitoso"  # Devuelve un mensaje de éxito si el registro se realiza correctamente

def verify_hash(username, password):
    conn = sqlite3.connect(db_name)  # Conecta a la base de datos SQLite
    c = conn.cursor()
    query = "SELECT HASH FROM USER_HASH WHERE USERNAME = '{0}'".format(username)
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == hashlib.sha256(password.encode()).hexdigest()

@app.route('/login/v2', methods=['GET', 'POST'])
def login_v2():
    error = None
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            error = 'Inicio de sesión exitoso'  # Mensaje de éxito si la verificación del hash es correcta
        else:
            error = 'Nombre de usuario/contraseña no válidos'  # Mensaje de error si la verificación del hash es incorrecta
    else:
        error = 'Método no válido'  # Mensaje de error para solicitudes no válidas
    return error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9500, ssl_context='adhoc')  # Ejecuta la aplicación Flask en el host y puerto especificados con contexto SSL ad hoc