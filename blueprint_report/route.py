from flask import Blueprint, render_template, request, redirect, url_for, current_app

from access import login_required, group_required
from db_work import call_proc

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')

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
    rep_month = 9
    rep_year = 2022
    res = call_proc(current_app.config['db_config'], 'product_report', rep_month, rep_year)
    print("res=", res)
    return render_template('report_created.html')


@blueprint_report.route('/page2')
@group_required
def start_page2():
    return render_template('page2.html')
