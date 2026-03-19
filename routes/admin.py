from flask import Blueprint, render_template, request, url_for, redirect, session
from sqlalchemy.exc import IntegrityError
from models import *

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    user_id = session.get("user_id")
    user = User.query.filter(User.user_id == user_id).first()
    if (not (user_id and user.role == "Admin")):
        return redirect(url_for("auth.login"))
    
    return render_template("/admin/dashboard.html", current_user_role="Admin", stats=getStats())

# utility functions

def getStats():
    stats = {
        "student_total": 0,
        "student_active": 0,
        "student_blocklisted": 0,

        "company_total": 0,
        "company_active": 0,
        "company_pending": 0,
        "company_blacklisted": 0
    }

    stats["student_total"] = Student.query.count()
    stats["student_active"] = User.query.filter(User.role == "Student", User.is_active == True).count()
    stats["student_blacklisted"] = stats["student_total"] - stats["student_active"]

    stats["company_total"] = Company.query.count()
    stats["company_active"] = Company.query.filter(Company.status == "Approved").count()
    stats["company_pending"] = Company.query.filter(Company.status == "Pending").count()
    stats["company_blacklisted"] = Company.query.filter(Company.status == "Rejected").count()

    return stats


