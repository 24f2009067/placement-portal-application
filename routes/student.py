from flask import Blueprint, render_template, request, url_for, redirect, session
from sqlalchemy.exc import IntegrityError
from models import *
from datetime import datetime

student_bp = Blueprint("student", __name__)

@student_bp.route("/student/dashboard")
def student_dashboard():
    page = reLogin()
    if page: return page
    
    user_id = session.get("user_id")
    student = Student.query.filter(Student.user_id == user_id).first()
    id = student.student_id

    return render_template("/student/dashboard.html",
                           current_user_role="Student", 
                           student=student, 
                           regCompanies=getRegCompanies(), 
                           appliedDrives=getAppliedDrives(id))

# History
@student_bp.route("/student/history")
def history():
    page = reLogin()
    if page: return page

    user_id = session.get("user_id")
    student = Student.query.filter(Student.user_id == user_id).first()
    id = student.student_id

    return render_template("/student/history.html", current_user_role="Student", student=student)

# company routes
@student_bp.route("/student/company/<int:id>/view")
def viewCompany(id):
    page = reLogin()
    if page: return page

    company = Company.query.filter(Company.company_id == id).first()

    if company:
        return render_template("/student/company.html", current_user_role="Student", company=company, drives = getDrives(company.company_id))

    return redirect(url_for("student.student_dashboard"))

# drive routes
@student_bp.route("/student/drives/<int:id>/view")
def viewDrive(id):
    page = reLogin()
    if page: return page

    drive = Drive.query.filter(Drive.drive_id == id).first()

    if drive:
        return render_template("/student/drive.html", current_user_role="Student", drive=drive)

    return redirect(url_for("student.student_dashboard"))

@student_bp.route("/student/drives/<int:id>/view")


# Application routes
@student_bp.route("/student/drives/<int:id>/apply", methods=["POST", "GET"])
def apply(id):
    page = reLogin()
    if page: return page

    drive = Drive.query.filter(Drive.drive_id == id).first()

    if drive:
        uid = session.get("user_id")
        student_id = Student.query.filter(Student.user_id == uid).first().student_id
        try:
            application = Application(drive_id=id, student_id=student_id, applied_on=datetime.today())
            db.session.add(application)
            db.session.commit()

            return render_template("/student/drive.html", current_user_role="Student", drive=drive, message="Applied Successfully!")
        
        except(IntegrityError):
            db.session.rollback()
            return render_template("/student/drive.html", current_user_role="Student", drive=drive, message="An application already exists!")
    
    return redirect(url_for('student.student_dashboard'))

# Utilities
def reLogin():
    user_id = session.get("user_id")
    user = User.query.filter(User.user_id == user_id).first()
    if (not (user_id and user.role == "Student")):
        return redirect(url_for("auth.login"))
    
    if (not user.is_active):
        return render_template("login.html", current_user_role="User", message="Access Denied! Contact your administrator.")
    
def getRegCompanies():
    return Company.query.filter(Company.status == "Approved").order_by(Company.name).order_by(Company.company_id).all()

def getAppliedDrives(id):
    return Drive.query.join(Drive.applications).filter(Application.student_id == id, Drive.deadline >= datetime.today(), Drive.status == "Approved").order_by(Drive.drive_id).all()

def getDrives(id):
    return Drive.query.filter(Drive.company_id == id, Drive.deadline >= datetime.today(), Drive.status == "Approved").order_by(Drive.drive_id).all()