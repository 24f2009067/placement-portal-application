from flask import Blueprint, render_template, request, url_for, redirect, session
from sqlalchemy.exc import IntegrityError
from models import *

company_bp = Blueprint("company", __name__)

@company_bp.route("/company/dashboard")
def company_dashboard():
    user_id = session.get("user_id")
    user = User.query.filter(User.user_id == user_id).first()
    if (not (user_id and user.role == "Company")):
        return redirect(url_for("auth.login"))
    
    return render_template("/company/dashboard.html", current_user_role="Company")