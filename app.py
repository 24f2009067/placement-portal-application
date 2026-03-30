from flask import Flask
from extensions import db
from models import User, Student, Drive
from datetime import datetime

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.student import student_bp
from routes.company import company_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement_portal.db"
app.secret_key = b'8c47a8b456b70ef3036e3edc1466d53ac8994a127fb849935118c03ca4e81250'
db.init_app(app)

with app.app_context():
    db.create_all()
    if (User.query.filter(User.email == "admin@ppa.com").first() == None):
        admin = User(email="admin@ppa.com", role="Admin")
        admin.set_password("password")
        db.session.add(admin)
        db.session.commit()


app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(company_bp)


@app.before_request
def driveCleanup():
    now = datetime.now()

    expired = Drive.query.filter(Drive.deadline < now, Drive.status == "Approved").all()
    if not expired: return

    for drive in expired:
        drive.status = "Closed"

    db.session.commit()

if (__name__ == "__main__"):
    app.run(debug=True, host="0.0.0.0")