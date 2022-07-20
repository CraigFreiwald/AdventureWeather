# -----------------------------------------------------------------------------------------#
#                             IMPORTS
# -----------------------------------------------------------------------------------------#
import requests
from flask import Flask, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

# -----------------------------------------------------------------------------------------#
#                       APP and DB CONFIG
# -----------------------------------------------------------------------------------------#
app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weatherlocs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# set url for api call to obtain city ID numbers
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=66e64fc4eb7e73b64c9e5eeccfcaed4c'


# -----------------------------------------------------------------------------------------#
#                     SET ORM MODEL ClASSES FOR DB
# -----------------------------------------------------------------------------------------#
class City(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(25), nullable=False)


# -----------------------------------------------------------------------------------------#
#                     SET HTTP ROUTES
# -----------------------------------------------------------------------------------------#
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return do_admin_login()


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        session['logged_in'] = True
        return index()
    else:
        flash('Login Unsuccessful. Please check you Username and Password and try Again')
        return home()


@app.route('/weather', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        new_city = request.form.get('city')
        cities = City.query.all()
        if new_city:
            for city in cities:
                if city.name == new_city:
                    print('City name already exists within user list')
                    flash('City name already exists within user list')
                    return render_template('weather.html', usersList=createList())
                elif searchAPI_DB(new_city):
                    print('invalid city name entered')
                    flash('Invalid city name entered, please check spelling and try again')
                    return render_template('weather.html', usersList=createList())
                else:
                    new_city_obj = City(name=new_city)
                    db.session.add(new_city_obj)
                    db.session.commit()

    return render_template('weather.html', usersList=createList())


# bad city error check
def searchAPI_DB(city):

    try:
        requests.get(url.format(city)).json()
    except KeyError:
        print('invalid city name entered')


# method to create list of Cities using API call and from DB info
def createList():
    # create list from DB model data
    cities = City.query.all()

    # create list to pass objects to template api
    usersList = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()

        userLoc = {
            'cityname': city.name,
            'cityID': r['id']
        }

    return usersList


if __name__ == '__main__':
    app.run(debug=True)

