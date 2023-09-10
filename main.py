import datetime

from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):

        user = Paid_user.query.get(int(user_id))
        if user:
            return user
        return None

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    class Paid_user(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(1000))
        name = db.Column(db.String(1000))
        role = db.Column(db.String(100))

    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        paid_user_id = db.Column(db.Integer, db.ForeignKey('paid_user.id'), nullable=False)
        paid_user = db.relationship('Paid_user', backref=db.backref('users', lazy=True))
        results = db.Column(db.String(100), nullable=False)
        news = db.Column(db.String(100))
        discounts = db.Column(db.String(100))
        results_done = db.Column(db.String(100))

    class items_not_done(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        case = db.Column(db.String(100))
        notes = db.Column(db.String(100))
        phone = db.Column(db.String(100))

    class items_done(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        case = db.Column(db.String(100))
        notes = db.Column(db.String(100))
        phone = db.Column(db.String(100))
        fees = db.Column(db.Integer)

    class analysis(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        price = db.Column(db.Integer)



    class news(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100))
        des = db.Column(db.String(100))

    class discounts(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        des = db.Column(db.String(100))

    class employees(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        phone = db.Column(db.Integer)
        Date = db.Column(db.DateTime, nullable=False)

    class messages(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.Integer)
        name = db.Column(db.String(100))
        message = db.Column(db.String(1000))
    class loves(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.Integer)
        name = db.Column(db.String(100))
        message = db.Column(db.String(1000))





    db.create_all()

class MyModelView(ModelView):
    def is_accessible(self):
        return True

admin = Admin(app)
admin.add_view(MyModelView(Paid_user, db.session))
admin.add_view(MyModelView(items_not_done, db.session))
admin.add_view(MyModelView(items_done, db.session))
admin.add_view(MyModelView(news, db.session))
admin.add_view(MyModelView(discounts, db.session))
admin.add_view(MyModelView(analysis, db.session))
admin.add_view(MyModelView(employees, db.session))
admin.add_view(MyModelView(loves, db.session))

@app.route('/')
def index():
    user_name = current_user
    return render_template('index.html', user_name=user_name)

@app.route('/loggedin')
@login_required
def logged():
    if current_user.role=="user":
        y = [10, 50, 30, 40, 50]
        x = ["urin1", "urin2", "urin3", "urin4", "urin5"]
        results = []
        items=items_not_done.query.all()
        for f in items:
            if f.phone == current_user.phone:
                results.append(f)
        done=items_done.query.all()
        new=news.query.all()
        dis=discounts.query.all()
        return render_template('dash.html', user_name=current_user.name, labels=x, data=y, items=results, done=done, news=new, discounts=dis)
    if current_user.role=="data entry":
        y = [10, 50, 30, 40, 50]
        x = ["urin1", "urin2", "urin3", "urin4", "urin5"]
        new = news.query.all()
        dis = discounts.query.all()
        all_messages=[]
        m=loves.query.all()
        for i in m :
            print(i.phone)
            print(current_user.phone)
            if i.phone==int(current_user.phone):
                print("iam here ")
                all_messages.append(i.message)
        print(all_messages)
        print(m)
        return render_template('data_entry.html', labels=x, data=y, user_name=current_user.name,news=new, discounts=dis,all_messages=all_messages)
    if current_user.role=="admin":
        y = [10, 50, 30, 40, 50]
        x = ["urin1", "urin2", "urin3", "urin4", "urin5"]
        name = analysis.query.all()
        price = analysis.query.all()
        all = items_done.query.all()
        total_fees = db.session.query(db.func.sum(items_done.fees)).scalar()
        all_users=Paid_user.query.all()
        for i in all_users:
            if i.role=="admin" or i.role=="user":
                pass
            else:
                print(i.role)
                found=employees.query.filter_by(phone=i.phone).first()
                if not found:


                        employee=employees(
                            name=i.name,phone=i.phone,
                            Date=datetime.datetime.today()
                        )
                        db.session.add(employee)
                        db.session.commit()

        return render_template('admin.html', labels=x, data=y, user_name=current_user.name, name=name, price=price, all=all, total_fees=total_fees)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        phone = request.form.get('number')
        password = request.form.get('password')
        user = Paid_user.query.filter_by(phone=phone).first()

        if not user:
            flash("That phone number does not exist, please try again.")
        elif not check_password_hash(user.password, password):
            flash('Incorrect password, please try again.')
        else:
            login_user(user)
            return redirect(url_for('logged'))

    return render_template("login.html")

@app.route('/not_done', methods=['GET', 'POST'])
def not_done():
    if request.method == 'POST':
        name = request.form.get("name")
        case = request.form.get("case")
        notes=request.form.get("notes")
        phone=request.form.get("phone")
        # Get other form fields as needed

        not_done=items_not_done(
            name=name,
            case=case,
            notes=notes,
            phone=phone
        )
        db.session.add(not_done)
        db.session.commit()

        return 'Form submitted successfully!'

    return render_template('not_done.html')
@app.route('/done', methods=['GET', 'POST'])
def done():

    if request.method == 'POST':
        name = request.form.get("name")
        case = request.form.get("case")
        notes=request.form.get("notes")
        phone=request.form.get("phone")
        # Get other form fields as needed
        item = items_not_done.query.filter_by(name=name).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            print("Item deleted successfully.")
        else:
            print("Item not found.")
        analysi=analysis.query.filter_by(name=name).first()
        fees=analysi.price
        not_done=items_done(
            name=name,
            case=case,
            notes=notes,
            phone=phone,
            fees=fees
        )
        db.session.add(not_done)
        db.session.commit()
    return render_template("done.html")

@app.route('/add_analysis', methods=['GET','POST'])
def add_analysis():
    if request.method=='POST':
        name = request.form.get('name')
        price = request.form.get('price')
        found=analysis.query.filter_by(name=name).first()
        if found:
            return """
            <script>
                setTimeout(function() {
                    window.location.href = '/pricing';
                }, 1000);
            </script>
            <p>This analysis has already been found. You will be redirected in 1 second...</p>
            """

        add_analysis = analysis(name=name, price=price)
        db.session.add(add_analysis)
        db.session.commit()
        return redirect(url_for('logged'))
    return redirect(url_for('logged'))

@app.route("/pricing")
def pricing():
    all=analysis.query.all()
    return render_template("prices.html",all=all)

@app.route("/messages", methods=["GET","POST"])
def messages():
    if request.method=="POST":
        name = request.form.get('name')
        message = request.form.get('message')
        employee = employees.query.filter_by(name=name).first()
        if employee:
            new_message = loves(phone=employee.phone,name=employee.name,message=message)
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('logged'))
    return render_template('messages.html')


@app.route("/edit",methods=["GET","POST"])
def edit():
    if request.method=="POST":
        name=request.form.get("name")
        price=request.form.get("price")
        found=analysis.query.filter_by(name=name).first()
        if found:
            found.price = price  # Update the price
            db.session.commit()  # Save the changes to the database
            return "Price updated successfully"
        else:
            return "No record found with the given name"
    return render_template("edit.html")
@app.route("/")
@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if request.method == 'POST':
        newss = request.form.get('news')
        description = request.form.get('des')
        print(news)
        print(description)

        new_post = news(title=newss, des=description)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('logged'))

    return redirect(url_for('logged'))


@app.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    post=news.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('logged'))





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('number')
        password = request.form.get('password')
        name = request.form.get('name')
        print(password)

        existing_user = Paid_user.query.filter_by(phone=phone).first()
        if existing_user:
            flash("An account with that phone number already exists.")
        else:
            hashed_password = generate_password_hash(password)
            new_user = Paid_user(phone=phone, password=hashed_password, name=name, role="user")
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.")

            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)