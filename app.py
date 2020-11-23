from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_migrate import Migrate, MigrateCommand
from flask_redis import FlaskRedis
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from configuration import Config


from views import bp

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.register_blueprint(bp)

redis_client = FlaskRedis(app)


@login_manager.user_loader
def _user_loader(user_id):
    from models import User
    return User.query.get(int(user_id))


@app.before_request
def _before_request():
    g.user = current_user
