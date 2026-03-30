from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(30), nullable=False) # Admin / Student / Company
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    student = db.relationship("Student", backref="user", uselist=False)
    company = db.relationship("Company", backref="user", uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique=True, nullable=False)

    name = db.Column(db.String(30), nullable=False)
    skills = db.Column(db.String(200))
    dept = db.Column(db.String(30), nullable=False)
    course = db.Column(db.String(30), nullable=False)
    resume_path = db.Column(db.String(50))

    applications = db.relationship("Application", backref="student")

class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique=True, nullable=False)

    name = db.Column(db.String(30), nullable=False)
    website = db.Column(db.String(150))
    status = db.Column(db.String(30), nullable=False, default="Pending") # Pending / Approved / Rejected

    drives = db.relationship("Drive", backref="company")

class Drive(db.Model):
    drive_id = db.Column(db.Integer, primary_key=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    job_title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(200))
    eligibility = db.Column(db.String(200))
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Approved") # Approved / Rejected / Closed

    applications = db.relationship('Application', backref="drive")

class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True, nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.drive_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    applied_on = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Applied") # Applied / Rejected / Selected
    history = db.Column(db.String(250), nullable=False, default="Applied")

    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="unique_student_drive"),
    )