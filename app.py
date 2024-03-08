from flask import *
import db
import requests


app = Flask(__name__)
app.secret_key = '61BQ6[|j>2\_w~e'
app.teardown_appcontext(db.close_db)


def get_weather(state: str):
    r = requests.get(f'https://api.weather.gov/alerts/active?area={state}')
    return r.json()


@app.get('/')
def hello():
    states = db.get_states()
    return render_template('index.html', states=states)


@app.get('/api/birds')
def get_bird():
    state = request.args.get('state')
    if state is None:
        return error("'state' parameter is required")

    state = state.upper()
    if len(state) == 2 and state.isalpha():
        bird = db.get_bird(state)
        if bird is None:
            return error(f"'{state}' bird does not exist", 404)
    else:
        return error(f"State '{state}' is invalid")

    weather = get_weather(state)
    return {'bird': bird, 'weather': weather}


def error(message: str, code=400):
    return {'error': message}, code


if __name__ == '__main__':
    app.run(host='0.0.0.0')
