# -----------------------------------------------------------------------------------------#
#                             IMPORTS
# -----------------------------------------------------------------------------------------#
import requests
from model import db
from flask import Flask, render_template, request, session


# -----------------------------------------------------------------------------------------#
#                       APP and DB CONFIG
# -----------------------------------------------------------------------------------------#


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UsersAndCities.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True


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

    # create list from DB model.py data
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

