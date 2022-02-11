import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'WebStockDB.db')) #DB 주소
SQLALCHEMY_TRACK_MODIFICATIONS = False #모르는데 False