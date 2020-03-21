# Premise of the hackaton: A virus breakout happened and we need
# solutions, not good code. Panic, Panic, ahhh, ahh AHHHH!!1

import os

from flask import Flask, request, Response
from whitenoise import WhiteNoise

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')


DATABASE_URL = os.environ.get('DATABASE_URL')

# I use that for local development
if not DATABASE_URL:
    import sqlite3
    conn = sqlite3.connect(
    ':memory:',
    check_same_thread=False)


else:
    import psycopg2
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')


cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS entry (
  userid varchar(255),
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  plz varchar(12),
  status varchar(255)  /* example: "fever,healthy,sniff"*/
);
''')
cursor.close()


@app.route('/', methods=["POST", "GET"])
def poll():

    if request.method == "GET":
        return app.send_static_file('form.html')

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
    INSERT INTO entry (userid, plz, status)
    VALUES (?, ?, ?);''',
    [
        request.form.get("userid"),
        request.form.get("plz"),
        status_set_repr,

    ])
    cursor.close()

    return app.send_static_file('success.html')


@app.route('/data.csv', methods=["GET"])
def download():
    cursor = conn.cursor()
    cursor.execute('SELECT userid, timestamp, plz, status FROM entry')
    def generate():
        yield "userid;timestamp;plz;status\n"
        while True:
            many = cursor.fetchmany()
            if not many:
                break
            for entry in many:
                userid, timestamp, plz, status = (i or '' for i in entry)
                yield f"{userid};{timestamp};{plz};{status}\n"
        cursor.close()
    return Response(generate(), mimetype='text/csv')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
