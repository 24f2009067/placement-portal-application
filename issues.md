# Issues

### 1. Preserve user login status

    solution: Use session to store user_id

### 2. Prevent accesing /role/dashboard without login
    
    solution: verify user_id is present in the session, else redirect to login page

### 3. Prevent accessing other role dashboards after login (e.g. student accessing /admin/dashboard after loging in as student)
    
    solution: verify role of user_id from session, and allow only if role matches corresponding dashboard

### 4. Duplicate logic for logins (Student, Admin, Company)
    
    solution: merge individual login page into single /login page and redirect based on role
