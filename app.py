from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Crear la base de datos y la tabla
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS butacas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            fila INTEGER,
            numero INTEGER,
            vendida BOOLEAN,
            protocolo BOOLEAN,
            balcon_numero INTEGER,
            fumadores BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa la base de datos
init_db()

# Ruta para ver el formulario inicial
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para obtener todas las butacas
@app.route('/butacas', methods=['GET'])
def get_butacas():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM butacas")
    butacas = c.fetchall()
    conn.close()
    return jsonify(butacas)

# Ruta para agregar una butaca
@app.route('/butacas', methods=['POST'])
def add_butaca():
    data = request.json
    tipo = data['tipo']
    fila = data['fila']
    numero = data['numero']
    protocolo = data.get('protocolo', False)
    balcon_numero = data.get('balcon_numero', None)
    fumadores = data.get('fumadores', False)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO butacas (tipo, fila, numero, vendida, protocolo, balcon_numero, fumadores)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (tipo, fila, numero, False, protocolo, balcon_numero, fumadores))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Butaca añadida exitosamente'})

# Ruta para eliminar una butaca
@app.route('/butacas/<int:id>', methods=['DELETE'])
def delete_butaca(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM butacas WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Butaca eliminada exitosamente'})

if __name__ == '__main__':
    app.run(debug=True)
