from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pymysql
from pymysql.cursors import DictCursor
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import date
import calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

# MySQL Database
db = pymysql.connect(
    host='localhost',
    user='root',
    database='gym_details',
    password='ujjwal123',
    cursorclass=DictCursor
)
cursor = db.cursor()

# JWT setup
jwt = JWTManager(app)

# --- Decorators ---
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_roles = claims.get('role', [])
            if not any(role in user_roles for role in roles):
                return jsonify({'message': 'Unauthorized access'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

# --- Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute('SELECT * FROM user_details WHERE email = %s', (email,))
        user = cursor.fetchone()
        if not user:
            flash('User does not exist. Please sign up.')
            return redirect(url_for('login'))

        if check_password_hash(user['password'], password):
            # Fetch user roles
            cursor.execute("""
                SELECT roles.name 
                FROM roles 
                JOIN roles_users ON roles.id = roles_users.role_id 
                WHERE roles_users.user_id = %s
            """, (user['id'],))
            roles = [row['name'] for row in cursor.fetchall()]

            # Create JWT
            access_token = create_access_token(identity=str(user['id']), additional_claims={"role": roles})
            response = redirect(url_for('grand'))
            response.set_cookie('access_token', access_token, httponly=True)
            return response
        else:
            flash('Incorrect password')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    selected_membership = request.args.get('membership')
    price = request.args.get('price')
    description = request.args.get('description')
    duration = int(request.args.get('duration', 0))
    #get class details from url 
    class_name = request.args.get('name')
    class_description = request.args.get('description')
    class_trainer = request.args.get('trainer')
    class_time = request.args.get('time')

    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        role_name = request.form['role']
        password = request.form['password']
        selected_membership = request.form.get('membership')
        price = request.form.get('price')
        description = request.form.get('description')
        duration = int(request.form.get('duration', 0))
        #class info from url 
        class_name = request.form.get('class_name')
        class_time = request.form.get('time')
        class_description = request.form.get('description')
        class_trainer = request.form.get('trainer')

        hashed_password = generate_password_hash(password)

        cursor.execute("SELECT * FROM user_details WHERE username = %s AND email = %s", (username, email))
        if cursor.fetchone():
            flash('User already exists. Try logging in.')
            return redirect(url_for('signup'))

        # Insert user
        cursor.execute("""
            INSERT INTO user_details(username, name, email, password, phone, address) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, name, email, hashed_password, phone, address))
        user_id = cursor.lastrowid

        # Assign role
        cursor.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
        role = cursor.fetchone()
        role_id = role['id'] if role else None
        if not role_id:
            cursor.execute("INSERT INTO roles(name) VALUES(%s)", (role_name,))
            role_id = cursor.lastrowid

        cursor.execute("INSERT INTO roles_users(user_id, role_id) VALUES(%s, %s)", (user_id, role_id))

        # Assign membership
        cursor.execute("SELECT id FROM memberships WHERE name = %s", (selected_membership,))
        membership = cursor.fetchone()
        if not membership:
            cursor.execute("INSERT INTO memberships(name, price, description) VALUES(%s, %s, %s)",
                           (selected_membership, price, description))
            membership_id = cursor.lastrowid
        else:
            membership_id = membership['id']

        start_date = date.today()
        raw_month = start_date.month + duration
        end_year = start_date.year + (raw_month - 1) // 12
        end_month = (raw_month - 1) % 12 + 1
        end_day = min(start_date.day, calendar.monthrange(end_year, end_month)[1])
        end_date = date(end_year, end_month, end_day)

        cursor.execute("""
            INSERT INTO user_memberships(user_id, membership_id, end_date, duration, start_date) 
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, membership_id, end_date, duration, start_date))

        # Optional assign class enrollment
        if class_name:
            cursor.execute("SELECT id FROM classes WHERE name =%s",(class_name,))
            classes = cursor.fetchone()
            class_id = classes['id']

            #prevent duplicate enrollments 
            cursor.execute("SELECT * from enrollments WHERE user_id =%s AND class_is = %s", (user_id, class_id))
            if not cursor.fetchone():
            #assign enrollment
                cursor.execute("INSERT INTO enrollments(user_id, class_id, started_date) VALUES(%s, %s, %s)", (user_id, class_id, start_date))
                db.commit()
            else:
                flash('User successfully enrolled ')  
        return redirect(url_for('login'))

    return render_template('signup.html', membership=selected_membership, price=price,
                           description=description, duration=duration, class_info ={"name":class_name,"description":class_description, "time":class_time, "trainer":class_trainer} )


@app.route('/')
def dashboard():
    cursor.execute("SELECT name, price, description FROM memberships")
    membership = cursor.fetchall()
    return render_template('index.html', membership=membership)


@app.route('/grand')
@role_required('admin', 'member')
def grand():
    cursor.execute("SELECT name, description, trainer, time FROM classes")
    class_data = cursor.fetchall()

    cursor.execute("SELECT name, price, description FROM memberships")
    membership_list = cursor.fetchall()

    user_id = get_jwt_identity()

    cursor.execute("SELECT * FROM user_details WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()

    cursor.execute("""
        SELECT roles.name 
        FROM roles JOIN roles_users ON roles.id = roles_users.role_id 
        WHERE roles_users.user_id = %s
    """, (user_id,))
    role_row = cursor.fetchone()
    role_name = role_row['name'] if role_row else None 

    cursor.execute("""
        SELECT memberships.name 
        FROM memberships 
        JOIN user_memberships ON memberships.id = user_memberships.membership_id 
        WHERE user_memberships.user_id = %s
    """, (user_id,))
    membership_row = cursor.fetchone()
    membership_name = membership_row['name'] if membership_row else None

    cursor.execute("SELECT start_date, end_date FROM user_memberships WHERE user_id = %s", (user_id,))
    dates = cursor.fetchone()


    return render_template('grand.html', user=user_data, role=role_name,
                           membership=membership_name, dates=dates,
                           member=membership_list, classes=class_data)

#add_membership 
@app.route('/add_membership', methods=['GET', 'POST'])
@role_required('admin')
def add_membership():
    # cursor = pymysql.connection.cursor()
    user_id = get_jwt_identity()
    if request.method == 'POST':
        membership_name = request.form['membership_name']
        price = request.form['price']
        selected_class_ids = request.form.getlist('selected_classes')

        #check membership 
        cursor.execute("SELECT * FROM memberships WHERE name=%s",(membership_name))
        if cursor.fetchone():
            flash("membership already exsist")
            return redirect(url_for('add_membership'))
        # insert new membership 
        class_desc =[]
        for cls_id in selected_class_ids:
            cursor.execute("SELECT * FROM classes WHERE id =%s",(cls_id,))
            cls = cursor.fetchone()
            if cls:
                desc = f"Include class {cls['name']} on {cls['time']} with {cls['trainer']} for {cls['description']}"
                class_desc.append(desc)
                print(class_desc)
                print(desc)
                cursor.execute("INSERT INTO memberships(name, price, description) VALUES(%s, %s, %s)",(membership_name, price, desc))
                db.commit()
                flash("membership created succesfully!")
            return redirect(url_for('grand'))

    # get request
    cursor.execute("SELECT * FROM classes")
    class_data =cursor.fetchall()

    return render_template('add_membership.html', class_data = class_data)

#member profile 
@app.route('/profile')
@role_required('trainer', 'member')
def profile():
    user_id = get_jwt_identity()
    cursor.execute("SELECT username, name, email, phone, address FROM user_details WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    return render_template('profile.html', user=user_data)


@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.delete_cookie('access_token')
    return response


if __name__ == '__main__':
    app.run(debug=True)