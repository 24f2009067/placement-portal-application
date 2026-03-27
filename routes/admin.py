from flask import Blueprint, render_template, request, url_for, redirect, session
from sqlalchemy.exc import IntegrityError
from models import *

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    page = reLogin()
    if page: return page
    
    return render_template("/admin/dashboard.html", 
                           current_user_role="Admin", 
                           stats=getStats(), 
                           regCompanies=getRegCompanies(), 
                           pendCompanies=getPendCompanies(),
                           ongoingDrives=getOngingDrives(),
                           regStudents = getRegStudents(),
                           applications = getApplications()
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

        "drive_total": 0,
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

def getRegCompanies():
    return Company.query.filter(Company.status == "Approved").order_by(Company.name).all()

def getPendCompanies():
    return Company.query.filter(Company.status == "Pending").order_by(Company.name).all()

def getOngingDrives():
    return Drive.query.join(Drive.company).filter(Drive.status == "Approved").order_by(Drive.company_id).all()

def getRegStudents():
    return Student.query.join(Student.user).filter(User.is_active == True).order_by(Student.student_id).all()

def getApplications():
    return Application.query.join(Application.drive).join(Drive.company).filter(Drive.status == "Approved").order_by(Drive.drive_id).all()
