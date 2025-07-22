# gym-management-project

# 🏋️‍♂️ Gym Management Web App (Flask + MySQL)

A dynamic, role-based gym management system built with Flask and MySQL that supports user registration, login, membership management, class enrollment, and secure role-specific access using JWT.

---

## 🚀 Features

- 🔒 Secure **JWT-based authentication** using cookies
- 🧑‍💼 Role-based access control (Admin, Member, Trainer)
- 📝 Dynamic signup with **membership & class selection**
- 📅 Automatic calculation of membership **start and end dates**
- 🎯 Admin features: Add memberships with associated classes
- 🧾 MySQL-backed data storage
- 📄 Organized `templates/` for frontend rendering (HTML)

---

## 📁 Project Structure

```
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── UJJWAL.session.sql      # SQL setup and updates (commented)
├── templates/              # HTML templates (login, signup, dashboard, etc.)
└── static/                 # (Optional) CSS, JS, images
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ujjwal-154/gym-flask-app.git
cd gym-flask-app
```

### 2. Create Virtual Environment
```bash
python -m venv env
source env/bin/activate    # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database

- Create a database named `gym_details`
- Use the SQL script (`UJJWAL.session.sql`) to set up tables and insert initial data
- Update DB credentials in `app.py` if needed:
```python
db = pymysql.connect(
    host='localhost',
    user='root',
    password='ujjwal123',     # Change if different
    database='gym_details',
    cursorclass=DictCursor
)
```

---

## 🧪 Run the App

```bash
python app.py
```

Access the app at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📸 Screens (You can add screenshots here)

- Login Page
- Signup Page with Membership Options
- Dashboard (`/grand`) with Role-Based View
- Membership Add Page (Admin)

---

## 📌 Notes

- `.vscode/` and `env/` should not be uploaded to GitHub.
- JWT tokens are stored in cookies (`access_token`) and are used for route protection.
- `requirements.txt` includes Flask, JWT, and MySQL dependencies.

---

## 🙋‍♂️ Author

**Ujjwal Dhiman**

- 💼 [LinkedIn](https://www.linkedin.com/in/ujjwal-dhiman/)
- 📫 Email: dhimanujjwal072@gmail.com

---

## 🪪 License

This project is for educational and learning purposes.
