from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from website import logic
import logging
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["JWT_SECRET_KEY"] = "asjdaskjdajsjdksajjdksajkdas"
jwt = JWTManager(app)
db = SQLAlchemy(app)




#baza danych dla rejestracji
class SignIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    confirm_password = db.Column(db.String, nullable=False)


class KDA(db.Model):
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
        dbname = SignIn.query.filter_by(name=name, password=password).first()
        if dbname:
            if dbname.name == name and dbname.password == password:
                access_token = create_access_token(identity=dbname.name)
                return render_template("search.html")

        else:
            return jsonify({"msg": "Bad username or password"}), 401

    return render_template("login.html")




@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = SignIn.query.filter_by(name=get_jwt_identity()).first()

    return current_user


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        summoner = request.form['summoner']
        return render_template("test.html", summoner=summoner)
    return render_template("search.html")



@app.route('/test')
def test():
    return render_template("test.html")




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




# from datetime import datetime

#This are hardcoded region name and tagline of my account feal free to change it
region = 'europe'
name = 'Porsze'
tag_line = 'EUNE'
API_KEY_FILE_PATH = './API_KEY' #change path to pointing to your coresponding API_key
# API_KEY_FILE_PATH = './API_KEY_OLD' #old key
# API key you can get from https://developer.riotgames.com/ in your account dashboard


# function reused later to request all API endpints
def standard_get(path=''):
    r = requests.get(f'https://{region}.api.riotgames.com{path}?api_key={api_key}')
    if r.status_code == 200:
        return r.json()
    if r.status_code != 200:
        logging.log(msg = f'main() func - status: {r.status_code}', level = 50)
        return r.json() #Here should be backup or database.


def get_api_key():
    try:
        with open(API_KEY_FILE_PATH, 'r') as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        print(f"Error: apikey file path not found.")
        return None





# function get out user puuid, after we have imidiatly call this func to store puuid in variable
def puuid_get():
    # r = requests.get('https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/121512511/EUNE?api_key=RGAPI-4a07bcfa-a6ee-46ad-b676-ab0efd1c710a')
    r = standard_get(path=f'/riot/account/v1/accounts/by-riot-id/{name}/{tag_line}')
    try:
        return r['puuid']
    except Exception as e:
        logging.log(msg=f'puuid_get() func - response: {r}', level = 40)
        logging.log(msg={e}, level = 50)
        return None


def lol_history():
    try:
        r = standard_get(path =f'/lol/match/v5/matches/by-puuid/{puuid}/ids')
        return r
    except Exception as e:
        logging.log(msg=f'error {e} ocurre', level=50)


def match_details(match_id):
    try:
        idx = match_history[match_id]['metadata']['participants'].index(puuid)
        kills = match_history[match_id]['info']['participants'][idx]['kills']
        deaths = match_history[match_id]['info']['participants'][idx]['deaths']
        assists = match_history[match_id]['info']['participants'][idx]['assists']
        # game_end_timestamp = datetime.fromtimestamp((match_history[match_id]['info']['gameEndTimestamp'])/1000)
        # champion_name = match_history[match_id]['info']['participants'][idx]['championName']
        # champion_ID = match_history[match_id]['info']['participants'][idx]['championId']

        if match_history[match_id]['info']['participants'][idx]['win']:
            temp_str = 'Win'
        else:
            temp_str = 'Lose'

        if deaths == 0:
            return_str = f'{kills}/{deaths}/{assists} KDA: PERFECT \t{temp_str}'
        else:
            return_str = f'{kills}/{deaths}/{assists} KDA: {round(kills + assists / deaths, 2)} \t{temp_str}'
            # f'{champion_name}: {champion_ID} \t{game_end_timestamp}'
        return print(return_str)
    except Exception as e:
        logging.log(msg=f'error in match_details() func - {e}', level=50)


api_key = get_api_key()
puuid = puuid_get()
match_history = {}