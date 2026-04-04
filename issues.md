# Issues

### 1. Preserve user login status

    solution: Use session to store user_id

### 2. Prevent accesing /role/dashboard without login

    solution: verify user_id is present in the session, else redirect to login page

### 3. Prevent accessing other role dashboards after login (e.g. student accessing /admin/dashboard after loging in as student)

    solution: verify role of user_id from session, and allow only if role matches corresponding dashboard

### 4. Duplicate logic for logins (Student, Admin, Company)

    solution: merge individual login page into single /login page and redirect based on role

### 5. No proper way to hangle student notifications

    solution: Create separate Notification table in the db with a one to many relaton with the student table

### 6. Using datetime.now() to remove drives past there due dates, removes drives on the last day of the due date instead of the next day.

    solution: remove drives that have deadlines < datetime.now() - timedelta(days=1), This removes drives whose due date has passed yesterday.

### 7. Notifications sent on the same day don't order themselves based on time.

    solution: Change db to use datetime insted of date. to order based on time and date.
