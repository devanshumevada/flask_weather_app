import requests
from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_data.db'
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        city_to_check = request.form.get('city')

        if city_to_check:
            city_to_check_obj = City(name=city_to_check)
            db.session.add(city_to_check_obj)
            db.session.commit()
    all_cities = City.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=efb5873a54c481225b7ef9b052a12b5c'
    weather_all = []

    for city in all_cities:
        response = requests.get(url.format(city.name)).json()

        weather_data = {
            'city': city.name,
            'temperature':response['main']['temp'],
            'description':response['weather'][0]['description'],
            'icon':response['weather'][0]['icon'],
        }

        weather_all.append(weather_data)
    return render_template('index.html',weather_all=weather_all)

if __name__ == '__main__':
    app.run(debug=True)