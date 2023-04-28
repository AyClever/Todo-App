import random

from flask import Flask, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["SECRET_KEY"] = "shaklfhzhjhgjj1111111111"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo_db.sqlite"

# Configure Flask-Mail settings for sending email
app.config['MAIL_SERVER'] = 'your-mail-server.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your-mail-username'
app.config['MAIL_PASSWORD'] = 'your-mail-password'
app.config['MAIL_DEFAULT_SENDER'] = 'sshorinola39004826@gmail.com'
mail = Mail(app)


db.init_app(app)
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"Users <{Users.name}>"


class Records(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    employment_type = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    def __init__(self, name, email, phone_number, date_of_birth, gender, empolyment_type, address):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.employment_type = empolyment_type
        self.address = address

    def __repr__(self):
        return f"Records <{Records.name}>"


@app.route("/", methods=['get', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # check_email = Users.query.filter_by(email=email).first()
        # if check_email == email:
        #     return f"Username Taken"
        if password == confirm_password:
            new_user = Users(name, email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
        else:
            return "invalid confirm_password"
    return render_template('signup.html')


@app.route('/login', methods=['get', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        check_user = Users.query.filter_by(email=email).first()
        if check_user and check_user.check_password(password):
            login_user(check_user)
            return redirect(url_for('dashboard', current_user=current_user, Tittle=dashboard))
        return "Invalid Login Credentials"
    return render_template('login.html')


@app.route('/forget password', methods=['get', 'POST'])
def forget_pass():
    a1 = random.randint(0, 19)
    a2 = random.randint(0, 19)
    ans = a1 + a2
    if request.method == 'POST':
        email = request.form['email']
        answer = int(request.form['answer'])
        check_user = Users.query.filter_by(email=email).first()
        if check_user:
            new_password = f"@abc{random.randint(1000, 9999)}"
            hashed_password = generate_password_hash(new_password)
            check_user.set_password(hashed_password)
            db.session.add(check_user)
            db.session.commit()

            msg = Message('Password Reset', recipients=['fayoseayomipo170@gmail.com'])
            msg.body = f'Your new password is: {new_password}'
            mail.send(msg)
            flash('Password reset successfully. Check your email for the new password.')
            return redirect(url_for('login'))
        else:
            return 'Invalid email address.'
    return render_template('forget_pass.html', first_number=a1, second_number=a2)


@app.route('/add-record', methods=['get', 'POST'])
def add_record():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        dob = request.form['dob']
        gender = request.form['gender']
        employment_type = request.form['employment_type']
        address = request.form['address']
        new_record = Records(name, email, phone_number, dob, gender, employment_type, address)
        db.session.add(new_record)
        db.session.commit()
        return render_template('add-record.html')
    return render_template('add-record.html')


@app.route('/view-all', methods=['get', 'POST'])
def view_all():
    view_all = Records.query.all()

    return render_template('view-all.html', records=view_all)


@app.route('/view-single')
def view_single():
    user_id = request.args.get('view')
    single = Records.query.filter_by(id=user_id).first()
    return render_template('view-single.html', records=single)


@app.route('/delete')
def delete():
    user_id = request.args.get('view')
    single = Records.query.filter_by(id=user_id).first()
    name = single.name
    db.session.delete(single)
    db.session.commit()
    return redirect(url_for('view_all'))


@app.route('/edit', methods=['get', 'POST'])
def edit():
    if request.method == 'POST':
        id = request.form['id']
        new_name = request.form['name']
        new_email = request.form['email']
        new_phone_number = request.form['phone_number']
        new_dob = request.form['dob']
        new_gender = request.form['gender']
        new_employment_type = request.form['employment_type']
        new_address = request.form['address']

        single = Records.query.filter_by(id=id).first()
        single.name = new_name
        single.email = new_email
        single.phone_number = new_phone_number
        single.dob = new_dob
        single.gender = new_gender
        single.employment_type = new_employment_type
        single.address = new_address
        db.session.add(single)
        db.session.commit()
        return redirect(url_for('view_all'))

    user_id = request.args.get('view')
    single = Records.query.filter_by(id=user_id).first()
    return render_template('edit.html', records=single)


@app.route('/dashboard', methods=['get', 'POST'])
@login_required
def dashboard():
    male = 0
    female = 0
    length = Records.query.all()
    todo_db_len = len(length)

    for lent in length:
        if lent.gender == 'male':
            male += 1
        else:
            female += 1
    return render_template('dashboard.html', length=todo_db_len, male=male, female=female)


@app.route('/profile', methods=['get', 'POST'])
def profile():
    if request.method == "POST":

        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if current_password == current_user.password:
            if new_password == confirm_password:
                single = Users.query.filter_by(id=id).first()


                single.name = name
                single.email = email
                single.password = confirm_password

                db.session.add(single)
                db.session.commit()

    return render_template('profile.html')


@app.route("/logout")
def logout():
    logout_user()
    return render_template("login.html")


@login_manager.user_loader
def load_user(users_id):
    if users_id is not None:
        return Users.query.get(users_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("Login is required")
    return redirect(url_for('logout'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
