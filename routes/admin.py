from flask import Blueprint, render_template, request, url_for, redirect, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from datetime import datetime
from models import *

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    page = reLogin()
    if page: return page

    q = request.args.get("q")
    
    return render_template("/admin/dashboard.html", 
                           current_user_role="Admin", 
                           stats=getStats(), 
                           regCompanies=getRegCompanies(q), 
                           pendCompanies=getPendCompanies(q),
                           ongoingDrives=getOngingDrives(q),
                           regStudents = getRegStudents(q),
                           applications = getApplications(q)
                           )

# Company routes
@admin_bp.route("/admin/companies/<int:id>/approve", methods=["POST"])
def approveCompany(id):
    page = reLogin()
    if page: return page
    
    company = Company.query.filter(Company.company_id == id).first()
    if company:
        company.status = "Approved"
        company.user.is_active = True

        db.session.commit()
    
    return redirect(url_for("admin.admin_dashboard"))

@admin_bp.route("/admin/companies/<int:id>/blacklist", methods=["POST"])
def blacklistCompany(id):
    page = reLogin()
    if page: return page
    
    company = Company.query.filter(Company.company_id == id).first()
    if company:
        company.status = "Rejected"
        company.user.is_active = False

        for drive in company.drives:
            drive.status = "Rejected"
            for application in drive.applications:
                application.status = "Company Blacklisted"
                now = datetime.now()
                application.history = application.history + "," + "Company Blacklisted" + f" ({now:%Y-%m-%d})"

                student_id = application.student.student_id
                title = f"{application.drive.company.name} • {application.drive.job_title}"
                message = "Application status changed to Company Blacklisted."
                notification = Notification(student_id=student_id, created_on=now, title=title, message=message)
                db.session.add(notification)

        db.session.commit()
    
    return redirect(url_for("admin.admin_dashboard"))

# Student routes
@admin_bp.route("/admin/students/<int:id>/blacklist", methods=["POST"])
def blacklistStudent(id):
    page = reLogin()
    if page: return page
    
    student = Student.query.filter(Student.student_id == id).first()
    if student:
        student.user.is_active = False

        db.session.commit()
    
    return redirect(url_for("admin.admin_dashboard"))

# Drive routes
@admin_bp.route("/admin/drives/<int:id>/complete", methods=["POST"])
def completeDrive(id):
    page = reLogin()
    if page: return page
    
    drive = Drive.query.filter(Drive.drive_id == id).first()
    if drive:
        drive.status = "Closed"

        db.session.commit()
    
    return redirect(url_for("admin.admin_dashboard"))

# Applications
@admin_bp.route("/admin/applications/<int:id>/view")
def viewApplication(id):
    page = reLogin()
    if page: return page

    application = Application.query.filter(Application.application_id == id).first()
    
    if application:
        return render_template("/admin/application.html", current_user_role="Admin", application=application)
    
    return redirect(url_for("admin.admin_dashboard"))

# Drive
@admin_bp.route("/admin/drives/<int:id>/view")
def viewDrive(id):
    page = reLogin()
    if page: return page

    drive = Drive.query.filter(Drive.drive_id == id).first()
    
    if drive:
        return render_template("/admin/drive.html", current_user_role="Admin", drive=drive)

    return redirect(url_for("admin.admin_dashboard"))

# utility functions
def reLogin():
    user_id = session.get("user_id")
    user = User.query.filter(User.user_id == user_id).first()
    if (not (user_id and user.role == "Admin")):
        return redirect(url_for("auth.login"))
    
    return False

def getStats():
    stats = {
        "student_total": 0,
        "student_active": 0,
        "student_blocklisted": 0,

        "company_total": 0,
        "company_active": 0,
        "company_pending": 0,
        "company_blacklisted": 0,

        "drive_total": 0,"{{ url_for(current_user_role.lower() + '.' + current_user_role.lower() + '_dashboard' if current_user_role != 'User' else 'auth.login') }}"
        "drive_active": 0,
        "drive_closed": 0,
        "drive_applications": 0     
    }

    stats["student_total"] = Student.query.count()
    stats["student_active"] = User.query.filter(User.role == "Student", User.is_active == True).count()
    stats["student_blacklisted"] = stats["student_total"] - stats["student_active"]

    stats["company_total"] = Company.query.count()
    stats["company_active"] = Company.query.filter(Company.status == "Approved").count()
    stats["company_pending"] = Company.query.filter(Company.status == "Pending").count()
    stats["company_blacklisted"] = Company.query.filter(Company.status == "Rejected").count()

    stats["drive_total"] = Drive.query.filter(Drive.status != "Rejected").count()
    stats["drive_active"] = Drive.query.filter(Drive.status == "Approved" ).count()
    stats["drive_closed"] = Drive.query.filter(Drive.status == "Closed" ).count()
    stats["drive_applications"] = Application.query.join(Application.drive).join(Drive.company).filter(Drive.status == "Approved").order_by(Drive.drive_id).count()
    return stats

def getRegCompanies(q):
    query = Company.query
    if q:
        if q.isdigit():
            query = query.filter(Company.company_id == int(q))
        else:
            query = query.filter(Company.name.ilike(f"%{q}%"))

    output = query.filter(Company.status == "Approved").order_by(Company.name).all()
    
    return output

def getPendCompanies(q):
    query = Company.query
    if q:
        if q.isdigit():
            query = query.filter(Company.company_id == int(q))
        else:
            query = query.filter(Company.name.ilike(f"%{q}%"))

    output = query.filter(Company.status == "Pending").order_by(Company.name).all()

    return output

def getOngingDrives(q):
    query = Drive.query.join(Drive.company)
    if q:
        if q.isdigit():
            query = query.filter(Drive.drive_id == int(q))
        else:
            query = query.filter(Company.name.ilike(f"%{q}%"))

    output = query.filter(Drive.status == "Approved").order_by(Drive.company_id).all()

    return output

def getRegStudents(q):
    query = Student.query.join(Student.user)
    if q:
        if q.isdigit():
            query = query.filter(Student.student_id == int(q))
        else:
            query = query.filter(Student.name.ilike(f"%{q}%"))

    output = query.filter(User.is_active == True).order_by(Student.student_id).all()

    return output

def getApplications(q):
    query = Application.query.join(Application.drive).join(Drive.company).join(Application.student)
    if q:
        if q.isdigit():
            query = query.filter(Application.application_id == int(q))
        else:
            query = query.filter(or_(Student.name.ilike(f"%{q}%"), Company.name.ilike(f"%{q}%")))

    output = query.filter(Drive.status == "Approved").order_by(Drive.drive_id).all()

    return output
