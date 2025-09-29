from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)

# Clave para manejar sesiones en Flask
app.secret_key = "clave_secreta"

# Ruta principal que muestra el formulario para ingresar datos

@app.route('/')
def index():
   return render_template('index.html')


# Ruta para enviar los datos del formulario y almacenarlos en sesión
@app.route('/enviar', methods=['POST'])
def enviar():
    session['nombre'] = request.form.get('nombre')
    session['edad'] = request.form.get('edad')
    session['color'] = request.form.get('color')
    session['animal'] = request.form.get('animal')
    return redirect('/futuro')

# Ruta para mostrar la predicción del futuro basada en los datos ingresados
@app.route('/futuro')
def futuro():
    mensajes = [
        "¡Hoy tendrás mucha suerte y alegría!",
        "Prepárate, algo inesperado te sorprenderá.",
        "Un nuevo amigo aparecerá en tu vida.",
        "Ten cuidado, podrías perder algo importante.",
        "La fortuna te sonríe, aprovecha las oportunidades.",
        "Hoy no es tu mejor día, pero mañana será mejor."
    ]
    mensaje = random.choice(mensajes)
    nombre = session.get('nombre', '')
    edad = session.get('edad', '')
    color = session.get('color', '')
    animal = session.get('animal', '')
    return render_template('futuro.html', nombre=nombre, edad=edad, color=color, animal=animal, mensaje=mensaje)

if __name__ == "__main__":
   app.run(debug=True)