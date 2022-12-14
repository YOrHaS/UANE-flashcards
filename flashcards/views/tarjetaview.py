from webbrowser import get
from flask import(
    render_template, Blueprint, flash, g, redirect, request, url_for)

from werkzeug.exceptions import abort
from requests_html import AsyncHTMLSession

from flashcards.models.mazo import Mazo
from flashcards.models.usuario import Usuario
from flashcards.models.tarjeta import Tarjeta

from flashcards.views.auth import login_required

from flashcards import db
from flashcards.views.mazoview import get_deck

import re


mazoprint = Blueprint('mazo', __name__)
tarjetaprint = Blueprint('tarjeta', __name__)


#Webscraper create card
@tarjetaprint.route("/card/createauto/<int:id>/", methods=['GET', 'POST'])
async def searchdef(id):
        if request.method == 'POST':

            diccionario = request.form.get('diccionario')
            result = ""
            word = ""

            if diccionario == 'CDIE':
        
                word = request.form.get('searched')
                word = word.strip()
                word = re.sub(' +', '-', word)
                
                #Crear sesión
                session = AsyncHTMLSession()
                
                #Definir URL
                url = "https://dictionary.cambridge.org/es/diccionario/ingles-espanol/" + word
                
                
                r = await session.get(url)
                
                r.html.arender(sleep=1, keep_page=True, scrolldown=1)

                pronunciacion = r.html.find('div.pr.entry-body__el span.ipa.dipa', first=True) 
                definicion = r.html.find('div.pr.entry-body__el  span.trans.dtrans.dtrans-se', first=True)
                ejemplo = r.html.find('div.examp.dexamp', first=True)
              
                
                if pronunciacion is not None:
                    result = pronunciacion.text + "\n" +definicion.text + "\n" + ejemplo.text

            if diccionario == 'CDEI':
        
                word = request.form.get('searched')
                word = word.strip()
                word = re.sub(' +', '-', word)
                
                #Crear sesión
                session = AsyncHTMLSession()
                
                #Definir URL
                url = "https://dictionary.cambridge.org/es/diccionario/espanol-ingles/" + word
                
                
                r = await session.get(url)
                
               
                r.html.arender(sleep=1, keep_page=True, scrolldown=1)

               
                definicion = r.html.find('span.trans.dtrans', first=True)
             
                if definicion is not None:
                    result = definicion.text

       
        
        return  render_template('tarjeta/create_card.html', id = id, result = result, word = word)


#Webscraper create card
@tarjetaprint.route("/card/updateauto/<int:id>/", methods=['GET', 'POST'])
async def searchdefup(id):
        if request.method == 'POST':
            tarjeta = get_card(id)
            diccionario = request.form.get('diccionario')
            result = ""
            word = ""

            if diccionario == 'CDIE':
        
                word = request.form.get('searched')
                word = word.strip()
                word = re.sub(' +', '-', word)
            
                session = AsyncHTMLSession()
                
            
                url = "https://dictionary.cambridge.org/es/diccionario/ingles-espanol/" + word
            
                r = await session.get(url)
                
            
                r.html.arender(sleep=1, keep_page=True, scrolldown=1)

                pronunciacion = r.html.find('div.pr.entry-body__el span.ipa.dipa', first=True) 
                definicion = r.html.find('div.pr.entry-body__el  span.trans.dtrans.dtrans-se', first=True)
                ejemplo = r.html.find('div.examp.dexamp', first=True)
              
                
                if pronunciacion is not None:
                    result = pronunciacion.text + "\n" +definicion.text + "\n" + ejemplo.text

            if diccionario == 'CDEI':
        
                word = request.form.get('searched')
                word = word.strip()
                word = re.sub(' +', '-', word)
                
                session = AsyncHTMLSession()
                
            
                url = "https://dictionary.cambridge.org/es/diccionario/espanol-ingles/" + word
            
                r = await session.get(url)
                
                r.html.arender(sleep=1, keep_page=True, scrolldown=1)

               
                definicion = r.html.find('span.trans.dtrans', first=True)
             
                if definicion is not None:
                    result = definicion.text

       
        
        return  render_template('tarjeta/update_card.html', id = id, result = result, word = word, tarjeta = tarjeta)
        
    
    


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
            
    return render_template('tarjeta/create_card.html', id = id)

    
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
    result = ""

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
    return render_template('tarjeta/update_card.html', tarjeta = tarjeta, id = id, result = result)


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
