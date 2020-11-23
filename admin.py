from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask import g, url_for
from khayyam3 import JalaliDate
from werkzeug.utils import redirect


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if not g.user.is_authenticated:
            return redirect(url_for('main_pages.login', next=url_for('admin.index')))
        msg = 'Welcome'
        return self.render('admin/index.html', msg=msg)


class AdminAuthentication(object):
    def is_accessible(self):
        return g.user.is_authenticated and g.user.is_admin()


class CommonAdmin(AdminAuthentication, ModelView):
    pass


class InvoiceAdmin(CommonAdmin):
    from models import Entity
    inline_models = (Entity,)
    column_list = ('number', 'title', 'date', 'created_time', 'factor')
    column_editable_list = ('title',)
    column_formatters = dict(data=lambda v, c, m, p: JalaliDate(m.date))


class StaticFileAdmin(AdminAuthentication, FileAdmin):
    pass

