import requests
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		new_city = request.form.get('city')

		if new_city:
			
			new_city_obj = City(name=new_city)
			db.session.add(new_city_obj)
			db.session.commit()


	cities = City.query.order_by(City.id.desc())

	weather_data = []

	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3090f73c10a247abcf71580aec532829'

	for city in cities:

		r = requests.get(url.format(city.name)).json()
		
		weather = {
			'city' : city.name,
			'temperature' : r['main']['temp'],
			'description' : r['weather'][0]['description'],
			'icon' : r['weather'][0]['icon'],
		}

		weather_data.append(weather)

	return render_template('weather.html', weather_data=weather_data)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
	if request.method == 'GET':
		name = City.query.all()

		if name:
			City.__table__.drop()
			db.session.create_all()
			db.session.commit()
		
		
	return redirect('/')
'''
	db.drop_all()
	db.session.create_all()
	db.session.commit()
	return redirect(url_for('weather'))
'''

if __name__ == '__main__':
	app.run(debug=True)