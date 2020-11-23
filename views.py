from coverage.debug import os
from flask import Blueprint, g, redirect, url_for, request, flash, render_template, send_file
from flask_login import login_user, logout_user, login_required
from weasyprint import HTML

from forms import LoginForm
from settings import files_dir, static_dir
from utils import extract_data

bp = Blueprint('main_pages', __name__)


@bp.route('/invoice_template/', methods=['GET', 'POST'])
@login_required
def invoice_template():
    from models import Invoice
    invoice_id = request.form.get('id', None)
    if invoice_id is None:
        return 'wrong parameters sent'
    invoice = Invoice.query.filter(invoice_id == invoice_id).first()
    factor_data = extract_data(invoice)
    return render_template('invoice_template.html', **factor_data)


@bp.route('/invoice_print/', methods=['GET', 'POST'])
@login_required
def invoice_factor():
    from models import Invoice
    invoice_id = request.form.get('id', None)
    if invoice_id is None:
        return 'wrong parameters sent'
    invoice = Invoice.query.filter(invoice_id == invoice_id).first()
    file_path = os.path.join(files_dir, '{}.pdf'.format(invoice.number))
    static_path = os.path.join(static_dir, 'css/style.css')
    factor_data = extract_data(invoice)
    HTML(string=render_template('invoice.html', **factor_data)).write_pdf(
        target=file_path, stylesheets=[static_path]
    )
    return send_file(file_path)


@bp.route('/')
def hello():
    return "Hello"


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated:
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user)
            flash('Successfully logged in as %s' % g.user.email, 'success')
            return redirect(url_for('admin.index'))
    else:
        form = LoginForm()
    return render_template('login.html', form=form)


@bp.route('/logout/')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(request.args.get('next') or url_for('main_pages.hello'))
