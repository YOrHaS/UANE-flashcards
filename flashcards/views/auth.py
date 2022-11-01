import functools
from flask import(
    Blueprint, render_template, flash, g, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flashcards.models.usuario import Usuario
from flashcards import db

#Apunta a templates
auth = Blueprint('auth', __name__, url_prefix='/auth')

#Crear usuario
@auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('usuarioNombre')
        correo = request.form.get('usuarioCorreo')
        password = request.form.get('usuarioPassword')


        user = Usuario(username, correo, generate_password_hash(password))

        error = None
        if not username:
            error = 'Se requiere nombre de usuario'
        elif not password:
            error = 'Se requiere contraseña'
        
        user_name = Usuario.query.filter_by(usuarioNombre = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login')) 
        else:
            error = f'El usuario {username} ya esta registrado'
        flash(error)
    return render_template('auth/register.html')


#Iniciar sesión
@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('usuarioNombre')
        password = request.form.get('usuarioPassword')

        error = None

        user = Usuario.query.filter_by(usuarioNombre = username).first()

        if user == None:
            error = 'Nombre incorrecto'
        elif not check_password_hash(user.usuarioPassword, password):
            error = 'Contraseña incorrecta'
      
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('mazo.index')) 
        
        flash(error)
    return render_template('auth/login.html')

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Usuario.query.get_or_404(user_id)

#Cierra sesion
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('mazo.index')) 


#Pide estar logueado
def login_required(view):
    @functools.wraps(view)
    #argumentos indefinidos
    def wrapped_view(**view_args):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**view_args)
    return wrapped_view