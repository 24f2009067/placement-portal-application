from datetime import date, timedelta
from app import app
from models import *

students = [
    {"name": "Jerry", "email": "jerry@gmail.com", "skills": "C++, SQL", "dept": "CSE", "course": "DS", "resume_path": "https://www.jerry.com", "is_active": True},
    {"name": "Spike", "email": "spike@gmail.com", "skills": "C, Java", "dept": "ISE", "course": "OS", "resume_path": "https://www.spike.com", "is_active": True},
    {"name": "Alice", "email": "alice@gmail.com", "skills": "Python, Flask, SQL", "dept": "CSE", "course": "DBMS", "resume_path": "https://www.alice.com", "is_active": True},
    {"name": "Bob", "email": "bob@gmail.com", "skills": "Java, Spring Boot", "dept": "ISE", "course": "OOP", "resume_path": "https://www.bob.com", "is_active": True},
    {"name": "Charlie", "email": "charlie@gmail.com", "skills": "JavaScript, Vue, HTML, CSS", "dept": "CSE", "course": "Web Dev", "resume_path": "https://www.charlie.com", "is_active": True},
    {"name": "David", "email": "david@gmail.com", "skills": "C, Data Structures", "dept": "ECE", "course": "DSA", "resume_path": "https://www.david.com", "is_active": False},
    {"name": "Eva", "email": "eva@gmail.com", "skills": "Python, Machine Learning", "dept": "AIML", "course": "ML", "resume_path": "https://www.eva.com", "is_active": True},
    {"name": "Frank", "email": "frank@gmail.com", "skills": "C++, Operating Systems", "dept": "CSE", "course": "OS", "resume_path": "https://www.frank.com", "is_active": True},
    {"name": "Grace", "email": "grace@gmail.com", "skills": "SQL, Power BI, Excel", "dept": "ISE", "course": "Data Analytics", "resume_path": "https://www.grace.com", "is_active": True},
    {"name": "Henry", "email": "henry@gmail.com", "skills": "Java, JDBC, Servlets", "dept": "CSE", "course": "Java", "resume_path": "https://www.henry.com", "is_active": True},
    {"name": "Ivy", "email": "ivy@gmail.com", "skills": "React, Node.js, MongoDB", "dept": "AIDS", "course": "Full Stack", "resume_path": "https://www.ivy.com", "is_active": False},
    {"name": "Jack", "email": "jack@gmail.com", "skills": "C#, .NET, SQL Server", "dept": "ISE", "course": ".NET", "resume_path": "https://www.jack.com", "is_active": True},
    {"name": "Karen", "email": "karen@gmail.com", "skills": "Python, Pandas, NumPy", "dept": "CSE", "course": "Data Science", "resume_path": "https://www.karen.com", "is_active": True},
    {"name": "Leo", "email": "leo@gmail.com", "skills": "JavaScript, React, Node.js", "dept": "AIDS", "course": "MERN", "resume_path": "https://www.leo.com", "is_active": True},
    {"name": "Mia", "email": "mia@gmail.com", "skills": "UI/UX, Figma, HTML, CSS", "dept": "ISE", "course": "UI Design", "resume_path": "https://www.mia.com", "is_active": True},
    {"name": "Nina", "email": "nina@gmail.com", "skills": "Java, DSA, OOP", "dept": "CSE", "course": "Java", "resume_path": "https://www.nina.com", "is_active": True},
    {"name": "Oscar", "email": "oscar@gmail.com", "skills": "Linux, Bash, Docker", "dept": "CSE", "course": "DevOps", "resume_path": "https://www.oscar.com", "is_active": True},
    {"name": "Paul", "email": "paul@gmail.com", "skills": "C, Embedded Systems", "dept": "ECE", "course": "Embedded", "resume_path": "https://www.paul.com", "is_active": True},
]

