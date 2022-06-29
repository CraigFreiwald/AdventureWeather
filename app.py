# -----------------------------------------------------------------------------------------#
#                             IMPORTS
# -----------------------------------------------------------------------------------------#
import requests
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

# -----------------------------------------------------------------------------------------#
#                       APP and DB CONFIG
# -----------------------------------------------------------------------------------------#
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weatherlocs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)


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


@app.route('/login', methods=['GET'])
def do_admin_login():
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        session['logged_in'] = True
        return index()
    else:
        return home()


@app.route('/weather', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    # create list from DB model data
    cities = City.query.all()

    # set url for api call to obtain city ID numbers
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=66e64fc4eb7e73b64c9e5eeccfcaed4c'

    # create list to pass objects to template api
    usersList = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()

        userLoc = {
            'cityname': city.name,
            'cityID': r['id']
        }

        usersList.append(userLoc)

    return render_template('weather.html', usersList=usersList)


if __name__ == '__main__':
    app.run(debug=True)

