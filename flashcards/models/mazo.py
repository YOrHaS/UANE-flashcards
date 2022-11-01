from flashcards import db



class Mazo(db.Model):
    __tablename__ = 'mazos'
    id = db.Column(db.Integer, primary_key=True)
    idInterno = db.Column(db.String(32), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nombre = db.Column(db.Text)
    visibilidad = db.Column(db.Boolean, nullable=False)
   
   
    def __init__(self, idUsuario, idInterno, nombre, visibilidad) -> None:
        self.idInterno = idInterno
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.visibilidad = visibilidad
        

    def __repr__(self) -> str:
        return f'Mazo: {self.nombre}' 
    
    def getIdInterno(self):
        return self.idInterno