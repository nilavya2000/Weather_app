from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] : 'sqlite:///weather.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class city(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
	url='http://api.openweathermap.org/data/2.5/weather?q={}&appid=da607fdc1833d3f1052c37181b2c452c'
	city='siliguri'
	r= requests.get(url.format(city)).json()
	

	weather = {
		'city' : city,
		'temperature' : r['main']['temp'],
		'description' : r['weather'][0]['description'],
		'icon' : r['weather'][0]['icon'],
	}
	print(weather)
	return render_template('index1.html', weather=weather)

if __name__ == '__main__':
   app.run(debug=True) 