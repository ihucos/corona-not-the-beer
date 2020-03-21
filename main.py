import os

from flask import Flask
from whitenoise import WhiteNoise

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')



DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    import sqlite3
    conn = sqlite3.connect(':memory:')
else:
    import psycopg2
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')


@app.route('/')
def hello_world():
    return 'Hello World!'

