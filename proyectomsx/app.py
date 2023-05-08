import json
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

# Carga los datos del archivo JSON
with open('/home/kali/Documentos/proyectomsx/msx.json', encoding='utf-8') as archivo:
    datos = json.load(archivo)

# Ruta principal para mostrar la lista de juegos
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/juegos')
def juegos():
    return render_template('juegos.html', juegos=datos)


# Ruta para mostrar un juego individual
@app.route('/juego/<id>')
def juego(id):
    for juego in datos:
        if juego['id'] == int(id):
            return render_template('juego.html', juego=juego)
    return render_template('404.html')


# Ruta para mostrar una lista filtrada por categoría
@app.route('/categoria/<categoria>')
def categoria(categoria):
    juegos_filtrados = [juego for juego in datos if juego['categoria'] == categoria]
    return render_template('juegos.html', categoria=categoria, juegos=juegos_filtrados)


# Ruta para mostrar una lista filtrada por sistema
@app.route('/sistema/<sistema>')
def sistema(sistema):
    juegos_filtrados = [juego for juego in datos if juego['sistema'] == sistema]
    return render_template('juegos.html', sistema=sistema, juegos=juegos_filtrados)

@app.route('/listajuegos', methods=['POST'])
def lista_juegos():
    nombre_juego = request.form['busqueda']
    if nombre_juego == "all":
        return render_template('listajuegos.html', datos_juegos=datos)
    else:
        juegos_encontrados = [juego for juego in datos if nombre_juego.lower() in juego['nombre'].lower()]
        if len(juegos_encontrados) == 0:
            return render_template('404.html')
        else:
            return render_template('listajuegos.html', datos_juegos=juegos_encontrados)

@app.route('/buscarjuego', methods=['POST'])
def buscar_juego():
    nombre_juego = request.form['busqueda']
    if nombre_juego == "all":
        return render_template('listajuegos.html', datos_juegos=datos)
    else:
        juego_encontrado = None
        for juego in datos:
            if juego['nombre'] == nombre_juego:
                juego_encontrado = juego
                break
        if juego_encontrado is None:
            return render_template('404.html')
        else:
            return render_template('juego.html', juego=juego_encontrado)


# Ruta para mostrar el formulario de contacto
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


# Ruta para procesar el formulario de contacto
@app.route('/contacto', methods=['POST'])
def procesar_formulario():
    # Obtener los datos del formulario
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form['mensaje']

    # Aquí se podría enviar el mensaje por correo electrónico o guardarlo en una base de datos

    # Redirigir al usuario a la página de confirmación
    return redirect(url_for('confirmacion_contacto'))


# Ruta para mostrar la página de confirmación de contacto
@app.route('/confirmacion_contacto')
def confirmacion_contacto():
    return render_template('confirmacion_contacto.html')


# Ruta por defecto para mostrar la página 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
