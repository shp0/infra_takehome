import sqlite3
from flask import g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect('birds.db')
        g.db.row_factory = sqlite3.Row
    return g.db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_bird(state_abbrev: str):
    result = query_db("select * from birds where abbreviation = ?;", [state_abbrev], True)
    return dict(result)


def get_states():
    rows = query_db("select state, abbreviation from birds order by state;")
    return [dict(ix) for ix in rows]


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