companies = [
    {"name": "Tom", "email": "tom@gmail.com", "website": "https://www.tom.com", "status": "Pending"},
    {"name": "Google", "email": "google@gmail.com", "website": "https://www.google.com", "status": "Approved"},
    {"name": "Microsoft", "email": "microsoft@gmail.com", "website": "https://www.microsoft.com", "status": "Approved"},
    {"name": "Amazon", "email": "amazon@gmail.com", "website": "https://www.amazon.com", "status": "Pending"},
    {"name": "Infosys", "email": "infosys@gmail.com", "website": "https://www.infosys.com", "status": "Approved"},
    {"name": "TCS", "email": "tcs@gmail.com", "website": "https://www.tcs.com", "status": "Rejected"},
    {"name": "Wipro", "email": "wipro@gmail.com", "website": "https://www.wipro.com", "status": "Pending"},
    {"name": "Accenture", "email": "accenture@gmail.com", "website": "https://www.accenture.com", "status": "Approved"},
    {"name": "IBM", "email": "ibm@gmail.com", "website": "https://www.ibm.com", "status": "Approved"},
    {"name": "Oracle", "email": "oracle@gmail.com", "website": "https://www.oracle.com", "status": "Approved"},
    {"name": "Zoho", "email": "zoho@gmail.com", "website": "https://www.zoho.com", "status": "Approved"},
    {"name": "Capgemini", "email": "capgemini@gmail.com", "website": "https://www.capgemini.com", "status": "Pending"},
]

# Only APPROVED companies are allowed to create drives
drives = [
    {"company_email": "google@gmail.com", "job_title": "Software Engineer Intern", "description": "Work on backend systems and APIs.", "eligibility": "CSE/ISE, CGPA >= 8.0, Python/Java", "deadline": date.today() + timedelta(days=10), "status": "Approved"},
    {"company_email": "google@gmail.com", "job_title": "Frontend Intern", "description": "Build UI components and dashboards.", "eligibility": "CSE/ISE, JavaScript/React", "deadline": date.today() + timedelta(days=12), "status": "Approved"},
    {"company_email": "google@gmail.com", "job_title": "Site Reliability Intern", "description": "Monitor services and improve infrastructure reliability.", "eligibility": "CSE/ISE, Linux, Networking basics", "deadline": date.today() - timedelta(days=5), "status": "Closed"},

    {"company_email": "microsoft@gmail.com", "job_title": "SDE Intern", "description": "Work on cloud and developer tools.", "eligibility": "CSE/AIML, CGPA >= 7.5, DSA", "deadline": date.today() + timedelta(days=8), "status": "Approved"},
    {"company_email": "microsoft@gmail.com", "job_title": "QA Intern", "description": "Assist in testing enterprise software products.", "eligibility": "CSE/ISE, Testing basics, Java/Python", "deadline": date.today() - timedelta(days=3), "status": "Closed"},

    {"company_email": "infosys@gmail.com", "job_title": "Systems Engineer", "description": "Entry level software role.", "eligibility": "All branches, CGPA >= 6.5", "deadline": date.today() + timedelta(days=20), "status": "Approved"},
    {"company_email": "infosys@gmail.com", "job_title": "Support Trainee", "description": "Support applications and internal systems.", "eligibility": "All branches, communication skills", "deadline": date.today() - timedelta(days=7), "status": "Closed"},

    {"company_email": "accenture@gmail.com", "job_title": "Associate Software Engineer", "description": "Work on enterprise applications.", "eligibility": "All CS related branches, CGPA >= 7.0", "deadline": date.today() + timedelta(days=14), "status": "Approved"},

    {"company_email": "ibm@gmail.com", "job_title": "Data Analyst Intern", "description": "Analyze data and create reports.", "eligibility": "CSE/ISE/AIML, SQL, Python", "deadline": date.today() + timedelta(days=9), "status": "Approved"},

    {"company_email": "oracle@gmail.com", "job_title": "Database Intern", "description": "Work on DB support and SQL optimization.", "eligibility": "CSE/ISE, SQL, DBMS", "deadline": date.today() + timedelta(days=11), "status": "Approved"},

    {"company_email": "zoho@gmail.com", "job_title": "Web Developer Intern", "description": "Develop internal web tools.", "eligibility": "JavaScript, HTML, CSS, any CS branch", "deadline": date.today() + timedelta(days=13), "status": "Approved"},
]

