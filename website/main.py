from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["JWT_SECRET_KEY"] = "asjdaskjdajsjdksajjdksajkdas"
jwt = JWTManager(app)
db = SQLAlchemy(app)


#testowa db
# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)


#baza danych dla rejestracji
class SignIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    confirm_password = db.Column(db.String, nullable=False)


#strona glowna
@app.route('/')
def home():
    return render_template("index.html")


#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        dbname = SignIn.query.filter_by(name=name).first()
        if dbname:
            if dbname.name == name:
                return render_template("search.html")
            else:
                return render_template("login.html")
        else:
            return render_template("login.html")
    return render_template("login.html")


@app.route('/search')
def search():
    return render_template("search.html")

#
# def compare_strings(input_username):
#     # Query the database to get the user with the provided username
#     user_from_db = SignIn.query.filter_by(name=input_username).first()
#
#     if user_from_db:
#         # If the user is found in the database, compare the strings
#         if user_from_db.username == input_username:
#             result = f"The input username '{input_username}' matches the username from the database."
#         else:
#             result = f"The input username '{input_username}' does not match the username from the database."
#     else:
#         result = f"The username '{input_username}' does not exist in the database."
#
#     return result


#
# @app.route('/test',methods=['GET', 'POST'])
# def test():
#
#
#     return render_template()




#rejestracja
@app.route('/sign-up',methods=['GET', 'POST'])
def sign_up():
    db.create_all()
    if request.method == 'POST':
        signin = SignIn(name=request.form['username'], email=request.form['email'], password=request.form['password'], confirm_password=request.form['confirmPassword'])
        db.session.add(signin)
        db.session.commit()

    signins = SignIn.query.all()
    return render_template("sign-up.html", signins=signins)


#jakies testowe gowno
# @app.route('/todo', methods=['GET', 'POST'])
# def todo():
#     db.create_all()
#     if request.method == 'POST':
#         task = Task(name=request.form["task"])
#         db.session.add(task)
#         db.session.commit()
#
#     tasks = Task.query.all()
#     return render_template("todo.html", tasks=tasks)


app.run()
