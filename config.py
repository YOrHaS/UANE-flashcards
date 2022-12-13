class Config:
    DEBUG = True
    TESTING = True

    #configuracion de base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/api_flashcards"
    #caa269e6-544a-41d8-8b27-ba3d95a638c1
    #SQLALCHEMY_DATABASE_URI = "postgresql://lffvohgbhqtidc:ba6ffb9ff8c954004cf21fbe0faa1ac1f27832206b5f015e8b8f1a1795c9e448@ec2-54-160-200-167.compute-1.amazonaws.com:5432/d1n7s1vclebbbt"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:KlNBJQjP89xLnr0HhUj5@containers-us-west-162.railway.app:7361/railway"

    
#clases que herada de Config
class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    SECRET_KEY = 'dev'
    DEBUG = True
    TESTING = True