# Replaced all "Shortlisted" with "Selected"
applications = [
    {"student_email": "jerry@gmail.com", "company_email": "google@gmail.com", "job_title": "Software Engineer Intern", "status": "Applied"},
    {"student_email": "alice@gmail.com", "company_email": "google@gmail.com", "job_title": "Frontend Intern", "status": "Selected"},
    {"student_email": "bob@gmail.com", "company_email": "microsoft@gmail.com", "job_title": "SDE Intern", "status": "Applied"},
    {"student_email": "charlie@gmail.com", "company_email": "zoho@gmail.com", "job_title": "Web Developer Intern", "status": "Selected"},
    {"student_email": "eva@gmail.com", "company_email": "ibm@gmail.com", "job_title": "Data Analyst Intern", "status": "Selected"},
    {"student_email": "frank@gmail.com", "company_email": "infosys@gmail.com", "job_title": "Systems Engineer", "status": "Applied"},
    {"student_email": "grace@gmail.com", "company_email": "oracle@gmail.com", "job_title": "Database Intern", "status": "Applied"},
    {"student_email": "henry@gmail.com", "company_email": "accenture@gmail.com", "job_title": "Associate Software Engineer", "status": "Rejected"},
    {"student_email": "jack@gmail.com", "company_email": "infosys@gmail.com", "job_title": "Systems Engineer", "status": "Selected"},
    {"student_email": "karen@gmail.com", "company_email": "ibm@gmail.com", "job_title": "Data Analyst Intern", "status": "Applied"},
    {"student_email": "leo@gmail.com", "company_email": "google@gmail.com", "job_title": "Frontend Intern", "status": "Applied"},
    {"student_email": "mia@gmail.com", "company_email": "zoho@gmail.com", "job_title": "Web Developer Intern", "status": "Selected"},
    {"student_email": "nina@gmail.com", "company_email": "microsoft@gmail.com", "job_title": "SDE Intern", "status": "Rejected"},
]

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

with app.app_context():
    # Uncomment these if you want a fresh reset before seeding
    # Application.query.delete()
    # Drive.query.delete()
    # Student.query.delete()
    # Company.query.delete()
    # User.query.delete()
    # db.session.commit()

    for user in users:
        existing_user = User.query.filter_by(email=user["email"]).first()
        if not existing_user:
            u = User(
                email=user["email"],
                role=user["role"],
                is_active=user["is_active"]
            )
            u.set_password(user["password"])
            db.session.add(u)
    db.session.commit()

    for student in students:
        user = User.query.filter_by(email=student["email"]).first()
        if user:
            existing_student = Student.query.filter_by(user_id=user.user_id).first()
            if not existing_student:
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

    for company in companies:
        user = User.query.filter_by(email=company["email"]).first()
        if user:
            existing_company = Company.query.filter_by(user_id=user.user_id).first()
            if not existing_company:
                c = Company(
                    name=company["name"],
                    website=company["website"],
                    status=company["status"],
                    user_id=user.user_id
                )
                db.session.add(c)
    db.session.commit()

    for drive in drives:
        company_user = User.query.filter_by(email=drive["company_email"]).first()
        if company_user:
            company = Company.query.filter_by(user_id=company_user.user_id).first()
            if company and company.status == "Approved":
                existing_drive = Drive.query.filter_by(
                    company_id=company.company_id,
                    job_title=drive["job_title"]
                ).first()
                if not existing_drive:
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

                if drive:
                    existing_application = Application.query.filter_by(
                        drive_id=drive.drive_id,
                        student_id=student.student_id
                    ).first()

                    if not existing_application:
                        a = Application(
                            drive_id=drive.drive_id,
                            student_id=student.student_id,
                            status=app_data["status"]
                        )

                        if hasattr(a, "applied_on"):
                            a.applied_on = date.today() - timedelta(days=2)

                        db.session.add(a)
    db.session.commit()

    print("Mock data inserted successfully.")