from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Function to fetch weather data
def get_weather_data(location, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Weather result route
@app.route('/weather', methods=['POST'])
def weather():
    location = request.form['location']
    api_key = "cf11a443c5175ed8d1cb7c22dc434177"  # Replace with your OpenWeatherMap API key
    weather_data = get_weather_data(location, api_key)
    
    if weather_data:
        city = weather_data['name']
        country = weather_data['sys']['country']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather_description = weather_data['weather'][0]['description']
        
        return render_template('result.html', city=city, country=country, temperature=temperature, 
                               humidity=humidity, description=weather_description.capitalize())
    else:
        return render_template('error.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
