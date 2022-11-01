from flashcards import db
from flashcards import app
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuarioNombre = db.Column(db.String(50))
    usuarioCorreo = db.Column(db.String(50))
    usuarioPassword = db.Column(db.Text)

    #Constructor
    def __init__(self, usuarioNombre, usuarioCorreo, usuarioPassword) -> None:
        self.usuarioNombre = usuarioNombre
        self.usuarioCorreo = usuarioCorreo
        self.usuarioPassword = usuarioPassword
       