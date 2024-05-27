from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Config(object):
    SECRET_KEY = '50c8760b1003677c617b374921f95c539c5ef73ae38bfa791c67b855325f866c'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@postgres/vkr'
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@localhost/vkr'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
