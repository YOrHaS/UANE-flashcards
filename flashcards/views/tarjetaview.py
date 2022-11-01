from webbrowser import get
from flask import(
    render_template, Blueprint, flash, g, redirect, request, url_for
)

from werkzeug.exceptions import abort

from flashcards.models.mazo import Mazo
from flashcards.models.usuario import Usuario
from flashcards.models.tarjeta import Tarjeta

from flashcards.views.auth import login_required

from flashcards import db
from flashcards.views.mazoview import get_deck



mazoprint = Blueprint('mazo', __name__)
tarjetaprint = Blueprint('tarjeta', __name__)



#Crear tarjeta
@tarjetaprint.route('/card/create/<int:id>', methods = ('GET', 'POST'))
@login_required
def create_card(id):
    if request.method == 'POST':
        mazo = Mazo.query.get(id)
        
        if mazo.idUsuario == g.user.id:
            adelante = request.form.get('adelante')
            atras = request.form.get('atras')

            error = None

            if not adelante:
                error = "Falta un texto adelante"

            elif not atras:
                
                error = "Falta un texto atras"


            if error is None:

                tarjeta = Tarjeta(id, adelante, atras)

                db.session.add(tarjeta)
                db.session.commit()
            
            if error is not None:
            
                flash(error)
            
    return render_template('tarjeta/create_card.html')

    
#Mostrar tarjetas propias
@tarjetaprint.route('/mycards', methods = ('GET', 'POST'))
@login_required
def mycards():
    mazos = Mazo.query.filter(Mazo.idUsuario == g.user.id).all()
    ids =[]
    for mazo in mazos:

        ids.append(mazo.id)
    
    TT =[]
    for id in ids:
        tarjetas = Tarjeta.query.filter(Tarjeta.idMazo == id).all()    
        for tarjeta in tarjetas:
            TT.append(tarjeta)

       

    db.session.commit()
               

    return render_template('tarjeta/mycards.html', tarjetas  = TT, mazos = mazos) # get_user = get_user


#Obtener mazo
def get_card(id):
    tarjeta = Tarjeta.query.get(id)    
    return tarjeta



#Actualizar tarjeta
@tarjetaprint.route('/card/update/<int:id>', methods = ('GET', 'POST'))
@login_required
def update_card(id):

    tarjeta = get_card(id)
    id_mazo = tarjeta.idMazo
    mazo = get_deck(id_mazo)

    if request.method == 'POST':
        if mazo.idUsuario == g.user.id:
            tarjeta.adelante = request.form.get('adelante')
            tarjeta.atras = request.form.get('atras')

            
            error = None
            if not tarjeta.adelante:
                error = 'Se requiere nombre'
            
            if error is not None:
                flash(error)
            else:
                #agrega registgro si no existe y si existe lo modifica
                db.session.add(tarjeta)
                db.session.commit()
                return redirect(url_for('tarjeta.mycards')) 

            flash(error)
    return render_template('tarjeta/update_card.html', tarjeta = tarjeta)


#Eliminar mazo
@tarjetaprint.route('/card/delete/<int:id>')
@login_required
def card_delete(id):
    tarjeta = get_card(id)
    id_mazo = tarjeta.idMazo
    mazo = get_deck(id_mazo)
    if mazo.idUsuario == g.user.id:
        db.session.delete(tarjeta)
        db.session.commit()

        return redirect(url_for('tarjeta.mycards'))