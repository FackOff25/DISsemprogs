from typing import Callable, List

from flask import Flask, url_for, render_template, request, json, session, redirect
from auth.route import blueprint_auth
from basket.route import blueprint_order
from access import login_required, group_required
from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report

app = Flask(__name__)
app.secret_key = 'Superkey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_order, url_prefix='/order')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_query, url_prefix='/query')

app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))
app.config['reports_config'] = json.load(open('data_files/reports.json'))
app.config['reports_list_config'] = json.load(open('data_files/reports_list.json'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def menu_choice():
    if 'user_id' in session:
        if session.get('user_group', None):
            return render_template('internal_user_menu.html')
        else:
            return render_template('external_user_menu.html')
    else:
        return redirect(url_for('blueprint_auth.start_auth'))


@app.route('/exit')
def exit_func():
    session.clear()
    return "До свидания, заходите к нам ещё!"

def add_blueprint_access_handler(app: Flask, blueprint_names: List[str], handler: Callable) -> Flask:
    for view_func_name, view_func in app.view_functions.items():
        print("view_func_name=", view_func_name)
        print("view_func=", view_func)
        view_func_parts = view_func_name.split('.')
        if len(view_func_parts) > 1:
            view_blueprint = view_func_parts[0]
            if view_blueprint in blueprint_names:
                view_func = handler(view_func)
                app.view_functions[view_func_name] = view_func
    return app


if __name__ == '__main__':
    app = add_blueprint_access_handler(app, ['bp_report'], group_required)
    app.run(host='127.0.0.1', port=8000)
