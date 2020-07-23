import pymysql
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()
db = SQLAlchemy()
migrate = Migrate()


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)