# Premise of the hackaton: A virus breakout happened and we need
# solutions, not good code. Panic, Panic, ahhh, ahh AHHHH!!1

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
  session varchar(255),
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  plz varchar(12),
  status varchar(255)  /* example: "fever,healthy,sniff"*/
);
''')
cursor.close()


@app.route('/poll', methods=["POST"])
def poll():
    status_set = set([])

    for key, value in request.form.items():

        if key == 'throaty' and value:
            status_set.add('throaty')

        elif key == 'sniff' and value:
            status_set.add('sniff')

        elif key == 'nausea' and value:
            status_set.add('nausea')

        elif key == 'fever' and value:
            status_set.add('fever')

        elif key == 'mood':
            if value == 'happy':
                status_set.add('mood_happy')
            elif value == 'unhappy':
                status_set.add('mood_unhappy')
            elif value == 'neutral':
                status_set.add('mood_neutral')
            elif value == 'problem':
                status_set.add('mood_problem')

    status_set_repr = ','.join(sorted(status_set))

    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO table_name (session, plz, status)
    VALUES (?, ?, ?);''',
    [
        request.form.get("session"),
        request.form.get("plz"),
        status_set_repr,

    ])
    cursor.close()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
