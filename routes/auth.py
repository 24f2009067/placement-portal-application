from flask import Blueprint, render_template, request, url_for, redirect, session
from sqlalchemy.exc import IntegrityError
from models import *

auth_bp = Blueprint("auth", __name__)

# Student ---------------------------------------------------------------------------------------------------------------
@auth_bp.route("/student/register", methods=["GET", "POST"])
def student_register():
    if request.method == "GET":
        return render_template("student/register.html", current_user_role="User")

    elif request.method == "POST":
        form = request.form
        name = form["name"].strip().title()
        email = form["email"].strip().lower()
        password = form["password"]
        skills = form["skills"].strip()
        dept = form["dept"].strip().upper()
        course = form["course"].strip().upper()
        resume = form["resume"].strip()

        try:
            user = User(email=email, role="Student")
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            user = User.query.filter(User.email == email).first()

            student = Student(name=name, user_id=user.user_id, skills=skills, dept=dept, course=course, resume_path=resume)
            db.session.add(student)
            db.session.commit()
        except(IntegrityError):
            db.session.rollback()
            return render_template("student/register.html", current_user_role="User", message="Email already exists!")

        return render_template("student/register.html", current_user_role="User", message="Registration Successfull!")

# Company ---------------------------------------------------------------------------------------------------------------
@auth_bp.route("/company/register", methods=["GET", "POST"])
def company_register():
    if request.method == "GET":
        return render_template("company/register.html", current_user_role="User")

    elif request.method == "POST":
        form = request.form
        name = form["name"].strip().title()
        email = form["email"].strip().lower()
        password = form["password"]
        website = form["website"].strip()

        try:
            user = User(email=email, role="Company")
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            user = User.query.filter(User.email == email).first()

            company = Company(user_id=user.user_id, name=name, website=website)
            db.session.add(company)
            db.session.commit()
        except(IntegrityError):
            db.session.rollback()
            return render_template("company/register.html", current_user_role="User", message="Email already exists!")

        return render_template("company/register.html", current_user_role="User", message="Registration Successfull!")
    

# Common Login and Logout Functions -------------------------------------------------------------------------------------
@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", current_user_role="User")
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            session["user_id"] = user.user_id
            role = user.role
            return redirect(url_for(f"{role.lower()}.{role.lower()}_dashboard"))
        else:
            return render_template("login.html", current_user_role="User", message="Incorrect Email or Password!")

@auth_bp.route("/logout")
def logout():
    if "user_id" in session:
        session.clear()
    return redirect("/")
