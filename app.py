import pyrebase
import requests
from flask import *

config = {
     "apiKey": "available on your firebase dashboard",
     "authDomain": "available on your firebase dashboard",
     "databaseURL": "available on your firebase dashboard",
     "projectId": "available on your firebase dashboard",
     "storageBucket": "available on your firebase dashboard",
     "messagingSenderId": "available on your firebase dashboard"
}



firebase = pyrebase.initialize_app(config)

db_f = firebase.database()
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        city_to_check = request.form.get('city')

        if city_to_check:
            db_f.child("city").push({"name": city_to_check})
            
    all_cities_f = db_f.child("city").get()
    t = all_cities_f.val()
    all_cities = t.values()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=get_your_app_id_on_openweathermap_website_and_paste_it_here'
    weather_all = []

    for city in all_cities:
        response = requests.get(url.format(city['name'])).json()

        weather_data = {
            'city': city['name'],
            'temperature':response['main']['temp'],
            'description':response['weather'][0]['description'],
            'icon':response['weather'][0]['icon'],
        }

        weather_all.append(weather_data)
    return render_template('index.html',weather_all=weather_all)

if __name__ == '__main__':
   app.run(debug=True)
