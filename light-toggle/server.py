#!/usr/bin/env python

from flask import (Flask, request, render_template)
from flask.ext import restful
from flask.ext.restful import reqparse
import pickle

SETTINGS_P = 'settings.p'

app = Flask(__name__)
api = restful.Api(app)


def get_settings():
    settings = {'state':'off'}
    try:
        settings = pickle.load(open(SETTINGS_P, 'rb'))
    except IOError:
        pass
    return settings


def set_state(state):
    settings = get_settings()
    settings['state'] = state
    pickle.dump( settings, open(SETTINGS_P, 'wb'))



# Restful Resource for setting the light state
@api.resource('/api/state')
class SetState(restful.Resource):
    def get(self):

        settings = get_settings()

        parser = reqparse.RequestParser()
        parser.add_argument('value', type=str, location='args',
                choices=['on','off'])
        args = parser.parse_args()

        value = args['value']

        if value:
            set_state(value)
            settings = get_settings()
            print "Setting state to {}".format(value)

        return {'state':settings['state']}


# View to present a form to change the light state
@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST':
        set_state(request.form['state'])

    settings = get_settings()
    state = settings['state']

    return render_template('index.html', state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
