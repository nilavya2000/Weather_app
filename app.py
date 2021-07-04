from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class city(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

def g_w(c):
	url='http://api.openweathermap.org/data/2.5/weather?q={}&appid=da607fdc1833d3f1052c37181b2c452c'
	r= requests.get(url.format(c)).json()
	return r


@app.route('/')
def index_get():	
	cities = city.query.all()
		
	weather_data=[]
	for c in cities:
		r= g_w(c.name)

		weather = {
			'city' : c,
			'temperature' :round( r['main']['temp'] - 273.15),
			'humidity': r['main']['humidity'],
			'description' : r['weather'][0]['description'],
			'icon' : r['weather'][0]['icon'],
		}
		
		weather_data.append(weather)
	t=datetime.now()
	t_now = t.strftime("%H:%M:%S")
	print(t_now)
	return render_template('index1.html', weather_data=weather_data, t_now=t_now)




@app.route('/', methods=['POST'])
def index_post():
	e_r=''
	
	new_city = request.form.get('city')
	if new_city:
		e_city = city.query.filter_by(name=new_city).first()

		if not e_city:
			n_d_obj = g_w(new_city)
			if n_d_obj['cod']==200:
				new_city_obj = city(name=new_city)
				db.session.add(new_city_obj)
				db.session.commit()
			else:
				e_r='city doesnot exist in the world '
		else:
			e_r='City already exist. '
	return redirect(url_for('index_get'))


@app.route('/delete/<name>/')
def delete_city(name):
	c_name=city.query.filter_by(name=name).first()
	db.session.delete(c_name)
	db.session.commit()
	
	return redirect(url_for('index_get'))

if __name__ == '__main__':
   app.run(debug=True) 
