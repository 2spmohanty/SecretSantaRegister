import os



class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Ensure this path is correct
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'secret_santa.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
