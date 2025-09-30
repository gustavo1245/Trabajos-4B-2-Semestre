from base.models.travel_plan_model import TravelPlan
from base.models.usuario_model import Usuario
from flask import render_template, redirect, request, session, Blueprint, flash

bp = Blueprint('citas', __name__, url_prefix='/citas')

@bp.route('/')
def citas_simple():
    if 'usuario_id' not in session:
        return redirect('/')
    
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    
    return render_template('citas_simple.html', usuario=usuario)

@bp.route('/crear_plan', methods=['POST'])
def crear_plan_viaje():
    if 'usuario_id' not in session:
        return redirect('/')
    
    if not TravelPlan.validar_plan_viaje(request.form):
        return redirect('/citas')
    
    data = {
        'destination': request.form['destination'],
        'travel_start_date': request.form['travel_start_date'],
        'travel_end_date': request.form['travel_end_date'],
        'plan': request.form['plan'],
        'autor_id': session['usuario_id']
    }
    
    TravelPlan.crear_plan_viaje(data)
    flash("¡Plan de viaje creado exitosamente! 🌟", 'success')
    return redirect('/citas')

@bp.route('/descripcion/<int:plan_id>')
def descripcion_viaje(plan_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    plan = TravelPlan.obtener_por_id(plan_id)
    
    if not plan:
        flash("Plan de viaje no encontrado", 'error')
        return redirect('/citas')
    
    usuarios_unidos = TravelPlan.obtener_usuarios_unidos_al_plan(plan_id)
    
    return render_template('descripcion_viaje.html', 
                         usuario=usuario, 
                         plan=plan, 
                         usuarios_unidos=usuarios_unidos)

@bp.route('/unirse/<int:plan_id>')
def unirse_a_plan(plan_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    TravelPlan.unirse_a_plan(session['usuario_id'], plan_id)
    flash("¡Te has unido al viaje! 🎒", 'success')
    return redirect('/citas')

@bp.route('/cancelar_participacion/<int:plan_id>')
def cancelar_participacion(plan_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    TravelPlan.cancelar_participacion(session['usuario_id'], plan_id)
    flash("Has cancelado tu participación en el viaje", 'info')
    return redirect('/citas')

@bp.route('/eliminar_plan/<int:plan_id>')
def eliminar_plan(plan_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    TravelPlan.eliminar_plan(plan_id)
    flash("Plan de viaje eliminado", 'warning')
    return redirect('/citas')

@bp.route('/perfil')
def ver_perfil():
    if 'usuario_id' not in session:
        return redirect('/')
    
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)



