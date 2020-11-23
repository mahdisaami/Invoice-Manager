from flask_admin import Admin

from admin import InvoiceAdmin, StaticFileAdmin, ModelView, CommonAdmin
from app import app, db
from models import Invoice, User, Entity

app.config['FLASK_ADMIN_SWATCH'] = 'slate'
admin = Admin(
    app, name='InvoiceManager', template_mode='bootstrap3',
)
admin.add_view(InvoiceAdmin(Invoice, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(CommonAdmin(Entity, db.session))
admin.add_view(StaticFileAdmin(app.config['STATIC_DIR'], '/static/', name='Static Files'))

if __name__ == '__main__':
    app.run(debug=True)
