from flask import Flask, render_template, json, session

from access import login_required
from auth.route import blueprint_auth
from blueprint_report.route import blueprint_report

# from access import login_required

app = Flask(__name__)
app.secret_key = 'Superkey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/reports')

app.config['access_config'] = json.load(open('data_files/access.json'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def main_menu():
    return render_template('main_menu.html')


@app.route('/exit')
def exit_func():
    session.clear()
    return "До свидания, заходите к нам ещё!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
