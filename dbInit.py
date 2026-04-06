from datetime import date, timedelta
from app import app
from models import *
from extensions import db


# ------------------ STUDENTS ------------------
students = [
    {"name": "Jerry", "email": "jerry@gmail.com", "skills": "C++, SQL", "dept": "CSE", "course": "DS", "resume_path": "https://www.jerry.com", "is_active": True},
    {"name": "Spike", "email": "spike@gmail.com", "skills": "C, Java", "dept": "ISE", "course": "OS", "resume_path": "https://www.spike.com", "is_active": True},
    {"name": "Alice", "email": "alice@gmail.com", "skills": "Python, Flask, SQL", "dept": "CSE", "course": "DBMS", "resume_path": "https://www.alice.com", "is_active": True},
    {"name": "Bob", "email": "bob@gmail.com", "skills": "Java, Spring Boot", "dept": "ISE", "course": "OOP", "resume_path": "https://www.bob.com", "is_active": True},
    {"name": "Charlie", "email": "charlie@gmail.com", "skills": "JavaScript, Vue, HTML, CSS", "dept": "CSE", "course": "Web Dev", "resume_path": "https://www.charlie.com", "is_active": True},
]

# ------------------ COMPANIES ------------------
companies = [
    {"name": "Google", "email": "google@gmail.com", "website": "https://www.google.com", "status": "Approved"},
    {"name": "Microsoft", "email": "microsoft@gmail.com", "website": "https://www.microsoft.com", "status": "Approved"},
    {"name": "Infosys", "email": "infosys@gmail.com", "website": "https://www.infosys.com", "status": "Approved"},
]

# ------------------ DRIVES ------------------
drives = [
    {"company_email": "google@gmail.com", "job_title": "Software Engineer Intern", "description": "Backend work", "eligibility": "CSE, Python", "deadline": date.today() + timedelta(days=10), "status": "Approved"},
    {"company_email": "microsoft@gmail.com", "job_title": "SDE Intern", "description": "Cloud + Dev tools", "eligibility": "CSE, DSA", "deadline": date.today() + timedelta(days=8), "status": "Approved"},
]

# ------------------ APPLICATIONS ------------------
applications = [
    {"student_email": "jerry@gmail.com", "company_email": "google@gmail.com", "job_title": "Software Engineer Intern", "status": "Applied"},
    {"student_email": "alice@gmail.com", "company_email": "google@gmail.com", "job_title": "Software Engineer Intern", "status": "Selected"},
    {"student_email": "bob@gmail.com", "company_email": "microsoft@gmail.com", "job_title": "SDE Intern", "status": "Rejected"},
]


# ------------------ BUILD USERS ------------------
users = []

for student in students:
    users.append({
        "email": student["email"],
        "password": "1234",
        "role": "Student",
        "is_active": student["is_active"]
    })

for company in companies:
    users.append({
        "email": company["email"],
        "password": "1234",
        "role": "Company",
        "is_active": company["status"] == "Approved"
    })


# ------------------ DB INIT ------------------
with app.app_context():

    # Optional reset (use only if needed)
    # Application.query.delete()
    # Drive.query.delete()
    # Student.query.delete()
    # Company.query.delete()
    # User.query.delete()
    # db.session.commit()

    # -------- USERS --------
    for user in users:
        if not User.query.filter_by(email=user["email"]).first():
            u = User(
                email=user["email"],
                role=user["role"],
                is_active=user["is_active"]
            )
            u.set_password(user["password"])
            db.session.add(u)
    db.session.commit()

    # -------- STUDENTS --------
    for student in students:
        user = User.query.filter_by(email=student["email"]).first()
        if user and not Student.query.filter_by(user_id=user.user_id).first():
            s = Student(
                name=student["name"],
                skills=student["skills"],
                dept=student["dept"],
                course=student["course"],
                resume_path=student["resume_path"],
                user_id=user.user_id
            )
            db.session.add(s)
    db.session.commit()

    # -------- COMPANIES --------
    for company in companies:
        user = User.query.filter_by(email=company["email"]).first()
        if user and not Company.query.filter_by(user_id=user.user_id).first():
            c = Company(
                name=company["name"],
                website=company["website"],
                status=company["status"],
                user_id=user.user_id
            )
            db.session.add(c)
    db.session.commit()

    # -------- DRIVES --------
    for drive in drives:
        company_user = User.query.filter_by(email=drive["company_email"]).first()
        if company_user:
            company = Company.query.filter_by(user_id=company_user.user_id).first()

            if company and company.status == "Approved":
                if not Drive.query.filter_by(
                    company_id=company.company_id,
                    job_title=drive["job_title"]
                ).first():

                    d = Drive(
                        company_id=company.company_id,
                        job_title=drive["job_title"],
                        description=drive["description"],
                        eligibility=drive["eligibility"],
                        deadline=drive["deadline"],
                        status=drive["status"]
                    )
                    db.session.add(d)
    db.session.commit()

    # -------- APPLICATIONS --------
    for app_data in applications:
        student_user = User.query.filter_by(email=app_data["student_email"]).first()
        company_user = User.query.filter_by(email=app_data["company_email"]).first()

        if student_user and company_user:
            student = Student.query.filter_by(user_id=student_user.user_id).first()
            company = Company.query.filter_by(user_id=company_user.user_id).first()

            if student and company:
                drive = Drive.query.filter_by(
                    company_id=company.company_id,
                    job_title=app_data["job_title"]
                ).first()

                if drive and not Application.query.filter_by(
                    drive_id=drive.drive_id,
                    student_id=student.student_id
                ).first():

                    today = date.today()

                    # ---- HISTORY LOGIC ----
                    history = f"Applied ({today})"

                    if app_data["status"] == "Selected":
                        history += f",Selected ({today})"
                    elif app_data["status"] == "Rejected":
                        history += f",Rejected ({today})"

                    a = Application(
                        drive_id=drive.drive_id,
                        student_id=student.student_id,
                        applied_on=today - timedelta(days=2),
                        status=app_data["status"],
                        history=history
                    )

                    db.session.add(a)

    db.session.commit()

    print("✅ Mock data inserted successfully.")