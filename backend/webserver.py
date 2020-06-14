import requests
import validation
from flask import Flask, render_template, jsonify, abort
from analyse import analyse
from dataclasses import asdict

class VueFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

app = VueFlask(__name__, static_folder='./dist/static', template_folder='./dist')

def generate_error(msg):
    return jsonify({ 'error': msg })

@app.route('/analyse_word/')
@app.route('/analyse_word/<string:word>')
def api(word=None):
    if not validation.is_usable(word):
        return generate_error('Invalid input given (Either too short or too long)'), 422
        
    analysis_result = analyse(word)

    info = asdict(analysis_result)

    return jsonify(info)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if app.debug:
        raise RuntimeError('While debugging use the vue frontend at port 8080')
    return render_template('index.html')


app.run(debug=True)
