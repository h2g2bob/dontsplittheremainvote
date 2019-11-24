import re
import sys
import psycopg2

from flask import Flask
from flask import redirect
from flask import request

app = Flask(__name__)

# WSGI (apache mod_wsgi) magically runs anything named 'application'
application = app

RE_NON_ALNUM = re.compile(r'[^A-Z0-9]+')

@app.route('/')
def hello():
    return 'Hello, World'

@app.route('/postcode/redir/', methods=('GET', 'POST'))
def postcode_redir():
    postcode = RE_NON_ALNUM.sub('', request.form['postcode'].upper())
    section = request.form.get('section', 'constituency')

    conn = psycopg2.connect('dbname=dontsplit')
    with conn:
        with conn.cursor() as cur:
            cur.execute('set statement_timeout=30;')
            cur.execute('''
                select
                    c.slug
                from postcode p
                join constituency c using (constituency_id)
                where p.postcode = %s;''',
                (postcode,))
            rows = list(cur)
            if len(rows) == 0:
                return redirect('/{}/'.format(section))
            elif len(rows) == 1:
                [slug] = rows[0]
                return redirect('/{}/{}.html'.format(section, slug))
            else:
                raise ValueError('Postcode {} caused multiple rows'.format(repr(postcode)))
