from flask import Blueprint, render_template, request, url_for, redirect, session
from sqlalchemy.exc import IntegrityError
from models import *
from datetime import datetime

company_bp = Blueprint("company", __name__)

@company_bp.route("/company/dashboard")
def company_dashboard():
    page = reLogin()
    if page: return page

    user_id = session.get("user_id")
    id = Company.query.filter(Company.user_id == user_id).first().company_id
    
    return render_template("/company/dashboard.html", current_user_role="Company", ongoingDrives=getOngoingDrives(id), closedDrives=getClosedDrives(id))

# Drives
@company_bp.route("/company/drives/<int:id>/view")
def viewDrive(id):
    page = reLogin()
    if page: return page

    drive = Drive.query.filter(Drive.drive_id == id).first()
    
    if drive:
        if drive.company.user.user_id != session.get("user_id"):
            return redirect(url_for("auth.login"))
        return render_template("/company/drive.html", current_user_role="Company", drive=drive)

    return redirect(url_for("company.company_dashboard"))

@company_bp.route("/company/drives/<int:id>/complete", methods=["POST"])
def completeDrive(id):
    page = reLogin()
    if page: return page
    
    drive = Drive.query.filter(Drive.drive_id == id).first()
    if drive:
        if drive.company.user.user_id != session.get("user_id"):
            return redirect(url_for("auth.login"))
        
        drive.status = "Closed"

        db.session.commit()
    
    return redirect(url_for("company.company_dashboard"))

@company_bp.route("/company/drives/create", methods=["GET", "POST"])
def createDrive():
    if request.method == "GET":
        page = reLogin()
        if page: return page
        return render_template("/company/createDrive.html", current_user_role="Company", date=datetime.strftime(datetime.now(), "%Y-%m-%d"))
    
    if request.method == "POST":
        form = request.form
        company_id = Company.query.join(Company.user).filter(User.user_id == session.get("user_id")).first().company_id
        drive = Drive(company_id=company_id,
                      job_title=form["job_title"],
                      description=form["job_desc"],
                      eligibility=form["eligibility"],
                      deadline=datetime.strptime(form["deadline"], "%Y-%m-%d"),
                      )
        
        db.session.add(drive)
        db.session.commit()

        return redirect(url_for("company.company_dashboard"))

@company_bp.route("/company/drives/<int:id>/edit", methods=["GET", "POST"])
def updateDrive(id):
    if request.method == "GET":
        page = reLogin()
        if page: return page

        drive = Drive.query.filter(Drive.drive_id == id).first()
        if drive:
            if drive.company.user.user_id != session.get("user_id"):
                return redirect(url_for("auth.login"))
            
            return render_template("/company/updateDrive.html", current_user_role="Company", date=datetime.strftime(datetime.now(), "%Y-%m-%d"), drive=drive)
    
    if request.method == "POST":
        page = reLogin()
        if page: return page

        drive = Drive.query.filter(Drive.drive_id == id).first()
        if drive:
            if drive.company.user.user_id != session.get("user_id"):
                return redirect(url_for("auth.login"))

            form = request.form
            company_id = Company.query.join(Company.user).filter(User.user_id == session.get("user_id")).first().company_id
            drive = Drive.query.filter(Drive.drive_id == id).first()
            drive.company_id = company_id
            drive.job_title=form["job_title"]
            drive.description=form["job_desc"]
            drive.eligibility=form["eligibility"]
            drive.deadline=datetime.strptime(form["deadline"], "%Y-%m-%d")
            drive.status = "Approved"
            
            db.session.commit()

    return redirect(url_for("company.company_dashboard"))

# Applications
@company_bp.route("/company/applications/<int:id>/view")
def viewApplication(id):
    page = reLogin()
    if page: return page

    application = Application.query.filter(Application.application_id == id).first()


    
    if application:
        if application.drive.company.user.user_id != session.get("user_id"):
            return redirect(url_for("auth.login"))
        
        return render_template("/company/application.html", current_user_role="Company", application=application)
    
    return redirect(url_for("company.viewDrive", id=application.drive_id))

@company_bp.route("/company/application/<int:id>/status", methods=["POST"])
def setStatus(id):
    page = reLogin()
    if page: return page

    application = Application.query.filter(Application.application_id == id).first()

    if application:
        status = request.form["status"]
        application.status = status
        application.history = application.history + "," + status
        db.session.commit()
    
    return redirect(url_for("company.viewDrive", id=application.drive_id))


# utility functions

def reLogin():
    user_id = session.get("user_id")
    user = User.query.filter(User.user_id == user_id).first()
    if (not (user_id and user.role == "Company")):
        return redirect(url_for("auth.login"))
    
    if (not user.is_active):
        return render_template("login.html", current_user_role="User", message="Access Denied! Contact your administrator.")
    
    return False

def getOngoingDrives(id):
    return Drive.query.join(Drive.company).filter(Drive.status == "Approved", Drive.company_id == id).order_by(Drive.drive_id).all()

def getClosedDrives(id):
    return Drive.query.join(Drive.company).filter(Drive.status == "Closed", Drive.company_id == id).order_by(Drive.drive_id).all()