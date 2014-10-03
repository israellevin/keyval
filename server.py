#!/usr/bin/python3

import db
from flask import Flask, abort
app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'keyval',
    DEBUG = True
)

@app.route('/<key>')
@app.route('/<key>/<value>')
def getvalue(key, value=None):
    existing = db.Value.getbykey(key)
    if value is None:
        if existing: return existing.value
        abort(404)
    else:
        if not existing: return db.Value(key, value).value
        existing.value = value
        db.session.commit()
        return value

if __name__ == '__main__':
    from sys import argv
    try: app.run(host='0.0.0.0', port=int(argv[1]))
    except: app.run(host='0.0.0.0')
