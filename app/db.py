from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect("dbname=packlist user=postgres host=localhost")
cur = conn.cursor(cursor_factory=RealDictCursor)

# db = SQLAlchemy()

# def connect_db(app):
#     db.app = app
#     app.app_context().push()
#     db.init_app(app)