from flask import Blueprint, render_template, request

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
@auth_bp.route("/home")
def home():
    return render_template("home.html", current_user_role="User")

# Admin -----------------------------------------------------------------------------------------------------------------
@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin/login.html", current_user_role="User")

# Student ---------------------------------------------------------------------------------------------------------------
@auth_bp.route("/student/login", methods=["GET", "POST"])
def student_login():
    if request.method == "GET":
        return render_template("student/login.html", current_user_role="User")

@auth_bp.route("/student/register", methods=["GET", "POST"])
def student_register():
    if request.method == "GET":
        return render_template("student/register.html", current_user_role="User")

# Company ---------------------------------------------------------------------------------------------------------------
@auth_bp.route("/company/login", methods=["GET", "POST"])
def company_login():
    if request.method == "GET":
        return render_template("company/login.html", current_user_role="User")

@auth_bp.route("/company/register", methods=["GET", "POST"])
def company_register():
    if request.method == "GET":
        return render_template("company/register.html", current_user_role="User")