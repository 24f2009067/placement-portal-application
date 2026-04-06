# Placement Portal (MAD-1 Project)

A **role-based web application** developed using **Flask** that streamlines campus placement activities by enabling structured interaction between **Admin (Institute Placement Cell), Companies,** and **Students**.

The application replaces manual processes such as spreadsheets and emails with a centralized system for managing company **approvals, placement drives, student applications, and placement history**.


## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite + SQLAlchemy ORM
- **Frontend:** HTML, Jinja2
- **Styling:** Bootstrap 5, CSS


## Features

###  Student
- Register and login
- View available company drives
- Apply to drives
- Track application status
- View application history
- Receive notifications on status changes

### Admin
- Create and manage company drives
- View student applications
- Update application status
- Manage users and companies
- Monitor activity


### Company
- Provide company details
- Create placement drives (if allowed)
- Define eligibility criteria
- View applicants for their drives
- Select / Reject / Shortlist candidates

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/24f2009067/placement-portal-application.git

```

### 2. install dependencies
```bash
cd placement-portal-application
pip install -r requirements.txt

```

### 3. Start app
```bash
python ./app.py
```

> **Note:** Admin Email: admin@ppa.com, Default password: password

## Project Structure

    placement-portal-application/
    ├── app.py
    ├── dbInit.py
    ├── extensions.py
    ├── instance
    │   └── placement_portal.db
    ├── issues.md
    ├── models.py
    ├── README.md
    ├── requirements.txt
    ├── routes
    │   ├── admin.py
    │   ├── auth.py
    │   ├── company.py
    │   └── student.py
    ├── static
    │   ├── dark_mode.svg
    │   ├── light_mode.svg
    │   └── style.css
    ├── templates
    │   ├── admin
    │   │   ├── application.html
    │   │   ├── dashboard.html
    │   │   └── drive.html
    │   ├── base.html
    │   ├── company
    │   │   ├── application.html
    │   │   ├── createDrive.html
    │   │   ├── dashboard.html
    │   │   ├── drive.html
    │   │   ├── register.html
    │   │   └── updateDrive.html
    │   ├── components
    │   │   └── navbar.html
    │   ├── login.html
    │   └── student
    │       ├── company.html
    │       ├── dashboard.html
    │       ├── drive.html
    │       ├── editProfile.html
    │       ├── history.html
    │       ├── notifications.html
    │       └── register.html
    └── tests.md


## Author
Prajin GN (24f2009067)
