import requests
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


@app.route('/analyse_word/')
@app.route('/analyse_word/<string:word>')
def api(word=None):
    if not word:
        abort(422)

    info = analyse(word)
    return jsonify(asdict(info))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if app.debug:
        raise RuntimeError('While debugging use the vue frontend at port 8080')
    return render_template('index.html')


@app.errorhandler(422)
def internal_error(err):
    return jsonify({ 'error': 'That is not a valid input!' })

app.run(debug=True)
