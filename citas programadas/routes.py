
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Appointment
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.calendar'))
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.calendar'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        errors = []
        if User.query.filter_by(username=username).first():
            errors.append('El nombre de usuario ya existe.')
        if User.query.filter_by(email=email).first():
            errors.append('El correo ya está registrado.')
        if password != confirm:
            errors.append('Las contraseñas no coinciden.')
        if len(password) < 6:
            errors.append('La contraseña debe tener al menos 6 caracteres.')
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html')
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Hola {username}", 'success')
        login_user(new_user)
        return redirect(url_for('main.calendar'))
    return render_template('register.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('main.login'))

@main.route('/calendar')
@login_required
def calendar():
    appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.date).all()
    now = datetime.now()
    return render_template('calendar.html', appointments=appointments, now=now)

# Aquí irán las rutas para agregar, editar y eliminar citas

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_appointment():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date_str = request.form['date']
        try:
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Formato de fecha inválido.', 'danger')
            return render_template('add_appointment.html')
        if date <= datetime.now():
            flash('La fecha debe ser futura.', 'danger')
            return render_template('add_appointment.html')
        new_appointment = Appointment(title=title, description=description, date=date, user_id=current_user.id)
        db.session.add(new_appointment)
        db.session.commit()
        flash('Cita agregada correctamente.', 'success')
        return redirect(url_for('main.calendar'))
    return render_template('add_appointment.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.user_id != current_user.id:
        flash('No tienes permiso para editar esta cita.', 'danger')
        return redirect(url_for('main.calendar'))
    if appointment.status != 'pendiente' or appointment.date <= datetime.now():
        flash('Solo puedes editar citas pendientes y futuras.', 'danger')
        return redirect(url_for('main.calendar'))
    if request.method == 'POST':
        appointment.title = request.form['title']
        appointment.description = request.form['description']
        date_str = request.form['date']
        try:
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Formato de fecha inválido.', 'danger')
            return render_template('edit_appointment.html', appointment=appointment)
        if date <= datetime.now():
            flash('La fecha debe ser futura.', 'danger')
            return render_template('edit_appointment.html', appointment=appointment)
        appointment.date = date
        db.session.commit()
        flash('Cita actualizada correctamente.', 'success')
        return redirect(url_for('main.calendar'))
    return render_template('edit_appointment.html', appointment=appointment)

@main.route('/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.user_id != current_user.id:
        flash('No tienes permiso para eliminar esta cita.', 'danger')
        return redirect(url_for('main.calendar'))
    if appointment.status != 'pendiente' or appointment.date <= datetime.now():
        flash('Solo puedes eliminar citas pendientes y futuras.', 'danger')
        return redirect(url_for('main.calendar'))
    if request.method == 'POST':
        db.session.delete(appointment)
        db.session.commit()
        flash('Cita eliminada correctamente.', 'success')
        return redirect(url_for('main.calendar'))
    return render_template('delete_appointment.html', appointment=appointment)
