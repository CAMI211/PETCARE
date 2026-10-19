from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'mascotas.json'

# Función para cargar datos desde el archivo JSON
def cargar_mascotas():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Función para guardar datos en el archivo JSON
def guardar_mascotas(mascotas):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(mascotas, f, ensure_ascii=False, indent=4)

# 1. Ruta Inicio
@app.route('/')
def inicio():
    return render_template('inicio.html')

# 2. Ruta Lista de Mascotas (LEER)
@app.route('/mascotas')
def ver_mascotas():
    mascotas = cargar_mascotas()
    return render_template('mascotas.html', mascotas=mascotas)

# 3. Ruta Registrar Mascota (CREAR)
@app.route('/registro', methods=['GET', 'POST'])
def registrar_mascota():
    if request.method == 'POST':
        mascotas = cargar_mascotas()
        
        nuevo_id = len(mascotas) + 1
        
        nueva_mascota = {
            'id': nuevo_id,
            'nombre': request.form.get('nombre'),
            'raza': request.form.get('raza'),
            'edad': request.form.get('edad'),
            'dueño': request.form.get('dueño'),
            'peso': request.form.get('peso', 'No registrado'),
            'vacunas': request.form.get('vacunas', 'Sin registro')
        }
        
        mascotas.append(nueva_mascota)
        guardar_mascotas(mascotas)
        return redirect(url_for('ver_mascotas'))
        
    return render_template('registro.html')

# 4. Ruta Eliminar Mascota (ELIMINAR)
@app.route('/eliminar/<int:id_mascota>')
def eliminar_mascota(id_mascota):
    mascotas = cargar_mascotas()
    mascotas = [m for m in mascotas if m['id'] != id_mascota]
    guardar_mascotas(mascotas)
    return redirect(url_for('ver_mascotas'))

# 5. Ruta Vacunas y Salud
@app.route('/vacunas')
def vacunas():
    mascotas = cargar_mascotas()
    return render_template('vacunas.html', mascotas=mascotas)

if __name__ == '__main__':
    app.run(debug=True)
