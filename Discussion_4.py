from flask import Flask, request, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

class WeatherInfo(FlaskForm):
	zip_code = StringField("Enter any US zip code:", validators=[Required()])
	submit = SubmitField('Submit')

	def validate_zip_code(self, field):
		if len(str(field.data)) != 5:
			raise ValidationError("Please enter a valid 5-digit zip code.")

@app.route('/weather_form', methods = ['GET','POST'])
def weatherForm():
	form = WeatherInfo()
	if form.validate_on_submit():
		print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		base_url = "https://api.openweathermap.org/data/2.5/weather?"
		params_diction = {}
		params_diction["zip"] = form.zip_code.data
		params_diction["APPID"] = '366e9ab271a2967f2012be6f179a537e'
		resp = requests.get(base_url, params = params_diction)
		text = resp.text
		python_obj = json.loads(text)
		print(python_obj)

		current_temp = python_obj['main']['temp']
		weather_desc = python_obj['weather'][0]['description']
		name = python_obj['name']
		return render_template('weather_results.html', temp = current_temp, weather = weather_desc, name = name)
	flash(form.errors)
	return render_template('weather_zip.html', form = form)


if __name__ == "__main__":
	app.run(use_reloader=True,debug=True)