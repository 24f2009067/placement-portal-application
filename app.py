from flask import Flask, render_template
from extensions import db
from models import User, Student

from routes.auth import auth_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement_portal.db"
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)

if (__name__ == "__main__"):
    app.run(debug=True)