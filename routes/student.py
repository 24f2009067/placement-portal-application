from flask import Blueprint, render_template, request, url_for, redirect, session
from sqlalchemy import or_
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

    q = request.args.get("q")

    return render_template("/student/dashboard.html",
                           current_user_role="Student", 
                           student=student, 
                           regCompanies=getRegCompanies(q), 
                           appliedDrives=getAppliedDrives(id, q))

# History
@student_bp.route("/student/history")
def history():
    page = reLogin()
    if page: return page

    user_id = session.get("user_id")
    student = Student.query.filter(Student.user_id == user_id).first()
    id = student.student_id

    return render_template("/student/history.html", current_user_role="Student", student=student, history=getHistory(id))

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
            now = datetime.now()
            application.history = "Applied" + f" ({now:%Y-%m-%d})"
            db.session.add(application)
            db.session.commit()

            return render_template("/student/drive.html", current_user_role="Student", drive=drive, message="Applied Successfully!")
        
        except(IntegrityError):
            db.session.rollback()
            return render_template("/student/drive.html", current_user_role="Student", drive=drive, message="An application already exists!")
    
    return redirect(url_for('student.student_dashboard'))

# Profile
@student_bp.route("/student/profile/edit", methods=["GET", "POST"])
def editProfile():
    page = reLogin()
    if page: return page

    uid = session.get("user_id")
    student = Student.query.filter(Student.user_id == uid).first()

    if request.method == "POST":
        form = request.form
        student.name = form["name"].strip().title()
        if form["password"] != "":
            student.user.set_password(form["password"])
        student.skills = form["skills"].strip().lower()
        student.dept = form["dept"].strip().upper()
        student.course = form["course"].strip().upper()
        student.resume_path = form["resume_path"].strip()

        db.session.commit()
        return redirect(url_for("student.student_dashboard"))

    
    if request.method == "GET":
        return render_template("/student/editProfile.html", current_user_role="Student", student=student)
    
# Notifications
@student_bp.route("/student/notifications")
def viewNotifications():
    page = reLogin()
    if page: return page

    uid = session.get("user_id")
    student_id = Student.query.filter(Student.user_id == uid).first().student_id
    notifications = Notification.query.filter(Notification.student_id == student_id, Notification.is_seen == False).order_by(Notification.created_on.desc()).all()

    return render_template("/student/notifications.html", current_user_role="Student", notifications=notifications)

@student_bp.route("/student/notification/<int:id>/read", methods=["POST"])
def markAsRead(id):
    page = reLogin()
    if page: return page

    notification = Notification.query.filter(Notification.notification_id == id).first()
    if notification: notification.is_seen = True

    db.session.commit()

    return redirect(url_for("student.student_dashboard"))


# Utilities
def reLogin():
    user_id = session.get("user_id")
    user = User.query.filter(User.user_id == user_id).first()
    if (not (user_id and user.role == "Student")):
        return redirect(url_for("auth.login"))
    
    if (not user.is_active):
        return render_template("login.html", current_user_role="User", message="Access Denied! Contact your administrator.")
    
def getRegCompanies(q):
    query = Company.query

    if q:
        if q.isdigit():
            query = query.filter(Company.company_id == int(q))
        else:
            query = query.filter(Company.name.ilike(f"%{q}%"))

    output = query.filter(Company.status == "Approved").order_by(Company.name).order_by(Company.company_id).all()

    return output

def getAppliedDrives(id, q):
    query = Application.query.join(Application.drive).join(Drive.company)
    if q:
        if q.isdigit():
            query = query.filter(Drive.drive_id == int(q))
        else:
            query = query.filter(or_(Company.name.ilike(f"%{q}%"), Drive.job_title.ilike(f"%{q}%"), Application.status.ilike(f"%{q}%")))

    query = query.distinct()
    output = query.filter(Application.student_id == id).order_by(Drive.drive_id).all()

    return output

def getDrives(id):
    return Drive.query.filter(Drive.company_id == id, Drive.deadline >= datetime.today(), Drive.status == "Approved").order_by(Drive.drive_id).all()

def getHistory(id):
    return Application.query.filter(Application.student_id == id).all()