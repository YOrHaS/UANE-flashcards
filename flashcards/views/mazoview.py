from webbrowser import get
from flask import(
    render_template, Blueprint, flash, g, redirect, request, url_for
)
from sqlalchemy import desc
from werkzeug.exceptions import abort
import uuid

from flashcards.models.mazo import Mazo
from flashcards.models.usuario import Usuario
from flashcards.models.tarjeta import Tarjeta
from flashcards.views.auth import login_required

from flashcards import db


mazoprint = Blueprint('mazo', __name__)
tarjetaprint = Blueprint('tarjeta', __name__)


#Obtener usuario
def get_user(id):
    user = Usuario.query.get_or_404(id)
    return user  

#Mostrar mazos públicos
@mazoprint.route('/')
def index():
  
    #False significa mazo publico    
    mazos = Mazo.query.filter(Mazo.visibilidad == False).all()
    usuarios = Usuario.query.all()
        
    db.session.commit()              

    return render_template('mazo/index.html', mazos  = mazos, usuarios = usuarios) 


#Mostrar mazos propios
@mazoprint.route('/mydecks', methods = ('GET', 'POST'))
@login_required
def mydecks():
  
    mazos = Mazo.query.filter(Mazo.idUsuario == g.user.id).all()
    
        
    db.session.commit()            

    return render_template('mazo/mydecks.html', mazos  = mazos, get_user = get_user)


#Adquirir mazo
@mazoprint.route('/deck/acquire/<int:id>', methods = ('GET', 'POST'))
@login_required
def acquire(id):
    mazo = Mazo.query.filter(Mazo.id == id).first()
    if request.method == 'POST':
       
        if mazo.idUsuario != g.user.id:
           
        
            nombre = request.form.get('nombre')
            visibilidad = request.form.get('visibilidad') 

            error = None
            if not nombre:
                error = 'Se requiere nombre'

            else:           
            
                if visibilidad == 'on':
                    id_interno =  uuid.uuid1().hex
                    mazo = Mazo(g.user.id, id_interno ,  nombre, True)
                    db.session.add(mazo)
                    db.session.commit()


                    tarjetas = Tarjeta.query.filter(Tarjeta.idMazo == id).all()
                    id_nuevo = Mazo.query.filter(Mazo.idInterno == id_interno).first().id
                    

                    for tarjeta in tarjetas:
                        adelante = tarjeta.adelante
                        atras = tarjeta.atras

                        tarjeta_nueva = Tarjeta(id_nuevo, adelante, atras)
                        db.session.add(tarjeta_nueva)
                        db.session.commit()
                    
                
                else:
                    id_interno =  uuid.uuid1().hex
                    mazo = Mazo(g.user.id, id_interno ,  nombre, False)
                    db.session.add(mazo)
                    db.session.commit()

                  
                    tarjetas = Tarjeta.query.filter(Tarjeta.idMazo == id).all()
                    id_nuevo = Mazo.query.filter(Mazo.idInterno == id_interno).first().id

                    for tarjeta in tarjetas:
                        adelante = tarjeta.adelante
                        atras = tarjeta.atras

                        tarjeta_nueva = Tarjeta(id_nuevo, adelante, atras)
                        db.session.add(tarjeta_nueva)
                        db.session.commit()
                 
                return redirect(url_for('mazo.mydecks')) 
         
    return render_template('mazo/acquire.html', mazo = mazo)




#Crear mazo
@mazoprint.route('/deck/create', methods = ('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        visibilidad = request.form.get('visibilidad')

        if visibilidad == 'on':
            id_interno =  uuid.uuid1().hex
            mazo = Mazo(g.user.id, id_interno, nombre, True)
        else:
            id_interno =  uuid.uuid1().hex
            mazo = Mazo(g.user.id, id_interno, nombre, False)

        error = None
        if not nombre:
            error = 'Se requiere nombre'
        
        if error is not None:
            flash(error)
        else:
            db.session.add(mazo)
            db.session.commit()
            return redirect(url_for('mazo.mydecks')) 

        flash(error)
    return render_template('mazo/create.html')



#Obtener mazo
def get_deck(id, check_author = True):
    mazo = Mazo.query.get(id)

    if mazo is None:
        abort(404, f'ID {id} de la publicación no existe')

    if check_author and mazo.idUsuario != g.user.id:
        abort(404)
    return mazo



#Actualizar mazo
@mazoprint.route('/deck/update/<int:id>', methods = ('GET', 'POST'))
@login_required
def update(id):

    mazo = get_deck(id)
    if mazo.idUsuario == g.user.id:

        if request.method == 'POST':
            mazo.nombre = request.form.get('nombre')

            if request.form.get('visibilidad') == 'on':
                mazo.visibilidad = True
            else:
                mazo.visibilidad = False
            
            error = None
            if not mazo.nombre:
                error = 'Se requiere nombre'
            
            if error is not None:
                flash(error)
            else:
                #agrega registgro si no existe y si existe lo modifica
                db.session.add(mazo)
                db.session.commit()
                return redirect(url_for('mazo.mydecks')) 

            flash(error)
        return render_template('mazo/update.html', mazo = mazo)


#Eliminar mazo
@mazoprint.route('/deck/delete/<int:id>')
@login_required
def delete(id):
    mazo = get_deck(id)
    if mazo.idUsuario == g.user.id:
        tarjetas = Tarjeta.query.filter(Tarjeta.idMazo == id).all()
        
        for tarjeta in tarjetas:
            db.session.delete(tarjeta)
            db.session.commit()

        mazo = get_deck(id)
        db.session.delete(mazo)
        db.session.commit()

        return redirect(url_for('mazo.mydecks')) 


#Estudiar mazo
@mazoprint.route('/deck/study/<int:id>', methods = ('GET', 'POST'))
def study(id):
    if request.method == 'GET':
        #False significa mazo publico
        mazo = Mazo.query.get(id)

        #Ver mazos publicos
        if g.user is None or mazo.idUsuario != g.user.id:
            tarjetas = Tarjeta.query.filter(Tarjeta.idMazo == mazo.id).all()
        
            db.session.commit()


        #Estudiar mazo propiop
        elif mazo.idUsuario == g.user.id:
            tarjetas = Tarjeta.query.filter(Tarjeta.idMazo == mazo.id).order_by('dificultad').all()    
            db.session.commit()

        else:
           
            return redirect(url_for('mazo.index'))      

        return render_template('mazo/study.html', tarjetas = tarjetas, mazo = mazo)

    if request.method == 'POST':
        mazo = get_deck(id)
        if mazo.idUsuario == g.user.id:
            tarjetas = Tarjeta.query.filter(Tarjeta.idMazo == id).all()
          


            for tarjeta in tarjetas:
                nombredebug =  "% s" % tarjeta.id
                

                if request.form.get(nombredebug) == 'facil':
                    if tarjeta.dificultad <5:
                        tarjeta.dificultad += 1
                        db.session.add(tarjeta)
                        db.session.commit()
                    
                if request.form.get(nombredebug) == 'dificil':
                    if tarjeta.dificultad > 1:
                        tarjeta.dificultad -= 1
                        db.session.add(tarjeta)
                        db.session.commit()
        
            
            #Regresa a mydecks
            mazos = Mazo.query.filter(Mazo.idUsuario == g.user.id).all()
        
            db.session.commit()      

            return render_template('mazo/mydecks.html', mazos = mazos)
                
        