from flask import Flask, url_for, render_template, request, json
from blueprint_query.route import blueprint_query

app = Flask(__name__)

app.register_blueprint(blueprint_query, url_prefix='/requests')

with open('data_files/dbconfig.json', 'r') as f:
    db_config = json.load(f)
app.config['dbconfig'] = db_config


@app.route('/', methods=['GET', 'POST'])
def query():
    return render_template('start_request.html')


@app.route('/exit')
def goodbye():
    return "До свидания, заходите к нам ещё!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
