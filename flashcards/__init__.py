from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Cargar configuración
app.config.from_object('config.DevelopmentConfig')
#Se crea db variable
db = SQLAlchemy(app)


#importar vistas
from flashcards.views.auth  import auth
app.register_blueprint(auth)

from flashcards.views.mazoview import mazoprint
app.register_blueprint(mazoprint)

from flashcards.views.tarjetaview import tarjetaprint
app.register_blueprint(tarjetaprint)



with app.app_context():
    db.create_all()

    
