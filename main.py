import os

from flask import Flask, request
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


cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Entry (
  Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  session varchar(255),
  status varchar(255)  # example: "fever,healthy,sniff"
);
''')
cursor.close()


@app.route('/poll', methods=["POST"])
def poll():
    assert 0, request
