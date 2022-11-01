from flashcards import db


class Tarjeta(db.Model):
    __tablename__ = 'tarjetas'
    id = db.Column(db.Integer, primary_key=True)    
    adelante = db.Column(db.Text)
    atras = db.Column(db.Text)
    idMazo = db.Column(db.Integer, db.ForeignKey('mazos.id'), nullable=False)
    dificultad = db.Column(db.Integer, nullable=False)    

    #Constructor
    def __init__(self, idMazo, adelante, atras) -> None:
        self.idMazo = idMazo
        self.adelante = adelante
        self.atras = atras
        self.dificultad = 1
        

    def __repr__(self) -> str:
        return f'Tarjeta: {self.adelante}' 