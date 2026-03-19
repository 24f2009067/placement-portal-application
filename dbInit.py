from app import app
from models import *

users = [
    {"email": "jerry@gmail.com", "password": "1234", "role": "Student"},
    {"email": "spike@gmail.com", "password": "1234", "role": "Student"},
    {"email": "alice@gmail.com", "password": "1234", "role": "Student"},
    {"email": "bob@gmail.com", "password": "1234", "role": "Student"},
    {"email": "charlie@gmail.com", "password": "1234", "role": "Student"},
    {"email": "david@gmail.com", "password": "1234", "role": "Student", "is_active": False},
    {"email": "eva@gmail.com", "password": "1234", "role": "Student"},
    {"email": "frank@gmail.com", "password": "1234", "role": "Student"},
    {"email": "grace@gmail.com", "password": "1234", "role": "Student"},
    {"email": "henry@gmail.com", "password": "1234", "role": "Student"},
    {"email": "ivy@gmail.com", "password": "1234", "role": "Student", "is_active": False},
    {"email": "jack@gmail.com", "password": "1234", "role": "Student"},

    {"email": "tom@gmail.com", "password": "1234", "role": "Company", "is_active": False},
    {"email": "google@gmail.com", "password": "1234", "role": "Company"},
    {"email": "microsoft@gmail.com", "password": "1234", "role": "Company"},
    {"email": "amazon@gmail.com", "password": "1234", "role": "Company", "is_active": False},
    {"email": "infosys@gmail.com", "password": "1234", "role": "Company"},
    {"email": "tcs@gmail.com", "password": "1234", "role": "Company", "is_active": False},
    {"email": "wipro@gmail.com", "password": "1234", "role": "Company", "is_active": False},
]

students = [
    {"name": "Jerry", "email": "jerry@gmail.com", "skills": "C++, SQL", "dept": "CSE", "course": "DS", "resume_path": "www.jerry.com"},
    {"name": "Spike", "email": "spike@gmail.com", "skills": "C, Java", "dept": "ISE", "course": "OS", "resume_path": "www.spike.com"},
    {"name": "Alice", "email": "alice@gmail.com", "skills": "Python, Flask, SQL", "dept": "CSE", "course": "DBMS", "resume_path": "www.alice.com"},
    {"name": "Bob", "email": "bob@gmail.com", "skills": "Java, Spring Boot", "dept": "ISE", "course": "OOP", "resume_path": "www.bob.com"},
    {"name": "Charlie", "email": "charlie@gmail.com", "skills": "JavaScript, Vue, HTML, CSS", "dept": "CSE", "course": "Web Dev", "resume_path": "www.charlie.com"},
    {"name": "David", "email": "david@gmail.com", "skills": "C, Data Structures", "dept": "ECE", "course": "DSA", "resume_path": "www.david.com"},
    {"name": "Eva", "email": "eva@gmail.com", "skills": "Python, Machine Learning", "dept": "AIML", "course": "ML", "resume_path": "www.eva.com"},
    {"name": "Frank", "email": "frank@gmail.com", "skills": "C++, Operating Systems", "dept": "CSE", "course": "OS", "resume_path": "www.frank.com"},
    {"name": "Grace", "email": "grace@gmail.com", "skills": "SQL, Power BI, Excel", "dept": "ISE", "course": "Data Analytics", "resume_path": "www.grace.com"},
    {"name": "Henry", "email": "henry@gmail.com", "skills": "Java, JDBC, Servlets", "dept": "CSE", "course": "Java", "resume_path": "www.henry.com"},
    {"name": "Ivy", "email": "ivy@gmail.com", "skills": "React, Node.js, MongoDB", "dept": "AIDS", "course": "Full Stack", "resume_path": "www.ivy.com"},
    {"name": "Jack", "email": "jack@gmail.com", "skills": "C#, .NET, SQL Server", "dept": "ISE", "course": ".NET", "resume_path": "www.jack.com"},
]

companies = [
    {"name": "Tom", "email": "tom@gmail.com", "website": "www.tom.com", "status": "Pending"},
    {"name": "Google", "email": "google@gmail.com", "website": "www.google.com", "status": "Approved"},
    {"name": "Microsoft", "email": "microsoft@gmail.com", "website": "www.microsoft.com", "status": "Approved"},
    {"name": "Amazon", "email": "amazon@gmail.com", "website": "www.amazon.com", "status": "Pending"},
    {"name": "Infosys", "email": "infosys@gmail.com", "website": "www.infosys.com", "status": "Approved"},
    {"name": "TCS", "email": "tcs@gmail.com", "website": "www.tcs.com", "status": "Rejected"},
    {"name": "Wipro", "email": "wipro@gmail.com", "website": "www.wipro.com", "status": "Pending"},
]



with app.app_context():
    for user in users:
        u = User(email=user["email"], role=user["role"], is_active=user.get("is_active", True))
        u.set_password(user["password"])
        db.session.add(u)
    db.session.commit()


    for student in students:
        user = User.query.filter(User.email == student["email"]).first()
        uid = user.user_id
        s = Student(name=student["name"], skills=student["skills"], dept = student["dept"], course=student["course"], resume_path=student["resume_path"], user_id=uid)
        db.session.add(s)
    db.session.commit()

    for company in companies:
        user = User.query.filter(User.email == company["email"]).first()
        uid = user.user_id
        c = Company(name=company["name"], website=company["website"], status = company["status"], user_id=uid)
        db.session.add(c)
    db.session.commit()