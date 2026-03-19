from flask import Blueprint, render_template, request, url_for, redirect, session
from sqlalchemy.exc import IntegrityError
from models import *

student_bp = Blueprint("student", __name__)

@student_bp.route("/student/dashboard")
def student_dashboard():
    user_id = session.get("user_id")
    user = User.query.filter(User.user_id == user_id).first()
    if (not (user_id and user.role == "Student")):
        return redirect(url_for("auth.login"))
    
    if (not user.is_active):
        return render_template("login.html", current_user_role="User", message="Access Denied! Contact your administrator.")
    
    return render_template("/student/dashboard.html", current_user_role="Student")