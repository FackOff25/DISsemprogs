import os

from flask import Blueprint, render_template, request, redirect, url_for, current_app

from access import login_required, group_required
from db_work import call_proc, select, select_dict
from sql_provider import SQLProvider

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_report.route('/', methods=['GET', 'POST'])
@login_required
def start_report():
    if request.method == 'GET':
        return render_template('menu_report.html', report_list=current_app.config['reports_list_config'])
    else:
        rep_id = request.form.get('rep_id')
        if request.form.get('create_rep'):
            url_rep = current_app.config['reports_config'][rep_id]['create_rep']
        else:
            url_rep = current_app.config['reports_config'][rep_id]['view_rep']
        return redirect(url_for(url_rep))


@blueprint_report.route('/create_rep1')
@group_required
def create_rep1():
    month = 10
    year = 2022
    rep_num = 0
    proc_name = 'create_report'
    call_proc(current_app.config['db_config'], proc_name, month, year)
    return render_template('created.html', report=current_app.config['reports_list_config'][rep_num]['rep_name'])


@blueprint_report.route('/create_rep2')
@group_required
def create_rep2():
    month = 11
    year = 2022
    rep_num = 1
    proc_name = 'create_report'
    call_proc(current_app.config['db_config'], proc_name, month, year)
    return render_template('created.html', report=current_app.config['reports_list_config'][rep_num]['rep_name'])


@blueprint_report.route('/view_rep1')
@group_required
def view_rep1():
    month = 10
    year = 2022
    rep_num = 0
    _sql = provider.get('get_rep.sql', month=month, year=year)
    product_result, schema = select(current_app.config['db_config'], _sql)
    print("product_result=", product_result)
    if len(product_result) == 0:
        return render_template('not_created.html', report=current_app.config['reports_list_config'][rep_num]['rep_name'])
    return render_template('db_result.html', schema=schema, result=product_result)


@blueprint_report.route('/view_rep2')
@group_required
def view_rep2():
    month = 11
    year = 2022
    rep_num = 1
    _sql = provider.get('get_rep.sql', month=month, year=year)
    product_result, schema = select(current_app.config['db_config'], _sql)
    if len(product_result) == 0:
        render_template('created.html', report=current_app.config['reports_list_config'][rep_num]['rep_name'])
    return render_template('db_result.html', schema=schema, result=product_result)
