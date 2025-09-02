from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///citas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, User, Appointment
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Importar y registrar el Blueprint de rutas
from routes import main
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
