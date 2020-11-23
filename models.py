from datetime import datetime

from flask import url_for

from app import db, bcrypt, login_manager
from utils import factor_button
from markupsafe import Markup


@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(64), nullable=True)
    is_active = db.Column(db.Boolean(64), default=True)
    created_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def is_authenticated(self):
        return True

    def is_admin(self):
        return True

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @classmethod
    def create(cls, email, password, **kwargs):
        return User(email=email, password_hash=password, **kwargs)

    @staticmethod
    def make_password(plain_password):
        return bcrypt.generate_password_hash(plain_password)

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    @classmethod
    def create(cls, email, password, **kwargs):
        return User(email=email, password_hash=User.make_password(password), **kwargs)

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return False


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(12), nullable=True)
    title = db.Column(db.String(80), nullable=True)
    date = db.Column(db.DateTime(12), nullable=True)
    description = db.Column(db.Text, nullable=True)
    customer = db.Column(db.String(48), nullable=True)

    entities = db.relationship('Entity', backref='invoice', lazy=True)
    created_data = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __str__(self):
        return "{} - {}".format(self.title, self.number)

    @property
    def total_price(self):
        return sum([en.total_price for en in self.entities])

    @property
    def total_discount(self):
        return sum([en.discount or 0 for en in self.entities])

    @property
    def payable_price(self):
        return self.total_price - self.total_discount

    @property
    def factor(self):
        print_btn = factor_button.format(
            action=url_for('main_pages.invoice_factor'), value=self.id,
            class_type='default', text='Print')
        preview_btn = factor_button.format(
            action=url_for('main_pages.invoice_template'), value=self.id,
            class_type='primary', text='Preview')
        return Markup(print_btn + preview_btn)


class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Integer, nullable=True)
    fee = db.Column(db.Integer, nullable=True)
    discount = db.Column(db.Integer, nullable=True)

    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)

    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __str__(self):
        return self.description

    @property
    def total_price(self):
        return self.fee * self.qty
